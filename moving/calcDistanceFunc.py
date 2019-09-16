import rssi
import numpy as np
#import time
import csv

def formatCells(self, raw_cell_string):
    raw_cells = raw_cell_string.decode().split('Cell') # Divide raw string into raw cells.
    raw_cells.pop(0) # Remove unneccesary "Scan Completed" message.
    if(len(raw_cells) > 0): # Continue execution, if atleast one network is detected.
        # Iterate through raw cells for parsing.
        # Array will hold all parsed cells as dictionaries.
        formatted_cells = [self.parseCell(cell) for cell in raw_cells]
            # Return array of dictionaries, containing cells.
        return formatted_cells
    else:
        print("Networks not detected.")
        return False

def getAPinfo(self, networks=False, sudo=False):
    # TODO implement error callback if error is raise in subprocess
    # Unparsed access-point listing. AccessPoints are strings.
    raw_scan_output = self.getRawNetworkScan(sudo)['output'] 
    # Parsed access-point listing. Access-points are dictionaries.
    all_access_points = formatCells(self, raw_scan_output)
    # Checks if access-points were found.
    if all_access_points:
        # Checks if specific networks were declared.
        if networks:
            # Return specific access-points found.
            return self.filterAccessPoints(all_access_points, networks)
        else:
            # Return ALL access-points found.
            return all_access_points
    else:
        # No access-points were found. 
        return False
    
def getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter):
    rssi_scanner = rssi.RSSI_Scan('wlan0')
    ap_info = np.zeros(n_iter)
    #t0=time.time()
    for i in range(0,n_iter):
        ap_info[i] = getAPinfo(rssi_scanner, networks=wifiname, sudo=True)[0]['signal']
        print(i, ap_info[i])
    #t1=time.time()
    #print('Running time: ', t1-t0)
    fl = open('m5.csv', 'w')
    writer = csv.writer(fl)
    for values in ap_info:
        writer.writerow([values])
    fl.close()
    signalStrength = sum(ap_info)/n_iter
    print('Average signal: ', signalStrength)
#     for signalAttenuation in np.arange(1.0,4.0,0.1):
    beta_numerator = float(ref_signal-signalStrength)
    beta_denominator = float(10*signalAttenuation)
    beta = beta_numerator/beta_denominator
    distanceFromAP = round(((10**beta)*ref_distance),4)
    print(signalAttenuation, distanceFromAP)
    return distanceFromAP

wifiname ='EdgeCloud1'
signalAttenuation = 3.2
ref_distance = 1
ref_signal = -35
n_iter=1
getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
#     distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
#     print(signalAttenuation, distance)

    

        
     



    
    






