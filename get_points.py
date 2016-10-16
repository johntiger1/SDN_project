#!/usr/local/bin/python

from Points import trace_handler
import os, sys
i = 1
trace_file = os.path.expanduser('~')+'/Downloads/univ1_trace/univ1_pt'

TIME_THRESHOLD = 0.1
th = trace_handler(TIME_THRESHOLD)
stamps_list = th.get_timestamp_list()

while i<=20:
	path = trace_file+str(i) 
	
	th.set_number_file(i)
	cap = th.get_trace_controller(path)
	
	th.get_app_flow(cap,stamps_list)
	i += 1
