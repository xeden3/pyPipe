#!/usr/bin/env python
# coding:utf-8

import sys
import os
import time
#import multiprocessing
#from multiprocessing import Process, Manager
from Libs.termcolor import *
import threading
import ctypes
    
class PipeServerWorker(threading.Thread):
    def __init__(self, parent, pipeIdx, callbackRecv, onRecvLock):
        threading.Thread.__init__(self)
        self._pipeName = parent._pipeName
        self._pipeIdx = pipeIdx
        self._pipeClientPid =0
        self._callbackRecv = callbackRecv
        self._onRecvLock = onRecvLock
        
    def run(self):
        read_path = "/tmp/"+self._pipeName+"_" + str(self._pipeIdx) + "_in.pipe"
        write_path = "/tmp/"+self._pipeName+"_" + str(self._pipeIdx) + "_out.pipe"
        
        #获取当前进程ID addr 可能是 186, 224, 178 RasperryPi的地址是224
        self._tid = str(ctypes.CDLL('libc.so.6').syscall(224))
        
        try:
            os.remove(read_path)
        except FileNotFoundError:
            pass
        
        try:
            os.mkfifo( write_path )
        except OSError as e:
            if str(e) != "[Errno 17] File exists":
                print( e )
        fw = os.open( write_path, os.O_SYNC | os.O_CREAT | os.O_RDWR )
        
        try:
            os.mkfifo(read_path)
        except FileExistsError:
            pass
            
        fr = None
        while True:
            
            if fr==None:
                fr = os.open(read_path, os.O_RDONLY)
                
            s = os.read(fr, 1024)
            if len(s)==0:
                time.sleep(0.001)
                continue
            
            print(colored('[ i '+ self._tid +' ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] ', 'green') , 'RECV : ' + str(s, encoding='utf-8'))
            
            try:
                recv_s = str(s, encoding='utf-8')
                if len(recv_s)<6:
                    continue
                    
                act = recv_s[0:6]
                if act == '@CONT|':
                    d = recv_s[6:]
                    if self._pipeClientPid == 0 or self._pipeClientPid == int(d):
                        self._pipeClientPid = int(d)
                        os.write( fw, b'@CONT|OK|' )
                        
                if act == '@CLOS|':
                    d = recv_s[6:]
                    if self._pipeClientPid == int(d):
                        self._pipeClientPid = 0
                        os.write( fw, b'@CLOS|OK|' )
                        
                if act == '@SEND|':
                    new_s = recv_s[6:]
                    new_s = new_s.split('|',1)
                    d = new_s[0]
                    data = new_s[1]
                    if self._pipeClientPid == int(d):
                        with self._onRecvLock:
                            rtval =  self._callbackRecv(data)
                        os.write( fw, bytes('@SEND|OK|' + rtval, encoding='utf-8') )
            except ValueError as e:
                pass
                
            except IndexError as e:
                pass
                
        os.unlink(read_path)
        os.close(fr)
        os.close( fw )
        pass
    
class PipeServer:    
    def __init__(self, pipeName, pipeNumber, onDataRecv):
        #manager = Manager()
        self._pipeName = pipeName
        self._pipeNumber = pipeNumber
        self._pipServerProcess = []
        self._onDataRecv = onDataRecv
        self._onDataRecvLock  = threading.Lock()
        
        
        for i in range(self._pipeNumber):
            pw = PipeServerWorker(self,i,self._onDataRecv,self._onDataRecvLock)
            pw.setDaemon = True
            pw.start()
            self._pipServerProcess.append(pw)

