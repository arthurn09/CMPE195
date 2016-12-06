#written by Arthur Nguyen
import datetime
import re
import time

blindspotstring = ""
lanechangestring = ""
with open('blindspot.log') as fp:
    for line in fp:
        if not re.search('[a-zA-Z]', line):
            blindspotstring = line
with open('lanechange.log') as fp:
    for line in fp:
        if not re.search('[a-zA-Z]', line):
            lanechangestring = line

blindspottime = datetime.datetime.strptime(blindspotstring, "%Y-%m-%d %H:%M:%S.%f")
lanechangetime = datetime.datetime.strptime(lanechangestring, "%Y-%m-%d %H:%M:%S.%f")

difference = lanechangetime - blindspottime

if difference > datetime.timedelta(seconds=3):
    data_log_file = open('send_data.txt','a')
    data_log_file.write('Driver switched lanes without checking blindspot '),
    data_log_file.write('%s' % (datetime.datetime.now()))
    data_log_file.close()



