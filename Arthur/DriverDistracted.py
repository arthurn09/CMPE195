import datetime

datafile = open('send_Data.log', 'a')
datafile.write('Driver distracted '),
datafile.write('%s\n' % (datetime.datetime.now()))
datafile.close()