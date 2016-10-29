#!/usr/local/bin/python

from StatsGenerator import trace_handler
import os, sys
i = 0
PIECE_NUMBER = 8
TIME_THRESHOLD = 0
trace_file = 'univ2_trace/univ2_pt'

th = trace_handler(TIME_THRESHOLD)
stamps_list = th.get_timestamp_list(PIECE_NUMBER, trace_file)

while i<=PIECE_NUMBER:
	path = trace_file+str(i) 
	
	th.set_number_file(i)
	cap = th.get_trace_controller(path)
	
	th.get_app_flow(cap,stamps_list)
	i += 1
