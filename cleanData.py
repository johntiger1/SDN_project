#!/usr/local/bin/python

from StatsGenerator import trace_handler
import os, sys

if len(sys.argv) != 2:
	print "Please enter the dir of traces."
	exit(-1)

DIR = sys.argv[1]
trace_files = [filename for filename in os.listdir(DIR)]
PIECE_NUMBER = len(trace_files)
th = trace_handler()
timestamps = th.get_timestamp_dict(PIECE_NUMBER, DIR, trace_files)

for filename in trace_files:
	file = DIR+'/'+filename
	cap = th.get_trace_controller(file)	
	th.get_app_flow(cap,timestamps,filename)
