#!/usr/local/bin/python
import csv
import operator
import sys
import argparse

if len(sys.argv) != 5:
	print "wrong args."
	exit(-1)
parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
parser.add_argument("threshold")
parser.add_argument("pkt_file_number")
args = parser.parse_args()

input_file_name = args.input
output_file_name = args.output
THRESHOLD = float(args.threshold)
number_of_files = int(args.pkt_file_number)
csv.field_size_limit(sys.maxsize)
reader = csv.reader(open(input_file_name), delimiter=";")

sortedlist = sorted(reader, key=operator.itemgetter(0), reverse=True)

new_sortedlist = []

sortedlist = sortedlist[number_of_files:]

# sortedlist is the sorted sub_flows across files after removed first 20 headers

for i in range(0,len(sortedlist)):
	sortedlist[i] = sortedlist[i][0].split(",")

#sortedlist:[[key,"size_list_str","tiem_list_str"],[]...]

tmp_size_list = []
tmp_time_list = []
current_key = sortedlist[0][0]
for i in range(0, len(sortedlist)):#line is a list of [key,"size_list_str","tiem_list_str"]
	if i < len(sortedlist)-1:
		if sortedlist[i][0] == current_key:
			tmp_size_list.append(sortedlist[i][1])
			tmp_time_list.append(sortedlist[i][2])
		else:
			new_sortedlist.append([current_key,"|".join(tmp_size_list),"|".join(tmp_time_list)])			
			current_key = sortedlist[i][0]
			tmp_size_list = [sortedlist[i][1]]
			tmp_time_list = [sortedlist[i][2]]
	else:
		if sortedlist[i][0] == current_key:
			tmp_size_list.append(sortedlist[i][1])
			tmp_time_list.append(sortedlist[i][2])
		else:
			current_key = sortedlist[i][0]
			tmp_size_list = [sortedlist[i][1]]
			tmp_time_list = [sortedlist[i][2]]
		new_sortedlist.append([current_key,"|".join(tmp_size_list),"|".join(tmp_time_list)])


print "# of unique_flows: ", len(new_sortedlist)
key_check = set()
for _ in new_sortedlist:
	key_check.add(_[0])
assert (len(key_check) == len(new_sortedlist))

flows_counter = 0
# extract flows from after merged new_sortedlist
with open(output_file_name, 'w') as f:
	header = ['key','init_time','duration','size']
	writer = csv.DictWriter(f, header)
	writer.writeheader()
	for _ in new_sortedlist:# process per unique flow
		key = _[0]

		size_list = [int(i) for i in _[1].split('|')]
		time_list = [float(i[3:]) for i in _[2].split('|')]
		assert len(size_list) == len(time_list)
		#associate size and init_time
		size_time_list = []
		for i in range(0,len(size_list)):
			size_time_list.append((size_list[i], time_list[i]))

		size_time_list = sorted(size_time_list, key=operator.itemgetter(1))

		flow_start_time = size_time_list[0][1]
		last_time = size_time_list[0][1]
		flow_duration = 0
		flow_size = 0
		for i in range(0, len(size_time_list)):
			size_time_tuple = size_time_list[i]
			delta_time = size_time_tuple[1] - last_time
			assert (delta_time>=0)
			if i < len(size_time_list)-1:
				if delta_time > THRESHOLD:
					writer.writerow({'key':key,'init_time':flow_start_time,'size':flow_size,'duration':flow_duration})
					f.flush()
					flows_counter += 1
					last_time = size_time_tuple[1]
					flow_start_time = size_time_tuple[1]
					flow_duration = 0
					flow_size = size_time_tuple[0]
				else:
					last_time = size_time_tuple[1]
					flow_duration = size_time_tuple[1] - flow_start_time
					flow_size += size_time_tuple[0]
			else:
				if delta_time > THRESHOLD:
					writer.writerow({'key':key,'init_time':flow_start_time,'size':flow_size,'duration':flow_duration})
					f.flush()
					flows_counter += 1
					last_time = size_time_tuple[1]
					flow_duration = 0
					flow_start_time = size_time_tuple[1]
					flow_size = size_time_tuple[0]
				else:
					flow_duration = size_time_tuple[1] - flow_start_time
					flow_size += size_time_tuple[0]
				writer.writerow({'key':key,'init_time':flow_start_time,'size':flow_size,'duration':flow_duration})
				f.flush()
				flows_counter += 1
print "# of flows on threshold %s : %s" % (THRESHOLD, flows_counter)
