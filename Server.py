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