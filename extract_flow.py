#!/usr/local/bin/python

from traceHandler import trace_handler
import os, sys

trace_file = os.path.expanduser('~')+'/Downloads/univ1_trace/univ1_pt1'

th = trace_handler()

cap = th.get_trace_controller(trace_file)

th.get_app_flow(cap)