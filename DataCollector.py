import os
import time
from sense_hat import SenseHat
from time import sleep

class DataCollector:
    
    def __init__(self):
        self.data = []

    def get_cpu_temp(self):
        res = os.popen("vcgencmd measure_temp").readline()
        t = float(res.replace("temp=","").replace("'C\n",""))
        return(t)

    def get_temp(self):
        sense = SenseHat()
        sensor_temp  = round(sense.get_temperature_from_humidity(),1)
        cpu_temp = self.get_cpu_temp()
        correct_temp = sensor_temp - ((cpu_temp-sensor_temp)/1.5)
        return round(correct_temp,1)

    def get_humidity(self):
        sense = SenseHat()
        return round(sense.get_humidity(),1)
        
   

