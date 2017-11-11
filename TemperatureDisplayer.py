from DataCollector import DataCollector
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory
from sense_hat import SenseHat
from threading import Thread
import keys
import threading


class TemperatureDisplayer(threading.Thread):
    
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = keys.pubnunb_subscribe_key
    pnconfig.publish_key = keys.pubnub_publish_key
    pnconfig.ssl = False
    pubnub = PubNub(pnconfig)
    sense = SenseHat()
    
    class SACListener(SubscribeCallback):
        sac_temp = 20
            
        def message(self, pubnub, message):
            channel = message.channel
            message = message.message
            if(channel == 'Temperature_Data_Load_Channel'):
                temp = message['temperature']
                humid = message['humidity']
                sac_temp = message['sac_temperature']
                TemperatureDisplayer().sense.show_message(str(sac_temp))
               
        
        def presence(self, pubnub, presence):
            pass
        
    
        def get_sac_temp(self):
            return self.sac_temp
    
    def listen(self):
        listener = self.SACListener()
        self.pubnub.add_listener(listener)
        self.pubnub.subscribe().channels('Temperature_Data_Load_Channel').execute()
        
            
    def run(self):
        self.listen()
        