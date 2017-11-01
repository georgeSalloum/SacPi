from DataCollector import DataCollector
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory
from sense_hat import SenseHat 


pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-b27bafae-b390-11e7-8f6d-3a18aff742a6"
pnconfig.publish_key = "pub-c-b5098184-8741-481d-918f-6e08c2116ce0"
pnconfig.ssl = False
pubnub = PubNub(pnconfig)
sac_temp = 20
sense = SenseHat()

def display_temperature():
    sense.show_message(str(sac_temp))
    
def publish_callback(result,status):
    pass
    
def publish_data():
    dataCollector = DataCollector()
    temp = dataCollector.get_temp()
    humid = dataCollector.get_humidity()
    message = {
        'temperature': temp,
        'humidity': humid,
        'sac_temperature':sac_temp
        }
    pubnub.publish().channel('Temperature_Status_Channel').message(message).async(publish_callback)
    
class SACListener(SubscribeCallback):        
    def message(self, pubnub, message):
        channel = message.channel
        message = message.message
        
        if(channel == 'Temperature_Command_Channel'):
            req = message['Request']
            print(message)
            if(req == 'Get_Data'):
                publish_data()
            if(req == 'Change_Temp'):
                global sac_temp
                sac_temp = message['Temperature']
                display_temperature()
                
    def presence(self, pubnub, presence):
            pass

listener = SACListener()
pubnub.add_listener(listener)
pubnub.subscribe().channels('Temperature_Command_Channel').execute()

while (True):
    display_temperature()
