import pyshark
import os
import sys
import re
import json
import csv

class trace_handler():
	
	def get_trace_controller(self, tracepath):
		trace_file = os.path.expanduser('~')+'/Downloads/univ1_trace/univ1_pt1'

		try:
			cap = pyshark.FileCapture(trace_file,only_summaries=True)
		except:
			sys.stderr.write("Importing file failed.\n")
		#print cap[0]
		return cap

	# source_key & dest_key : "ip_port"
	def get_app_flow(self, cap):
		res = {}
		'''
		count_map = {}
		i = 0
		for _ in cap:
			if _.protocol == "TCP":
				info = _.info.split(" ")
				if len(info) in count_map:
					count_map[len(info)] = count_map[len(info)] + 1
				else:
					print "%s: %s" % (len(info), str(info))
					count_map[len(info)] = 1
		print count_map
		exit()
		'''
		#import pdb;pdb.set_trace()
		pattern = re.compile(ur"[0-9]{1,5}\\xe2\\x86\\x92[0-9]{1,5}",re.UNICODE)
		i = 0
		for pkt in cap:
			if pkt.protocol == "TCP":			
				source_ip = pkt.source
				dest_ip = pkt.destination

				# get ports
				# harzard!!!!!
				isFound = pattern.search(pkt.info)
				if isFound  == None:
					print pkt.no, ": ", pkt.info
					i = i + 1
					continue
				ports = pattern.search(pkt.info).group(0)
				ports = ports.split("\\xe2\\x86\\x92")

				source_port = ports[0]
				dest_port = ports[1]

				source_key = source_ip + "_" + source_port
				dest_key = dest_ip + "_" + dest_port
				app_key = source_key + "_" + dest_key

				content = {"pkt_info": pkt.info, "pkt_time": pkt.time, "pkt_len":pkt.length}

				if app_key in res.keys():
					res[app_key].append(content)
				else:
					res[app_key] =[content]
		with open('univ1_pt1.csv', 'w') as f:
			header = ['source_ip','destination_ip','source_port', 'destination_port','init_time','length','info']
			writer = csv.DictWriter(f, header)
			writer.writeheader()
			for _ in res.keys():
				addrs = _.split('_')
				for e in res[_]:
					writer.writerow({'source_ip':addrs[0],'destination_ip':addrs[2],'source_port':addrs[1], 'destination_port':addrs[3],'init_time':e['pkt_time'],'length':e['pkt_len'],'info':e['pkt_info']})
		#print i
