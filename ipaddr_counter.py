import pyshark
import os
import sys

file_path_stub = os.path.expanduser('~')+'/Downloads/univ1_trace/univ1_pt'
i = 1
set ip_set = set()
while (i<=20):
	cap = pyshark.FileCapture(file_path_stub+str(i), only_summaries=True)
	

	for pkt in cap:
		if pkt.protocol == 'TCP':
			source_ip = pkt.source
			if source_ip not in ip_set:
				ip_set.add(source_ip)
	print "univ ", i, " ip set size: ", len(ip_set)
	i += 1
