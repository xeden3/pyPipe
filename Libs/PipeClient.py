# named pipe Client
#encoding: utf-8

import os
import time
from Libs.termcolor import *

class PipeClientException(Exception):
    def __init__(self, code, value):
        err = '[ Exception {0}] {1}'.format(code, value)
        Exception.__init__(self, err)
        self.code = code
        self.value = value
        
        
        
class PipeClient:
    def __init__(self, pipeName, pipeNumber):
        self.pid = os.getppid()
        self.cmd_connect = '@CONT|' + str(self.pid)
        self.cmd_connect_done ='@CONT|OK|'
        self.cmd_close = '@CLOS|' + str(self.pid)
        self.cmd_close_done = '@CLOS|OK|'
        self.cmd_send = '@SEND|'+ str(self.pid)+'|'
        self.cmd_send_done = '@SEND|OK|'
        
        self._pipeName = pipeName
        self._pipeNumber = pipeNumber
        self._connect_idx = -1
        self.rf = None
        
    def pipe_send(self, data, wfp, rfp):
        # Client发送请求
        timeout_count = 0
        rtval = None
        while timeout_count < 10:
            f = os.open( wfp,  os.O_SYNC | os.O_CREAT | os.O_RDWR )
            len_send = os.write( f, bytes(data, encoding='utf-8') )
            os.close( f )
            start = time.time()
            while  time.time()-start<1:
                #print('timeout_count', timeout_count)
                if self.rf == None:
                    self.rf = os.open( rfp, os.O_RDONLY | os.O_NONBLOCK)
                s = b'A'
                try:
                    s = os.read( self.rf, 1024 )
                    if len(s)<6:
                        print('return val less then len(6)')
                        continue
                    ''' CRC next time
                    if len(s) != recv_len:
                        timeout_count = timeout_count + 1
                        os.close( rf )
                        continue
                   '''
                except OSError as e:
                    pass
                else:
                    rtval = str(s, encoding='utf-8')
                    break
            
            if rtval == None:
                timeout_count = timeout_count + 1
            else:
                return rtval
            pass
        return rtval
    
    def connect(self):
        timeout_count = 0
        result = False
        while timeout_count<5:
            rtval = self.pipe_send(self.cmd_connect, 
                                    "/tmp/"+self._pipeName+"_"+str(self._pipeNumber)+"_in.pipe", 
                                    "/tmp/"+self._pipeName+"_"+str(self._pipeNumber)+"_out.pipe")
            if rtval==None:
                timeout_count+=1
                continue
            elif len(rtval)<7:
                timeout_count+=1
                continue
            elif rtval==self.cmd_connect_done:
                print(colored('[ i '+ str(self.pid) +' ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] ', 'green') , 'CONT|OK : ' + str(self._pipeNumber))
                self._connect_idx = self._pipeNumber
                result = True
                break
            else:
                timeout_count+=1
        if result == False:
            raise(PipeClientException(7, "Can not connect server " + self._pipeName))
            
            
    def close(self):
        if self._connect_idx == -1:
           return
        timeout_count = 0
        result = False
        while timeout_count<5:
            rtval = self.pipe_send(self.cmd_close, 
                                    "/tmp/"+self._pipeName+"_"+str(self._connect_idx)+"_in.pipe", 
                                    "/tmp/"+self._pipeName+"_"+str(self._connect_idx)+"_out.pipe")
            if rtval==None:
                timeout_count+=1
                continue
            elif len(rtval)<7:
                timeout_count+=1
                continue
            elif rtval==self.cmd_close_done:
                print(colored('[ i '+ str(self.pid) +' ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] ', 'green') , 'CLOS|OK : ' + str(self._connect_idx))
                result = True
                self._connect_idx = -1
                break
            else:
                timeout_count+=1
        if result == False:
            raise(PipeClientException(9, "Can not close from server " + self._pipeName))
            
            
    def send(self, buffer):
        if self._connect_idx == -1:
           raise(PipeClientException(10, "There is no connection for client pipe [" + self._pipeName +"]"))
        
        result = False
        #buffer_str = self.cmd_send + str(buffer, encoding='utf-8')
        buffer_str = self.cmd_send + buffer
        rtval = self.pipe_send(buffer_str, 
                                "/tmp/"+self._pipeName+"_"+str(self._connect_idx)+"_in.pipe", 
                                "/tmp/"+self._pipeName+"_"+str(self._connect_idx)+"_out.pipe")
        if rtval==None:
            pass
        elif len(rtval)<7:
            pass
        elif rtval[0:9]==self.cmd_send_done:
            #print(colored('[ i '+ str(self.pid) +' ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] ', 'green') , 'CLOS|OK : ' + str(self._connect_idx))
            return rtval[9:]
            result = True
        else:
            pass

        if result == False:
            #return None
            raise(PipeClientException(11, "Send data exception "))