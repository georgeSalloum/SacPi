import sqlite3
import time
import threading
from threading import Thread
from DataCollector import DataCollector

class LocalDbHandler(threading.Thread):
    
    #sac_data (date DATE, time TIME, temperature NUMERIC, humidity NUMERIC)
    def collect_data(self):
        dataCollector = DataCollector()
        conn = sqlite3.connect('sac.db');
        cursor = conn.cursor()
        print("Connected to SAC db successfully")
    
        while(True):
            temp = dataCollector.get_temp();
            humidity = dataCollector.get_humidity();
            query = "INSERT INTO sac_data values(date('now'), time('now'), {}, {})".format(temp,humidity);
            print(query);
            cursor.execute(query);
            conn.commit();
            time.sleep(60)
        
    def run(self):
        self.collect_data()
        
