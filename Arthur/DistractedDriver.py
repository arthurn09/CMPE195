import datetime

datafile = open('send_data.txt', 'a')
datafile.write('Driver distracted '),
datafile.write('%s\n' % (datetime.datetime.now()))
datafile.close()