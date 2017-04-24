from settings import *
import sys
from paho.mqtt import client
import random
from byte_input_window import ByteInputWindow 

"""
class MqClient(client.Client):
    def __init__(self, name):
        client.Client.__init__(self, name)
"""


class BattleBitsNet(client.Client):
    def __init__(self, _id):
        client.Client.__init__(self, _id)
        #Attempt to get a network connection

        try:    
            self.connect(MQTT_GAME_SERVER, 1883, 60)
            #self.on_message = self.process_message
            self.on_connect = self._on_connect

            self.subscribe("battlebits/debug")
            self.publish("battlebits/connected","ID: #")

        except Exception as e:
            print("Error connecting to battlebits server")
            print(e.strerror)
            #sys.exit()
        #self.loop_forever()  #This will block so we do loop.start()
        self.loop_start()

    def process_message(self, client, userdata, msg):
        print("MSG: " + msg.payload)

    def _on_connect(self, client, userdata, flags, rc):
        print("Connection returned result: "+str(rc))





if __name__ == "__main__":

    #def process_message(client, userdata, msg):
        #print("MSG: " + msg.payload)

    bbn = BattleBitsNet(str(random.randint(0,99999)))
    #bbn.subscribe("battlebits/debug")
    bbn.on_message = process_message()
    #bbn.loop_forever()

