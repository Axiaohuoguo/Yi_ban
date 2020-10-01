import time
print str(time.strftime('%Y-%m-%d',time.localtime(time.time()-86400*7)))+" 00:00"
print str(time.strftime('%Y-%m-%d',time.localtime(time.time())))+" 23:59"

