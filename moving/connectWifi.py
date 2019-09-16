from wifi import Cell, Scheme
import os

wifiname = ['DistCloud']
def wifiscan(wifiname):
   allSSID = list(Cell.all('wlan0'))

   
   #print(allSSID, type(allSSID))
   #print(list(Cell.address
   #print(allSSID[0])
   myssid = [None]*len(wifiname)
   print(len(wifiname))
   for i in range(len(wifiname)):
        myssid[i] = 'Cell(ssid=' + wifiname[i] + ')'
        print(myssid[i])
        if myssid[i] in str(allSSID):
            os.system('sudo ./switchwifi ' + str(myssid[i]).replace("Cell(ssid=","").replace(")",""))
            return 1
        else:
            print("getout")
   return 0
   #for j in range(len(allSSID)):
   #     if str(allSSID[j]) in myssid:
   #         os.system('sudo ./switchwifi ' + str(allSSID[j]).replace("Cell(ssid=","").replace(")",""))
   #         return 1
            #break
   #     else:
   #         print("getout")
            #return 0
    #return 0
    
   # Creating Scheme with my SSID.
#    myssid= Scheme.for_cell('wlan0','home', myssid, 'qwer1234') # qwer1234 is the password to my wifi myssid is the wifi name 
# 
#    print(myssid, type(myssid))
#    myssid.save()
#    myssid.activate()

if wifiscan(wifiname) == 1:
    print('acd')
else:
    print('no signal')
    
os.system('sudo ./switchwifi DistCloud')
          