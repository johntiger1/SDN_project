import pyshark
import os
import sys
import re
import json
import csv

class trace_handler():
	
	def __init__ (self,threshold):
		self.threshold = threshold

	def set_threshold(self,threshold):
		self.threshold = threshold

	def get_trace_controller(self, tracepath):
		#trace_file = os.path.expanduser('~')+'/Downloads/univ1_trace/univ1_pt1'
		try:
			cap = pyshark.FileCapture(tracepath,only_summaries=True)
		except:
			sys.stderr.write("Importing file failed.\n")
		#print cap[0]
		return cap

	# source_key & dest_key : "ip_port"
	def get_app_flow(self, cap):
		res = {}
		pattern = re.compile(ur"[0-9]{1,5}\\xe2\\x86\\x92[0-9]{1,5}",re.UNICODE)
		i = 0
		for pkt in cap: # assume times are in order
			if pkt.protocol == "TCP":	

				source_ip = pkt.source
				dest_ip = pkt.destination

				# get ports
				# harzard!!!!! (PDU segments have no ports information)
				# skip those pkts
				isFound = pattern.search(pkt.info)
				if isFound  == None:
					continue
				ports = pattern.search(pkt.info).group(0)
				ports = ports.split("\\xe2\\x86\\x92")

				source_port = ports[0] #str
				dest_port = ports[1]


				source_key = source_ip + "_" + source_port
				dest_key = dest_ip + "_" + dest_port
				app_key = source_key + "_" + dest_key

				content = {"pkt_info": pkt.info, "pkt_time": pkt.time, "pkt_len":pkt.length}

				if app_key in res.keys():
					res[app_key].append(content)
				else:
					res[app_key] =[content]
		print "finished hashtable collection"
		with open('univ1_pt1_flow.csv', 'w') as f:
			header = ['source_ip','destination_ip','source_port', 'destination_port','init_time','duration','size']
			writer = csv.DictWriter(f, header)
			writer.writeheader()

			for k in res.keys():
				flow_start_time = float(res[k][0]['pkt_time'])
				last_time = float(res[k][0]['pkt_time'])
				flow_duration = 0
				flow_size = 0
				addrs = k.split('_')
				pkt_counts = len(res[k])
				new_flow = True
				count = 0
				for pkt in res[k]:
					if addrs[0] == "41.177.117.184" and addrs[1] == "1618" and addrs[3] == "51332" and addrs[2] == "41.177.3.224":
						print pkt['pkt_len']," ", pkt['pkt_time']
						import pdb;pdb.set_trace()
					else:
						continue
					pkt_time = float(pkt['pkt_time'])	
					pkt_length = int(pkt['pkt_len'])
					delta_time = pkt_time - last_time
					assert (delta_time >= 0)
					if count < pkt_counts-1:

						if delta_time > self.threshold:
							writer.writerow({'source_ip':addrs[0],'destination_ip':addrs[2],'source_port':addrs[1], 'destination_port':addrs[3],'init_time':flow_start_time,'size':flow_size,'duration':flow_duration})
							f.flush()
							last_time = pkt_time
							#reset default values
							flow_start_time = pkt_time
							flow_duration = 0
							flow_size = pkt_length
						else:
							last_time = pkt_time
							flow_duration = pkt_time - flow_start_time
							flow_size += pkt_length
					else:
						if delta_time > self.threshold:
							writer.writerow({'source_ip':addrs[0],'destination_ip':addrs[2],'source_port':addrs[1], 'destination_port':addrs[3],'init_time':flow_start_time,'size':flow_size,'duration':flow_duration})
							f.flush()
							last_time = pkt_time
							flow_duration = 0
							flow_start_time = pkt_time
							flow_size = pkt_length
						else:
							flow_duration = pkt_time - flow_start_time
							flow_size += pkt_length
						writer.writerow({'source_ip':addrs[0],'destination_ip':addrs[2],'source_port':addrs[1], 'destination_port':addrs[3],'init_time':flow_start_time,'size':flow_size,'duration':flow_duration})
						f.flush()
					count += 1