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
    print(raw_scan_output)
    # Parsed access-point listing. Access-points are dictionaries.
    all_access_points = formatCells(self, raw_scan_output)
    print(all_access_points)
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
    

# rssi_scanner = rssi.RSSI_Scan('wlan0')
for i in range(0,10):
    
    rssi_scanner = rssi.RSSI_Scan('wlan0')
    print(rssi_scanner.getRawNetworkScan(True)['output'])
    rssi_scanner = rssi.RSSI_Scan('wlan0')
    print(rssi_scanner.getRawNetworkScan(True))
#     print(getAPinfo(rssi_scanner, networks='EdgeCloud1', sudo=True))