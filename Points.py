import pyshark
import os
import sys
import re
import json
import csv

class trace_handler():
	
	def __init__ (self,threshold):
		self.threshold = threshold
		self.temp = True
		self.number_file = 1

	def set_number_file(self,i):
		self.number_file = i
	def set_threshold(self,threshold):
		self.threshold = threshold

	def set_output_by_key(self, temp):
		self.temp = temp

	def get_trace_controller(self, tracepath):
		#trace_file = os.path.expanduser('~')+'/Downloads/univ1_trace/univ1_pt1'
		try:
			cap = pyshark.FileCapture(tracepath, only_summaries=True)
		except:
			sys.stderr.write("Importing file failed.\n")
		#print cap[0]
		return cap

	def get_timestamp_list(self):
		init_timestamps_list = []
		i = 1
		trace_file = os.path.expanduser('~')+'/Downloads/univ1_trace/univ1_pt'
		#TIME_THRESHOLD = 0.1
		while i<=20:
			path = trace_file+str(i) 
			cap = pyshark.FileCapture(path)
			for pkt in cap:
				init_timestamps_list.append(float(pkt.sniff_timestamp))
				break
			i += 1
		print init_timestamps_list
		return init_timestamps_list

	# source_key & dest_key : "ip_port"
	def get_app_flow(self, cap, init_time_list):
		timestamp_list = init_time_list
		res={}
		pattern = re.compile(ur"[0-9]{1,5}\\xe2\\x86\\x92[0-9]{1,5}",re.UNICODE)
		
		for pkt in cap: # assume times are in order
			#import pdb;pdb.set_trace()
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

				content = {"pkt_time": pkt.time, "pkt_len":pkt.length}
				if app_key in res.keys():
					res[app_key].append(content)
				else:
					res[app_key] =[content]

		print "finished hashtable collection"

		with open('new_univ1_pt'+str(self.number_file)+'_flow_key_time_points.csv', 'w') as f:
			header = ['key','size', 'points']
			writer = csv.DictWriter(f, header)
			writer.writeheader()

			for k in res.keys():
				time_points = []
				flow_size = []
				for pkt in res[k]:
					time_points.append(str(format(float(pkt['pkt_time'])+timestamp_list[self.number_file-1], ".6f")))
					flow_size.append(pkt['pkt_len'])
				writer.writerow({'key':k,'size':"|".join(flow_size),'points':"|".join(time_points)})
				f.flush()