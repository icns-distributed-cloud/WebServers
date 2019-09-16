import rssi
import numpy as np
import time
import csv
#import matplotlib.pyplot as plt

interface = 'wlan0'
rssi_scanner = rssi.RSSI_Scan(interface)
print(rssi_scanner)
#print(type(rssi_scanner))
ssids = 'DistCloud'
n_iter= 1 #used for Kalman Filter

# python file will have to be run with sudo privileges.
# sudo argument automatixally gets set for 'false', if the 'true' is not set manually.
sudo=True

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

  
def getFilteredSignalStrength(ssids, ap_info, n_iter): #Kalman Filtering  
    # intial parameters
    sz = (n_iter,) # size of array
    Q = 1e-5 # process variance

    # allocate space for arrays
    xhat=np.zeros(sz)      # a posteri estimate of x
    P=np.zeros(sz)         # a posteri error estimate
    xhatminus=np.zeros(sz) # a priori estimate of x
    Pminus=np.zeros(sz)    # a priori error estimate
    K=np.zeros(sz)         # gain or blending factor

    R = 0.1**2 # estimate of measurement variance, change to see effect

    # intial guesses
    xhat[0] = ap_info[0]
    P[0] = 1.0

    for k in range(1,n_iter):
        # time update
        xhatminus[k] = xhat[k-1]
        Pminus[k] = P[k-1]+Q

        # measurement update
        K[k] = Pminus[k]/( Pminus[k]+R )
        xhat[k] = xhatminus[k]+K[k]*(ap_info[k]-xhatminus[k])
        P[k] = (1-K[k])*Pminus[k]
    
#    plt.figure()
#    plt.plot(ap_info,'k+',label='noisy measurements')
#    plt.plot(xhat,'b-',label='a posteri estimate')
#    plt.legend()
#    plt.title('Estimate vs. iteration step', fontweight='bold')
#    plt.xlabel('Iteration')
#    plt.ylabel('Received Signal Strength Indicator')
#    plt.show()
        
#    plt.figure()
#    plt.plot(ap_info,'k+',label='noisy measurements')
#    plt.plot(xhat,'b-',label='a posteri estimate')
#    plt.axhline(x,color='g',label='truth value')
#    plt.legend()
#    plt.title('Estimate vs. iteration step', fontweight='bold')
#    plt.xlabel('Iteration')
#    plt.ylabel('Voltage')
#
#    plt.figure()
#    valid_iter = range(1,n_iter) # Pminus not valid at step 0
#    plt.plot(valid_iter,Pminus[valid_iter],label='a priori error estimate')
#    plt.title('Estimated $\it{\mathbf{a \ priori}}$ error vs. iteration step', fontweight='bold')
#    plt.xlabel('Iteration')
#    plt.ylabel('$(Voltage)^2$')
#    plt.setp(plt.gca(),'ylim',[0,.01])
#    plt.show()
#    df = pd.DataFrame(array).T
#    df.to_excel('filterSignal.xlsx')
    fl = open('filteredm6.csv', 'w')
    print(type(xhat))

    writer = csv.writer(fl)
    for values in xhat:
        writer.writerow([values])
    fl.close()    
    return xhat

#ap_info = getAPinfo(rssi_scanner, networks=ssids, sudo=True)
#print(ap_info)



ap_info = np.zeros(n_iter)
t0=time.time()
for i in range(0,n_iter):
    ap_info[i] = getAPinfo(rssi_scanner, networks=ssids, sudo=True)[0]['signal']
    print(i, ap_info[i])
t1=time.time()
print('Running time: ', t1-t0)


fl = open('m6.csv', 'w')
writer = csv.writer(fl)
for values in ap_info:
    writer.writerow([values])
fl.close()

print('Average signal: ', sum(ap_info)/n_iter)
xhat = getFilteredSignalStrength(ssids, ap_info, n_iter)
signalStrength = sum(xhat)/n_iter
print(xhat)
print('Filtered signal: ', signalStrength)

accessPoint = {
     'signalAttenuation': 3.5, 
     'location': {
         'y': 1, 
         'x': 1
     }, 
     'reference': {
         'distance': 1, 
         'signal': -31
     }, 
     'name': ssids
}


def getDistanceFromAP(accessPoint, signalStrength):
    beta_numerator = float(accessPoint['reference']['signal']-signalStrength)
    beta_denominator = float(10*accessPoint['signalAttenuation'])
    beta = beta_numerator/beta_denominator
    distanceFromAP = round(((10**beta)*accessPoint['reference']['distance']),4)
    accessPoint.update({'distance':distanceFromAP})
    return accessPoint
distance = getDistanceFromAP(accessPoint, signalStrength)
print(distance)