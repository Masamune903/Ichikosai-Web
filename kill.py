import os
import time
while(True):
    time.sleep(5)
    a=os.system('curl https://ichikosai.net:8443/ -m 5 -k')
    if a!=0:
        print('再起動')
        os.system('ps aux | grep schoolfestival.py | grep -v grep | awk \'{ print "sudo kill -9", $2 }\' | sh')
        b=os.system('sudo nohup python3.6 schoolfestival.py &')