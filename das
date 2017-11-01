[1mdiff --git a/SAC.py b/SAC.py[m
[1mindex 6745def..f804a2f 100644[m
[1m--- a/SAC.py[m
[1m+++ b/SAC.py[m
[36m@@ -26,7 +26,8 @@[m [mdef publish_data():[m
     humid = dataCollector.get_humidity()[m
     message = {[m
         'temperature': temp,[m
[31m-        'humidity': humid[m
[32m+[m[32m        'humidity': humid,[m
[32m+[m[32m        'sac_temperature':sac_temp[m
         }[m
     pubnub.publish().channel('Temperature_Status_Channel').message(message).async(publish_callback)[m
     [m
[36m@@ -37,6 +38,7 @@[m [mclass SACListener(SubscribeCallback):[m
         [m
         if(channel == 'Temperature_Command_Channel'):[m
             req = message['Request'][m
[32m+[m[32m            print(message)[m
             if(req == 'Get_Data'):[m
                 publish_data()[m
             if(req == 'Change_Temp'):[m
[36m@@ -52,4 +54,4 @@[m [mpubnub.add_listener(listener)[m
 pubnub.subscribe().channels('Temperature_Command_Channel').execute()[m
 [m
 while (True):[m
[31m-    display_temperature()[m
\ No newline at end of file[m
[32m+[m[32m    display_temperature()[m
