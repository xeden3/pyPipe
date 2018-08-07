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