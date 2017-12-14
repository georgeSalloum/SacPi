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
        auto_mode = 1
            
        def message(self, pubnub, message):
            channel = message.channel
            message = message.message
            print(message)
            
            #Android
            if(channel == 'Temperature_Command_Channel_Android'):
                message = message['nameValuePairs'];
                req = message['Request']
                if(req == 'Get_Data_Load'):
                    TemperatureMonitor().publish_data(self.sac_temp,self.auto_mode,'Temperature_Data_Load_Channel')
                if(req == 'Change_Temp'):
                    new_temp = message['Temperature']
                    self.update_temperature(new_temp)
                    TemperatureMonitor().publish_data(self.sac_temp,self.auto_mode,'Temperature_Data_Load_Channel')
                if(req == 'Auto_Mode_Change'):
                    new_mode = message['Mode']
                    self.update_mode(new_mode)
                    TemperatureMonitor().publish_data(self.sac_temp,self.auto_mode,'Temperature_Data_Load_Channel')
            
            #WebApplication/js
            if(channel == 'Temperature_Command_Channel'):
                req = message['Request'] 
                if(req == 'Get_Data_Real_Time'):
                    TemperatureMonitor().publish_data(self.sac_temp,self.auto_mode,'Temperature_Real_Time_Channel')
                if(req == 'Change_Temp'):
                    new_temp = message['Temperature']
                    self.update_temperature(new_temp)
                    TemperatureMonitor().publish_data(self.sac_temp,auto_mode,'Temperature_Data_Load_Channel')
                    
             #MachineLearner
            if(channel == 'Temperature_Command_Channel_ML'):
                req = message['Request']
                if(req == 'Get_Data_ML'):
                    TemperatureMonitor().publish_data(self.sac_temp,self.auto_mode,'Temperature_Data_Channel_ML')
                if(req == 'Change_Temp'):
                    print('ml updating')
                    new_temp = message['ml_temperature']
                    if(self.auto_mode == 1):
                        self.update_temperature(new_temp)
                        TemperatureMonitor().publish_data(self.sac_temp,self.auto_mode,'Temperature_Data_Load_Channel')  
    
    
        def presence(self, pubnub, presence):
            pass
        
        def update_temperature(self,new_temp):
            self.sac_temp = new_temp
            
        def update_mode(self,new_mode):
            self.auto_mode = new_mode
                
        
    def publish_callback(self,result,status):
        pass
    
    
    def publish_data(self,sac_temp,auto_mode,channel_name):
        dataCollector = DataCollector()
        temp = dataCollector.get_temp()
        humid = dataCollector.get_humidity()
        message = {
            'temperature': temp,
            'humidity': humid,
            'sac_temperature':sac_temp,
            'auto_mode': auto_mode
            }
        if(channel_name == 'Temperature_Real_Time_Channel'):
            message = {'eon':
                        {'temperature': temp,
                        'humidity': humid,
                        'sac_temperature':sac_temp
                        }
                       }
        #print(channel_name)
        self.pubnub.publish().channel(channel_name).message(message).async(self.publish_callback)


    def listen(self):
        listener = self.SACListener()
        self.pubnub.add_listener(listener)
        self.pubnub.subscribe().channels('Temperature_Command_Channel').execute()
        self.pubnub.subscribe().channels('Temperature_Command_Channel_Android').execute()
        self.pubnub.subscribe().channels('Temperature_Command_Channel_ML').execute()

            
    def run(self):
        self.listen()
        
