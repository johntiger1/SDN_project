# SDN_project

## Task1 aggregate packets to flows
### Process raw data (Data Clean)
#### Step 1: get_stats_data.py
	Takes 1 arg: the folder or wireshark traces eg: ./cleanData.py univ1_trace
	To process raw wireshark data into pure statistic data, which can speed up process a lot, into format as in .csv files:
	key;"size1|size2|size3|...|sizen";"time1|time2|time3|...|timen"
	where key is in "srcIP_srcPort_dstIP_dstPort" format
	In this program, start_time for each wireshark packets files are extracted in timestamp format, used to add to reference time in each wireshark file to get absolute times.


#### StatsGenerator.py
	A class of function blocks provided for cleanData.py to use. 

#### Step 2: cat file1 file2 ... filen > input.csv

	“./cleanData.py” will generate as many as wireshark files fed in. 
	So, we need to concatenate processed .csv data into one input.csv file for further use. 
	The “input.csv” file is the input file for step 3 as input file of "packetsToFlows.py".

### Packets to Flows
#### Step 3: packetsToFlows.py
	Take 4 args:
	input: clean data outputted from step 2
	output: the file you want to store flows data in
	threshold: under what threshold you want to aggregate packets into a flow.
	Number_of_files: how many wireshark files are inputted.

	Will print out the # of unique flows & the # of flows under the specified threshold.

## Task 2: Group Assignment (preparation for assigning to paths)
#### bw_calc.py

	Takes 3 args: 
			input_file_name: the flow csv file you want to hash. 
		    #_of_groups: the number of groups for hashing flows;	
		    Output_file_name: the destination file for grouped flows
	
	Will assign flows by unit of ip pair to different groups for decision and further determination of assigning to paths. (Analysis Phase)


## Task 3: Intraflow Simulation (generate flows under Possion Distribution)
#### master.py
	Takes 2 more args: 
		mapping.csv: server numbers to ip addresses mapping. 
	    Flow_files: at least one flow file has to be provided, matlab data flow files for main server.

	eg: master.py mapping_serverNumber_to_ip flowDataMining1.mat flowDataMining2.mat ... (have to provide mapping file and at least one silulated flow file)
	Input: simulated flows among all servers
	Output: 16 files for each of the 16 servers for further simulation running on each server.

	Randomly assigned source ports(10000, 10199) and destination ports(11000,11199)
