import datetime

datafile = open("data.log", 'a')
datafile.write("Distracted "),
datafile.write("%s\n" % (datetime.datetime.now()))
datafile.close()