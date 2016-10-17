# SDN_project

## Process raw data (Data Clean)
### ./get_stats_data.py
    (Please modify your paths to files inside of this program)
    To process raw wireshark data into pure statistic data, which can speed up process a lot, into format like:
    key ; "size1|size2|size3|...|sizen" ; "time1|time2|time3|...|timen"

where key is in "srcIP_srcPort_dstIP_dstPort" format

In this program, start_time for each wireshark packets files are extracted in timestamp format, used to add to referance time in each wireshark file to get absolute times.

### cat file1 file2 ... filen > input.csv

       Then concatenate porcessed .csv data into one input.csv file
       Take "number_of_files" as the number of files to concatenate
## Get flows (Analysis usage)
### ./final_process.py input.csv output.csv threshold number_of_files
    Take 4 args: input, output, threshold, number_of_files

    Will print out the # of unique flows & the # of flows under the specified threshold.