import scipy.io
import csv
import sys
from random import randrange


if len(sys.argv) < 3:
	print "wrong inputs"
	exit(-1)

def getNumToIpMapping(filename):
	return #dict

def getFileList(fileList):
	return  fileList

# srcPort = randrange(10000,10199) # increase to 200
# desPort = randrange(11000,11199) # increase to 200
mapping = getNumToIpMapping(sys.argv[1])
files = getFileList([sys.argv[i] for i in range(2, len(sys.argv))])
try:
	fopens = [open("server%d.csv" % i, "w") for i in range(1,17)]
	header = ['start_time', 'src_ip', 'src_port', 'dest_ip', 'dest_port', 'size']
	writers = [csv.DictWriter(fopens[i],header) for i in range(16)]
	for writer in writers:
		writer.writeheader()

	for file in files:
		mat = scipy.io.loadmat(file)
		sizes = mat["JOBSIZE"]
		srcServers = None
		destServers = None
		# assign two lists in SERVERS to src and des
		for item in mat["SERVERS"]:
			srcServers = destServers
			destServers = item
		startTimes = mat["JOB_ARR_TIME"]
		
		for i in range(sizes.size):
			sz = sizes.item(i)
			srcServer = srcServers.item(i) # !! when finished mapping, only use srcIP&desIP
			srcIP = srcServer #srcIP = mapping[srcServer]
			destServer = destServers.item(i)
			destIP = destServer #desIP = mapping[desServer]
			startTime = startTimes.item(i)
			srcPort = randrange(10000,10199)
			destPort = randrange(11000,11199) 
			writer = writers[srcServer-1]
			#header = ['start_time', 'src_ip', 'src_port', 'dest_ip', 'dest_port', 'size']
			writer.writerow({'start_time':startTime,'src_ip':srcIP, 'src_port':srcPort, 'dest_ip':destIP, 'dest_port':destPort, 'size':sz})		
finally:
	for f in fopens:
		f.close()

import subprocess
for i in range(1,17):
	subprocess.call(["sort", "-o", "server"+str(i)+".csv", "-k1", "-n", "-t,", "server"+str(i)+".csv"])




