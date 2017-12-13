import mysql.connector
from mysql.connector import errorcode
import sqlite3
import time
import threading
import keys
import time
import datetime

class OnlineDbHandler(threading.Thread):
    

    #connect to online db
    config = {
        'host': keys.mysql_host,
        'user': keys.mysql_user,
        'password': keys.mysql_password,
        'database': keys.mysql_db_name
        }

    def clear_local_db(self):
        #connect to local db
        conn_local = sqlite3.connect('sac.db')
        cursor_local = conn_local.cursor() #delete from local db
        query = "delete from sac_data"
        cursor_local.execute(query)
        conn_local.commit()
    
    def store_data(self):
        #connect to local db
        conn_local = sqlite3.connect('sac.db')
        cursor_local = conn_local.cursor()
        print("Connected to SAC db successfully")
        
        try:
            conn = mysql.connector.connect(**self.config)
            print('Connection Established with online server')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Wrong user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('DB does not exist')
            else:
                print(err)
        else:
            cursor_online = conn.cursor()
                
        #fetch points collected from the last hour (60 points)
        query = "SELECT * FROM sac_data LIMIT 60 OFFSET (SELECT COUNT(*) FROM sac_data)-60";
        cursor_local.execute(query)

        rows = cursor_local.fetchall()
        data_points = len(rows)

        #get min max and average for humidity and temperature
        min_temp = 100;
        max_temp = 0;
        min_humid = 100;
        max_humid = 0;
        avg_temp = 0;
        avg_humid = 0;

        for row in rows:
            temp = row[2]
            humid = row[3]
            
            avg_temp = avg_temp + temp
            avg_humid = avg_humid + humid
            
            if(temp > max_temp):
                max_temp = temp
            if(temp < min_temp):
                min_temp = temp
            if(humid > max_humid):
                max_humid = humid
            if(humid < min_humid):
                min_humid = humid
                
        avg_temp = round(avg_temp/data_points,2)
        avg_humid = round(avg_humid/data_points,2)

        #push data to online database
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT into sac_data values('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(timestamp, avg_temp, max_temp, min_temp,
                                                                         avg_humid,max_humid,min_humid)


        #clear db online
        #query_delete = "delete from sac_data"
        #cursor_online.execute(query_delete)
        
        try:
            cursor_online.execute(query)
            conn.commit()
            print("Data storred online succesfully")
            self.clear_local_db()
        except mysql.connector.Error as err:
            print(err)
          
        conn.close()
        conn_local.close()

    def run(self):
        while(True):
            time.sleep(3600)
            self.store_data()
            
            
            
            
    
    
        
    