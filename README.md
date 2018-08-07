# pyPipe

This module makes it much easier to use named pipes. It only uses multithreading module and os module,The project provides server and client and simple.


# API
```
For Server 
       PipeServer(pipeName, pipeNumber, onCallbackFunc)
For Client
       PipeClient(pipeName, pipChannel)
       PipeClient.connect()
       PipeClient.send(data)
       PipeClient.close()
```
# Examples

### Server.py
```
#!/usr/bin/env python
# coding:utf-8

from Libs.PipeServer import *

# function for data get, must return a string
def onDataRecv(data):
    if data=="AAA":
        return "aaa"
    if data=="BBB":
        return "bbb"
    return "ccc"

if __name__ == "__main__":
    # open 3 pipes for client
    # client can choose one of them by using `PipeClient("PipeTest", n) n=0~2`
    p = PipeServer("Pipe485S0", 3, onDataRecv)
    print("initialized ...")
    while True:
        time.sleep(10)
```

### ClientA.py
```
#!/usr/bin/env python
#encoding: utf-8

import time
from Libs.PipeClient import *

p = PipeClient("PipeTest", 0)
p.connect()
start = time.time()
for i in range(1000):
    print(p.send("AAA"))
end = time.time()
print("tm:" + str((end-start)*1000))
p.close()
```



### ClientB.py
```
#!/usr/bin/env python
#encoding: utf-8

import time
from Libs.PipeClient import *

p = PipeClient("PipeTest", 1)
p.connect()
start = time.time()
for i in range(1000):
    print(p.send("BBB"))
end = time.time()
print("tm:" + str((end-start)*1000))
p.close()
```
# Screenshot
[https://raw.githubusercontent.com/xeden3/pyPipe/master/screenshot.png]
