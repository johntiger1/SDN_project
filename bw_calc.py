#!/usr/local/bin/python
import csv
import sys
import operator
FLOW_FILE = "Univ1_flows_at_01.csv"
GROUP_SIZE = 4
DURATION = 0.3
csv.field_size_limit(sys.maxsize)
reader = csv.reader(open(FLOW_FILE), delimiter=";")

output_file = "bandwidth.csv"
#import pdb;pdb.set_trace()
reader = list(reader)[1:]
f = open(output_file, 'w')
header = ['key','time']
header += [i for i in range(0,GROUP_SIZE)]
#print header
writer = csv.DictWriter(f, header)
writer.writeheader()

cur_src_ip = None # since sorted format: srcip_srcport_desip_desport, so can only processed by srcip
cur_time = None
s_time = None
pre_process_flows_per_src_ip = []
# buckets: [{0:[flows within 300ms]}, {1:[flows within the next 300ms]}, ...]
cur_buckets = []

def get_key(src_port, des_port):
	return (src_port ^ des_port) % GROUP_SIZE

def re_aggr(ready_list, src_ip_key):
	for flow in ready_list:
		flow_key_list = flow[0].split("_")
		src_ip = flow_key_list[0]		
		src_port = flow_key_list[1]
		des_ip = flow_key_list[2]
		des_port = flow_key_list[3]
		flow_key_list[1] = des_ip
		flow_key_list[2] = src_port
		flow[0] = "_".join(flow_key_list)
	ready_list = sorted(ready_list, key = operator.itemgetter(0))
	cur_des_ip = ready_list[0][0].split("_")[1]

	pair_ip_flows = []

	for i in range(0, len(ready_list)):
		flow_key_list = ready_list[i][0].split("_")
		src_ip = flow_key_list[0]		
		des_ip = flow_key_list[1]
		src_port = flow_key_list[2]
		des_port = flow_key_list[3]

		if des_ip == cur_des_ip and i != len(ready_list)-1: # gather all flows with the same src_ip
			pair_ip_flows.append(ready_list[i])
			continue	
		try:
			calc_bw(pair_ip_flows, src_ip_key, cur_des_ip)
		except IndexError:
			continue

		#initalize pre_process_flows list for the next src ip
		cur_des_ip = des_ip
		print cur_des_ip
		pair_ip_flows = [ready_list[i]]

def calc_bw(pair_ip_flows, src_ip_key, cur_des_ip):# calc per ip_pair
	n = 0
	# pair_ip_flows: [["ip_ip_port_port", init_time, duration, size],...]
	count = 0
	s_key = src_ip_key + "_" + cur_des_ip
	#print len(pair_ip_flows)
	keys = []
	#results = []
	for _ in pair_ip_flows:
		_[1] = float(_[1])

	pair_ip_flows = sorted(pair_ip_flows, key = operator.itemgetter(1))
	for i in range(0,GROUP_SIZE):
		keys.append(i)
	#import pdb;pdb.set_trace()
	buckets = dict.fromkeys(keys,0)
	#import pdb;pdb.set_trace()
	#print pair_ip_flows
	cur_time = pair_ip_flows[0][1]
	s_time = pair_ip_flows[0][1] + DURATION
	for i in range(0, len(pair_ip_flows)):
		flow = pair_ip_flows[i]
		flow_time = flow[1]
		flow_size = int(flow[3])

		if i < (len(pair_ip_flows)-1):
			if flow_time <= s_time: 
				#import pdb;pdb.set_trace()
				addrs = flow[0].split("_")
				src_port = int(addrs[2])
				des_port = int(addrs[3])
				k = get_key(src_port, des_port)
				buckets[k] += flow_size
				#print "flow %s added." % i
				continue
			else:
				dur = DURATION + n*DURATION
				row = buckets
				row.update({'key':s_key, 'time':dur})
				#print row
				writer.writerow(row)
				n += 1
				#initialize
				s_time = cur_time + DURATION + n*DURATION
				while(flow_time > s_time):
					n += 1
					s_time =cur_time + DURATION + n*DURATION

				buckets = dict.fromkeys(keys,0)
				addrs = flow[0].split("_")
				src_port = int(addrs[2])
				des_port = int(addrs[3])
				k = get_key(src_port, des_port)
				buckets[k] += flow_size
				#print "flow %s added." % i
		else:
			if flow_time <= s_time: 
				#import pdb;pdb.set_trace()
				dur = n*DURATION
				addrs = flow[0].split("_")
				src_port = int(addrs[2])
				des_port = int(addrs[3])
				k = get_key(src_port, des_port)
				buckets[k] += flow_size
				#print "flow %s added." % i
			else:
				dur = DURATION + n*DURATION
				s_time = cur_time + DURATION + n*DURATION
				while(flow_time > s_time):
					n += 1
					s_time =cur_time + DURATION + n*DURATION
				buckets = dict.fromkeys(keys,0)
				addrs = flow[0].split("_")
				src_port = int(addrs[2])
				des_port = int(addrs[3])
				k = get_key(src_port, des_port)
				buckets[k] += flow_size
				#print "flow %s added." % i
			row = buckets
			row.update({'key':s_key, 'time':dur})
			#print row
			writer.writerow(row)
				
				 
		# write into file:
		
# check init time order
	for i in range(0, len(pair_ip_flows)-1):
		assert pair_ip_flows[i+1][1] >= pair_ip_flows[i][1]

	

for i in range(0,len(reader)): # iterating flows
	#import pdb;pdb.set_trace()
	flow = reader[i][0].split(",")

	flow_key_list = flow[0].split("_")

	src_ip = flow_key_list[0]
	'''
	src_port = flow_key_list[1]
	des_ip = flow_key_list[2]
	des_port = flow_key_list[3]
	'''
	if cur_src_ip == None: # initialize
		cur_src_ip = src_ip
		pre_process_flows_per_src_ip = [flow]
		continue

	if src_ip == cur_src_ip and i != len(reader)-1: # gather all flows with the same src_ip
		pre_process_flows_per_src_ip.append(flow)
		continue	

	re_aggr(pre_process_flows_per_src_ip, cur_src_ip)

	#initalize pre_process_flows list for the next src ip
	cur_src_ip = src_ip
	pre_process_flows_per_src_ip = [flow]
	
	'''
	init_time = flow[1]
	flow_size = flow[3]
	'''
