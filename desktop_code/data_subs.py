import time
from azure.iot.device import IoTHubDeviceClient
import numpy as np
import warnings
import json
import pandas as pd
import numpy as np

warnings.filterwarnings("ignore", category=UserWarning)


RECEIVED_MESSAGES = 0
CONNECTION_STRING = "HostName=test-iot-1.azure-devices.net;DeviceId=pi;SharedAccessKey=dbC72EA5nNC/FwdDolbhu1omRWyz5IBhFAflcTMOx30="

def message_handler(message):
    global RECEIVED_MESSAGES
    global msg
    RECEIVED_MESSAGES += 1
    # print("")
    # print("Message received:")

    # print data from both system and application (custom) properties
    for property in vars(message).items():
        # print ("   {}".format(property))
        if property[0]=='data':
            msg = property[1].decode('ascii')

    try:
        #convert str to dict

        
        print(msg)
        with open("message.txt","w") as f:
            f.write(msg)
        
    except:
        pass       

    # print("Total calls received: {}".format(RECEIVED_MESSAGES))




def main():
    print ("Starting the Python IoT Hub C2D Messaging device sample...")

    # Instantiate the client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    # print ("Waiting for C2D messages, press Ctrl-C to exit")
    try:
        # Attach the handler to the client
        client.on_message_received = message_handler
        
        while True:
            time.sleep(1000)
    except KeyboardInterrupt:
        print("IoT Hub C2D Messaging device sample stopped")
    finally:
        # Graceful exit
        print("Shutting down IoT Hub Client")
        client.shutdown()

if __name__ == '__main__':
    main()