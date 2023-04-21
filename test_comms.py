from comms import Comms
import json
import time
import _thread

comms = Comms()

while True:
    #comms.send("get echo")
   
    try:
        message = comms.read()
        if message is not None:
            print(message)
    except:
        #serial state can be weird after power drops, this is a sledgehammer to prevent that from interupting startup
        pass
    time.sleep(0.1)