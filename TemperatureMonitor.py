from DataCollector import DataCollector
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory
from sense_hat import SenseHat
import keys
import threading

class TemperatureMonitor(threading.Thread):

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
            if(channel == 'Temperature_Command_Channel'):
                req = message['Request']
                print(message)
                if(req == 'Get_Data_Load'):
                    TemperatureMonitor().publish_data(self.sac_temp,'Temperature_Data_Load_Channel')
                if(req == 'Get_Data_Real_Time'):
                    TemperatureMonitor().publish_data(self.sac_temp,'Temperature_Real_Time_Channel')
                if(req == 'Get_Data_Storage'):
                    TemperatureMonitor().publish_data(self.sac_temp,'Temperature_Storage_Channel')
                if(req == 'Change_Temp'):
                    new_temp = message['Temperature']
                    self.update_temperature(new_temp)
                    TemperatureMonitor().publish_data(self.sac_temp,'Temperature_Data_Load_Channel')
    
    
        def presence(self, pubnub, presence):
            pass
        
        def update_temperature(self,new_temp):
            self.sac_temp = new_temp 
                
        
    def publish_callback(self,result,status):
        pass
    
    
    def publish_data(self,sac_temp,channel_name):
        dataCollector = DataCollector()
        temp = dataCollector.get_temp()
        humid = dataCollector.get_humidity()
        message = {
            'temperature': temp,
            'humidity': humid,
            'sac_temperature':sac_temp
            }
        if(channel_name == 'Temperature_Real_Time_Channel'):
            message = {'eon':
                        {'temperature': temp,
                        'humidity': humid,
                        'sac_temperature':sac_temp
                        }
                       }
        self.pubnub.publish().channel(channel_name).message(message).async(self.publish_callback)


    def listen(self):
        listener = self.SACListener()
        self.pubnub.add_listener(listener)
        self.pubnub.subscribe().channels('Temperature_Command_Channel').execute()

            
    def run(self):
        self.listen()
        
