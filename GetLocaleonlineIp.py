#encoding:"utf8"

import os
import threading
from queue import Queue
import re
import time
import sys

res = re.compile("100% 丢失")
lock = threading.RLock()
q = Queue()

ip_prefix = "192.168.0.%s"
for i in range(1,255):
    q.put(ip_prefix  % str(i))

def SaveResult(filename, content):
    lock.acquire()
    with open(filename, "at") as f:
        f.write(str(content) + "\n")
    lock.release()

def runCMD(ip):
    cmd = "ping %s /n 2" % ip
    result = os.popen(cmd)
    content = result.read()
    if not res.findall(result.read()):
        res2 = re.compile("TTL=")
        if res2.findall(content):
            print(time.ctime(), ip)
            SaveResult(os.path.join(os.path.abspath(os.path.dirname(__file__)), "result.log"), ip)
    
while True:
    t = []
    for i in range(50):
        if not q.empty():
            tt = threading.Thread(target=runCMD,args=(q.get(),))
            t.append(tt)
            tt.start()
        else:
            time.sleep(5)
            sys.exit(0)
        

    for tt in t:
        tt.join()
        


