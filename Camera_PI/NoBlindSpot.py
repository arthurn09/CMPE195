import datetime

data_log_file = open('send_data.txt','a')
data_log_file.write('Driver switched lanes without checking blindspot '),
data_log_file.write('%s' % (datetime.datetime.now()))
data_log_file.close()