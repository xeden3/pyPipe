# pyPipe

This module makes it much easier to use named pipes. It only uses multithreading module and os module,The project provides server and client and simple.


# API
```python
       Server PipeServer(pipeName, pipeNumber, onCallbackFunc)
       Client PipeClient(pipeName, pipChannel)
              PipeClient.connect()
              PipeClient.send(data)
              PipeClient.close()
```
# Examples

```
       #!/usr/bin/env python
       # coding:utf-8

       from Libs.PipeServer import *

       def onDataRecv(data):
           if data=="AAA":
               return "aaa"
           if data=="BBB":
               return "bbb"
           return "ccc"

       if __name__ == "__main__":
           p = PipeServer("Pipe485S0", 3, onDataRecv)
           print("initialized ...")
           while True:
               time.sleep(10)
```

```
       #!/usr/bin/env python
       #encoding: utf-8

       import json
       import base64
       import time
       from Libs.PipeClient import *

       p = PipeClient("PipeTest", 0)
       p.connect()
       start = time.time()
       for i in range(1000000):
           print(p.send("AAA"))
       end = time.time()
       print("tm:" + str((end-start)*1000))
       p.close()
```
