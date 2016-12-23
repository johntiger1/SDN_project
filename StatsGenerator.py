import pyshark
import os
import sys
import re
import json
import csv

class trace_handler():

	def get_trace_controller(self, tracepath):
		try:
			cap = pyshark.FileCapture(tracepath, only_summaries=True)
		except:
			sys.stderr.write("Importing file failed.\n")
		return cap

	def get_timestamp_dict(self, PIECE_NUMBER, DIR, trace_files):		
		init_timestamps_dict = {}

		for file in trace_files:
			path = DIR+"/"+file
			cap = pyshark.FileCapture(path)
			for pkt in cap:
				init_timestamps_dict[file] = (float(pkt.sniff_timestamp))
				break

		return init_timestamps_dict

	# source_key & dest_key : "ip_port"
	def get_app_flow(self, cap, init_timestamp_dict,filename):
		timestamps = init_timestamp_dict
		res={}
		pattern = re.compile(ur"[0-9]{1,5}\\xe2\\x86\\x92[0-9]{1,5}",re.UNICODE)
		
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

				content = {"pkt_time": pkt.time, "pkt_len":pkt.length}
				if app_key in res.keys():
					res[app_key].append(content)
				else:
					res[app_key] =[content]

		print "finished hashtable collection"

		with open("cleanData_"+filename+".csv", 'w') as f:
			header = ['key','size', 'points']
			writer = csv.DictWriter(f, header)
			writer.writeheader()

			for k in res.keys():
				time_points = []
				flow_size = []
				for pkt in res[k]:
					time_points.append(str(format(float(pkt['pkt_time'])+timestamps[filename], ".6f")))
					flow_size.append(pkt['pkt_len'])
				writer.writerow({'key':k,'size':"|".join(flow_size),'points':"|".join(time_points)})
				f.flush()