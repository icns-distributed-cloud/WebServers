from wifi import Cell, Scheme
import os

wifiname = 'icnslab'
def wifiscan(wifiname):
   allSSID = list(Cell.all('wlan0'))
   print(allSSID, type(allSSID)) # prints all available WIFI SSIDs
   myssid= 'Cell(ssid=' + wifiname + ')' # DistCloud is my wifi name

   for i in range(len(allSSID)):
        if str(allSSID[i]) == myssid:
                os.system('sudo ./switchwifi ' + wifiname)
                break
        else:
                print("getout")

   # Creating Scheme with my SSID.
#    myssid= Scheme.for_cell('wlan0','home', myssid, 'qwer1234') # qwer1234 is the password to my wifi myssid is the wifi name 
# 
#    print(myssid, type(myssid))
#    myssid.save()
#    myssid.activate()

wifiscan(wifiname)   