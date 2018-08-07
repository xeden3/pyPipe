# pyPipe
=====
This module makes it much easier to use named pipes. It only uses multithreading module and os module,The project provides server and client and simple.


# API
=====
       PipeServer(pipeName, pipeNumber, onCallbackFunc)
       PipeClient(pipeName, pipChannel)
              PipeClient.connect()
              PipeClient.send(data)
              PipeClient.close()
