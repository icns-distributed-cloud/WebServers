from flask import Flask, render_template, request, redirect, url_for
from wifi import Cell, Scheme
import os
import requests
import json

global choose_item
global choose_position
global path_route

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Book
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Connect to Database and create database session
engine = create_engine('sqlite:///fe-collection.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# landing page that will display all the books in our database
# This function operate on the Read operation.
@app.route('/')
@app.route('/start', methods=['GET', 'POST'])
def startBooks():
    if request.method == 'POST':
        return redirect(url_for('showBooks'))
    else:
        return render_template('start.html')


@app.route('/start/movingcloud', methods=['GET', 'POST'])
def showBooks():
    if request.method == 'POST':
        # print(request.form)
        # if request.form.get('action') == 'Cancel':
        # print(request.form.get('action'))
        return render_template('start.html')
    # else:
    # print(request.form.get('action'))
    # bookToDelete = session.query(Book).filter_by(id=book_id).first()
    engine.execute("DELETE FROM book;")
    ##engine.execute("SELECT * FROM book WHERE book.title='cola'")
    ##sengine.execute("UPDATE book SET book.author WHERE book.title='cola'")
    # print("cola deleted")
    session.commit()
    '''
    class infofe(object):
        all_item = []
        all_position = []
        all_status = []

        def __init__(self, item, position, status):
            self.item = item
            self.position = position
            self.status = status
            infofe.all_item.append(item)
            infofe.all_position.append(position)
            infofe.all_status.append(status)
'''

    url = 'http://192.168.2.17:8000'
    url = url + '/booksApi'
    # print(url)
    resp = requests.get(url)
    # print(resp.status_code)
    if resp.status_code == 200:
        jsonobj = resp.json()
        y_string = json.dumps(jsonobj)
        y_store = json.loads(y_string)
        #print(jsonobj)
        for element in y_store ["books"]:
            listname = element ['title']
            listposition = element ['author']
            liststatus = element ['genre']
            # print(element['title'])
            try:
                editedBook = session.query(Book).filter_by(title=listname).first()
                editedBook.author = listposition
                editedBook.genre = liststatus
                session.add(editedBook)
                session.commit()
                # print("Update cola")
            except:
                newBook = Book(title=listname, author=listposition, genre=liststatus)
                session.add(newBook)
                session.commit()
    books = session.query(Book).all()
    return render_template("books.html", books=books)


@app.route('/start/movingcloud/new/', methods=['GET', 'POST'])
def newBook():
    if request.method == 'POST':
        newBook = Book(title=request.form ['name'], author=request.form ['author'], genre=request.form ['genre'])
        session.add(newBook)
        session.commit()
        return redirect(url_for('showBooks'))
    else:
        return render_template('newBook.html')


# This will let us Update our books and save it in our database
@app.route("/start/movingcloud/<int:book_id>/edit/", methods=['GET', 'POST'])
def editBook(book_id):
    editedBook = session.query(Book).filter_by(id=book_id).first()
    # if request.method == 'POST':
    # return redirect(url_for('showBooks'))
    current_position = '(0,5)'
    choose_item = editedBook.title
    # print(choose_item)
    # else:
    # print(session.query(Book.title).all())
    current_ip='EdgeCloud1'

    url = "http://192.168.2.6:8000/booksApi/"
    url = url + choose_item
    # print(url)
    resp = requests.get(url)
    # print(resp.status_code)
    if resp.status_code == 200:
        target_ip=current_ip
        pass
    else:
        url = "http://192.168.2.17:8000/booksApi/"
        url = url + choose_item
        resp = requests.get(url)
    jsonobj = resp.json()
    tagetpoisition=jsonobj ['books'] ['author']
    # return "information is " + jsonobj ['books'] ['author']
    print('vi tri can den la',tagetpoisition)

    url = 'http://192.168.2.17:8000'
    url = url + '/booksApi'
    # print(url)
    resp = requests.get(url)
    # print(resp.status_code)
    listwifi = []
    listwifipo = []
    listwifiip=[]
    a = 0
    if resp.status_code == 200:
        jsonobj = resp.json()
        y_string = json.dumps(jsonobj)
        y_store = json.loads(y_string)
        # print(jsonobj)
        for element in y_store ["books"]:
            listname = element ['title']
            listposition = element ['author']
            liststatus = element ['genre']
            # print(listname)
            if ':8000' in listname:
                pass
            else:
                if 'EdgeCloud' in listname:
                    listwifi.insert(a,listname)
                    listwifipo.insert(a,listposition)
                    listwifiip.insert(a,liststatus)
                    if listposition==tagetpoisition:
                        target_ip=listname
                    a=a+1
    print('Ip cuoi', target_ip)
    print(listwifi)
    print(listwifipo)
    print(listwifiip)
    
    from collections import deque, namedtuple

    # we'll use infinity as a default distance to nodes.
    inf = float('inf')
    Edge = namedtuple('Edge', 'start, end, cost')

    def make_edge(start, end, cost=1):
        return Edge(start, end, cost)

    class Graph:
        def __init__(self, edges):
            # let's check that the data is right
            wrong_edges = [i for i in edges if len(i) not in [2, 3]]
            if wrong_edges:
                raise ValueError('Wrong edges data: {}'.format(wrong_edges))

            self.edges = [make_edge(*edge) for edge in edges]

        @property
        def vertices(self):
            return set(
                sum(
                    ([edge.start, edge.end] for edge in self.edges), []
                )
            )

        def get_node_pairs(self, n1, n2, both_ends=True):
            if both_ends:
                node_pairs = [[n1, n2], [n2, n1]]
            else:
                node_pairs = [[n1, n2]]
            return node_pairs

        def remove_edge(self, n1, n2, both_ends=True):
            node_pairs = self.get_node_pairs(n1, n2, both_ends)
            edges = self.edges [:]
            for edge in edges:
                if [edge.start, edge.end] in node_pairs:
                    self.edges.remove(edge)

        def add_edge(self, n1, n2, cost=1, both_ends=True):
            node_pairs = self.get_node_pairs(n1, n2, both_ends)
            for edge in self.edges:
                if [edge.start, edge.end] in node_pairs:
                    return ValueError('Edge {} {} already exists'.format(n1, n2))

            self.edges.append(Edge(start=n1, end=n2, cost=cost))
            if both_ends:
                self.edges.append(Edge(start=n2, end=n1, cost=cost))

        @property
        def neighbours(self):
            neighbours = {vertex: set() for vertex in self.vertices}
            for edge in self.edges:
                neighbours [edge.start].add((edge.end, edge.cost))

            return neighbours

        def dijkstra(self, source, dest):
            assert source in self.vertices, 'Such source node doesn\'t exist'
            distances = {vertex: inf for vertex in self.vertices}
            previous_vertices = {
                vertex: None for vertex in self.vertices
            }
            distances [source] = 0
            vertices = self.vertices.copy()

            while vertices:
                current_vertex = min(
                    vertices, key=lambda vertex: distances [vertex])
                vertices.remove(current_vertex)
                if distances [current_vertex] == inf:
                    break
                for neighbour, cost in self.neighbours [current_vertex]:
                    alternative_route = distances [current_vertex] + cost
                    if alternative_route < distances [neighbour]:
                        distances [neighbour] = alternative_route
                        previous_vertices [neighbour] = current_vertex

            path, current_vertex = deque(), dest
            while previous_vertices [current_vertex] is not None:
                path.appendleft(current_vertex)
                current_vertex = previous_vertices [current_vertex]
            if path:
                path.appendleft(current_vertex)
            return path

    '''
    find position of Wifi position
    find path  
    '''
    import math
    graphlist=[]
    ag=0
    if len(listwifi)>2:
        for aj in range (0,len(listwifi)):
            #print(listwifi[aj])
            x1=int(listwifipo[aj].split(",")[0])
            y1 = int(listwifipo[aj].split(",")[1])
            #print(int(x1))
            #print(int(y1))
            for bj in range (0,len(listwifi)):
                if aj!=bj:
                    x2 = int(listwifipo [bj].split(",") [0])
                    y2 = int(listwifipo [bj].split(",") [1])
                    #print(x1,",",y1)
                    #print(x2,",",y2)
                    distance=math.sqrt(math.pow((x1-x2),2)+math.pow((y1-y2),2))
                    #print("%s,%s,%d" % (listwifi [aj], listwifi [bj], distance))
                    #print('distance is', distance)
                    if distance<30:
                        #print(listwifi[bj])
                        #print(distance)
                        if ('%s' %listwifi [aj],'%s' %listwifi [aj], int(distance)) in graphlist:
                            pass
                        else:
                            #print("%s,%s,%d" %(listwifi[aj],listwifi[bj],distance))
                            graphlist.insert(ag,('%s' %listwifi [aj],'%s' %listwifi [bj], int(distance)))
                            ag=ag+1

    #print(graphlist)
    #graphlist=['117.113.128.32,117.113.128.30,34', '117.113.128.23,117.113.128.30,50']
    graph = Graph(graphlist)
    #print(graph)
    if current_ip != target_ip:
        #print(graph.dijkstra(current_ip, target_ip))
        Route_ip = graph.dijkstra(current_ip, target_ip)
        #print(Route_ip)
        aj=0
        Route_po=[]
        Route_ac=[]
        for ai in range(0,len(Route_ip)):
            #print(Route_ip[ai])
            for bj in range(0,len(listwifi)):
                if Route_ip[ai]==listwifi[bj]:
                    Route_po.insert(aj,listwifipo[bj])
                    Route_ac.insert(aj,listwifiip[bj])
                    aj=aj+1
        #print(Route_po)
    else:
        print('Local processing')
        Route_po=['5,5']
        Route_ip=['EdgeCloud1']
        Route_ac=['192.168.2.6:8000']
    
    print('Chosen item %s is being taken' %choose_item)
    print('From:           ',current_position)
    print('To:             ',tagetpoisition)
    print('Route IP:       ',Route_ip)
    print('Route position: ', Route_po)
    print('Route webserver:', Route_ac)
    
    def decision(arg1, arg2):  
        if arg1 + 1 < arg2:
            d=arg2-arg1
            deci=0
            # turn right
        else:
            if arg1 > arg2 +1:
                d = arg1-arg2
                deci=1
                # turn left                    
            else:
                deci=2
        return d,deci
    ##
    
    def runcart(dist):
        ser.write('w'.encode()) 
        time.sleep(1)
        ser.write('o'.encode())
        time.sleep(1)
        distance=dist
        if distance==20:
            distance=distance+5
        inc=int(distance/4)
        du=distance-inc*4        
        print(inc)
        for i in range(0,inc):
            ser.write('z'.encode())
            time.sleep(1)
        time_run=(distance+inc+1)
        print(time_run)
        time.sleep(time_run)
        for i in range(0,inc):
            ser.write('x'.encode())
            time.sleep(1)
        if inc>=3:
            time.sleep(4*(inc-3))
        else:
            time.sleep(4*inc)    
        if inc>=2:
            time.sleep(2)    
        ser.write('o'.encode())
        time.sleep(du*4)
        ser.write('s'.encode()) 
    
    
    #def checkposition(arg1, arg2)
    import time
    #import numpy as np
    import serial

    ser = serial.Serial(
        "/dev/ttyAMA0",
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        writeTimeout=1,
        timeout=10,
        rtscts=False,
        dsrdtr=False,
        xonxoff=False)
          
    #print(decision(5,10))
    def wifiscan(wifiname):
       allSSID = list(Cell.all('wlan0'))
       #return 0
       #print(allSSID, type(allSSID))
       #print(list(Cell.address
       #print(allSSID[0])
       #myssid = [None]*len(wifiname)
       for i in range(len(wifiname)):
            myssid = 'Cell(ssid=' + wifiname + ')'
            #print(myssid[i])
            if myssid in str(allSSID):
                os.system('sudo ./switchwifi ' + str(myssid).replace("Cell(ssid=","").replace(")",""))
                return 1
            else:
                print("getout")
       return 0
    
    import rssi
    import numpy as np
    #import time
    #import csv

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
    #     fl = open('m1.csv', 'w')
    #     writer = csv.writer(fl)
    #     for values in ap_info:
    #         writer.writerow([values])
    #     fl.close()
        signalStrength = sum(ap_info)/n_iter
        print('Average signal: ', signalStrength)
        beta_numerator = float(ref_signal-signalStrength)
        beta_denominator = float(10*signalAttenuation)
        beta = beta_numerator/beta_denominator
        distanceFromAP = round(((10**beta)*ref_distance),4)
        return distanceFromAP

    wifiname ='EdgeCloud1'
    signalAttenuation = 3.2
    ref_distance = 1
    ref_signal = -35
    n_iter=1
    
    print(len(Route_ip))
    for i in range(0,len(Route_ip)):
        print(i, ' name:', Route_ip[i])
    
    print(len(Route_po))
    for i in range(0,len(Route_po)):
        print(i, ' position:', Route_po[i])
        
    print(len(Route_ac))
    for i in range(0,len(Route_ac)):
        print(i, ' webaddress:', Route_ac[i])
    
    x0=0
    y0=5
    x=[]
    y=[]
    i=0
    for aj in range(0, len(Route_po)):
        # print(listwifi[aj])
        x.insert(i,int(Route_po [aj].split(",") [0]))
        y.insert(i, int(Route_po[aj].split(",") [1]))
        i=i+1
    print(x)
    print(y)
    
        #
    a=decision(x0,x[0])
        #b=decision(y0,y[i])
        #print(x[i],type(x[i]))
    
    if x0 < x[0]:
        print('Self-driving cart will move ...')
        #ser.write('w'.encode())        
        time_run=x[0]-x0-1
        runcart(time_run)
        #time.sleep(time_run*4)
        #ser.write('s'.encode()) 
        print('Self-driving cart have moved with ', time_run*4, ' seconds')
            
            ## check distance
        wifiname=Route_ip[0]
        print(wifiname)
        distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
        print(distance)
            
            #correct distance
        cod=distance-1.5
        if cod > 0.5:
            ser.write('w'.encode())        
            time_run=cod
            time.sleep(time_run*4)
            ser.write('s'.encode())
     
    #check x_axis
    for i in range(0,len(x)):        
            ## check distance
        print(i)
        ind=i+1
        if i==len(x)-1:            
            wifiname=Route_ip[i]
            print(wifiname)
            while wifiscan(wifiname) != 1:
                u=1
            if wifiscan(wifiname) == 1:
                print('connected ',wifiname)
            else:
                print('no signal')
            xt0=0
            yt0=0
            text=Route_ac[i]            
            print(text)
            url = "http://%s/booksApi/" %text
            url = url + choose_item
            print(url)
            resp = requests.get(url)
                # print(resp.status_code)
            if resp.status_code == 200:                
                jsonobj = resp.json()
                tagetpoisition=jsonobj ['books'] ['author']
                # return "information is " + jsonobj ['books'] ['author']
            print('vi tri can den la',tagetpoisition)
            target_x=int(tagetpoisition.split(",") [0])
            target_y=int(tagetpoisition.split(",") [1])
        else:            
            xt0=x[i]
            yt0=y[i]                
            target_x=x[i+1]
            target_y=y[i+1]
            
        print('target go', target_x, ' , ',target_y)
        print('so sanh lan 1 ',i, ': ', xt0,' , ',yt0, ' voi so ', x0, ' , ', y0)
        
        if x[i] > x0:
            if target_y < 0 and target_y != y[i]:
                    #turn right
                print('TRUONG HOP 1: Self-driving cart will turn right ...')
                ser.write('w'.encode())
                time.sleep(1)
                ser.write('r'.encode())
                time.sleep(7)
                ser.write('o'.encode())                    
                dis=yt0-target_y
                runcart(dis)
                #time.sleep(dis*4)
                #ser.write('s'.encode())
                
                if i==len(x)-1:
                    pass
                else:
                    wifiname=Route_ip[ind]               
                    print(wifiname)
                    distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                    print(distance)
                        
                        #correct distance
                    cod=distance-1.5
                    if cod > 0.5:
                        ser.write('w'.encode())        
                        time_run=cod
                        time.sleep(time_run*4)
                        ser.write('s'.encode())
                        
            else:
                if target_y > 0 and target_y != y[i]:
                        #turn left
                    print('TRUONG HOP 2: Self-driving cart will turn left ...')
                    ser.write('w'.encode())
                    time.sleep(1)
                    ser.write('l'.encode())
                    time.sleep(7)
                    ser.write('o'.encode())                        
                    dis=target_y-yt0
                    #time.sleep(dis*4)
                    runcart(dis)
                    #ser.write('s'.encode())
                    
                    if i==len(x)-1:
                        pass
                    else:
                        wifiname=Route_ip[ind]                
                        print(wifiname)
                        distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                        print(distance)
                            
                            #correct distance
                        cod=distance-1.5
                        if cod > 0.5:
                            ser.write('w'.encode())        
                            time_run=cod
                            time.sleep(time_run*4)
                            ser.write('s'.encode())
                else:
                    if target_x > xt0 and target_y == y[i]:
                        print('TRUONG HOP 3: Self-driving cart will go straight ...')
                        #ser.write('w'.encode())        
                        time_run=target_x - xt0
                        runcart(time_run)
                        #time.sleep(time_run*4)
                        #ser.write('s'.encode())
                        
                        if i==len(x)-1:
                            pass
                        else:
                            wifiname=Route_ip[ind]                
                            print(wifiname)
                            distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                            print(distance)
                                
                                #correct distance
                            cod=distance-1.5
                            if cod > 0.5:
                                ser.write('w'.encode())        
                                time_run=cod
                                time.sleep(time_run*4)
                                ser.write('s'.encode())
        if x[i] < x0:
            print('xi= ', x[i])
            print('x0= ' ,x0)
            print('target y = ',target_y)
            if target_y < 0 and target_y != y[i]:
                    #turn right
                print('TRUONG HOP 4: Self-driving cart will turn left ...')
                ser.write('w'.encode())
                time.sleep(1)
                ser.write('l'.encode())
                time.sleep(7)
                ser.write('o'.encode())                    
                dis=yt0-target_y
                runcart(dis)
                #time.sleep(dis*4)
                #ser.write('s'.encode())                
                
                if i==len(x)-1:
                    pass
                else:
                    wifiname=Route_ip[ind]                
                    print(wifiname)
                    distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                    print(distance)
                                
                                #correct distance
                    cod=distance-1.5
                    if cod > 0.5:
                        ser.write('w'.encode())        
                        time_run=cod
                        time.sleep(time_run*4)
                        ser.write('s'.encode())
            else:
                if target_y > 0 and target_y != y[i]:
                        #turn left
                    print('TRUONG HOP 5: Self-driving cart will turn right ...')
                    ser.write('w'.encode())
                    time.sleep(1)
                    ser.write('r'.encode())
                    time.sleep(7)
                    ser.write('o'.encode())
                    time_run=int(a[0])
                    dis=target_y-yt0
                    runcart(dis)
                    #time.sleep(dis*4)
                    #ser.write('s'.encode())
                    
                    if i==len(x)-1:
                        pass
                    else:
                        wifiname=Route_ip[ind]                
                        print(wifiname)
                        distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                        print(distance)
                                
                                #correct distance
                        cod=distance-1.5
                        if cod > 0.5:
                            ser.write('w'.encode())        
                            time_run=cod
                            time.sleep(time_run*4)
                            ser.write('s'.encode())
                else:
                    if target_x < xt0 and target_y == y[i]:
                        print('TRUONG HOP 6: Self-driving cart will go straight ...')
                        #ser.write('w'.encode())        
                        time_run=xt0-target_x
                        runcart(time_run)
                        #time.sleep(time_run*4)
                        #ser.write('s'.encode())
                        
                        if i==len(x)-1:
                            pass
                        else:
                            wifiname=Route_ip[ind]                
                            print(wifiname)
                            distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                            print(distance)
                                
                                #correct distance
                            cod=distance-1.5
                            if cod > 0.5:
                                ser.write('w'.encode())        
                                time_run=cod
                                time.sleep(time_run*4)
                                ser.write('s'.encode())
        if y[i] > y0:
            if target_x > 0 and target_x != x[i]:
                    #turn right
                print('TRUONG HOP 7: Self-driving cart will turn right ...')
                ser.write('w'.encode())
                time.sleep(1)
                ser.write('r'.encode())
                time.sleep(7)
                ser.write('o'.encode())                    
                dis=target_x-xt0
                runcart(dis)
                #time.sleep(dis*4)
                #ser.write('s'.encode())
                
                if i==len(x)-1:
                    pass
                else:
                    wifiname=Route_ip[ind]                
                    print(wifiname)
                    distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                    print(distance)
                                
                                #correct distance
                    cod=distance-1.5
                    if cod > 0.5:
                        ser.write('w'.encode())        
                        time_run=cod
                        time.sleep(time_run*4)
                        ser.write('s'.encode())
            else:
                if target_x < 0 and target_x != x[i]:
                        #turn left
                    print('TRUONG HOP 8: Self-driving cart will turn left ...')
                    ser.write('w'.encode())
                    time.sleep(1)
                    ser.write('l'.encode())
                    time.sleep(7)
                    ser.write('o'.encode())                        
                    dis=xt0-target_x
                    runcart(dis)
                    #time.sleep(dis*4)
                    #ser.write('s'.encode())
                    
                    if i==len(x)-1:
                        pass
                    else:
                        wifiname=Route_ip[ind]                
                        print(wifiname)
                        distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                        print(distance)
                                
                                #correct distance
                        cod=distance-1.5
                        if cod > 0.5:
                            ser.write('w'.encode())        
                            time_run=cod
                            time.sleep(time_run*4)
                            ser.write('s'.encode())
                else:
                    if target_y > yt0 and target_x == x[i]: 
                        print('TRUONG HOP 9: Self-driving cart will go straight ...')
                        #ser.write('w'.encode())
                        #print(i)
                        #print(target_y)
                        #print(yt0)
                        #print(y[1])
                        time_run=target_y - yt0+ 2
                        print(time_run)
                        runcart(time_run)
                        #time_run=25
                        #time.sleep(time_run*4)
                        #ser.write('s'.encode())
                        print('thoi gian la: ', time_run)
                        
                        if i==len(x)-1:
                            pass
                        else:
                            wifiname=Route_ip[ind]                
                            print(wifiname)
                            distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                            print(distance)
                                
                                #correct distance
                            cod=distance-1.5
                            if cod > 0.5:
                                ser.write('w'.encode())        
                                time_run=cod
                                time.sleep(time_run*4)
                                ser.write('s'.encode())
        if y[i] < y0:
            if target_x > 0 and target_x != x[i]:
                    #turn right
                print('TRUONG HOP 10: Self-driving cart will turn left ...')
                ser.write('w'.encode())
                time.sleep(1)
                ser.write('l'.encode())
                time.sleep(7)
                ser.write('o'.encode())                    
                dis=target_x-xt0
                runcart(dis)
                #time.sleep(dis*4)
                #ser.write('s'.encode())
                
                if i==len(x)-1:
                    pass
                else:
                    wifiname=Route_ip[ind]                
                    print(wifiname)
                    distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                    print(distance)
                                
                                #correct distance
                    cod=distance-1.5
                    if cod > 0.5:
                        ser.write('w'.encode())        
                        time_run=cod
                        time.sleep(time_run*4)
                        ser.write('s'.encode())
            else:
                if target_x < 0 and target_x != x[i]:
                        #turn left
                    print('TRUONG HOP 11: Self-driving cart will turn right ...')
                    ser.write('w'.encode())
                    time.sleep(1)
                    ser.write('r'.encode())
                    time.sleep(7)
                    ser.write('o'.encode())
                    time_run=int(a[0])
                    dis=xt0-target_x
                    runcart(dis)
                    #time.sleep(dis*4)
                    #ser.write('s'.encode())
                    
                    if i==len(x)-1:
                        pass
                    else:
                        wifiname=Route_ip[ind]                
                        print(wifiname)
                        distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                        print(distance)
                                
                                #correct distance
                        cod=distance-1.5
                        if cod > 0.5:
                            ser.write('w'.encode())        
                            time_run=cod
                            time.sleep(time_run*4)
                            ser.write('s'.encode())
                else:
                    if target_y < yt0 and target_x == x[i]:
                        print('TRUONG HOP 12: Self-driving cart will go straight ...')
                        #ser.write('w'.encode())        
                        time_run=yt0-target_x
                        runcart(time_run)
                        #time.sleep(time_run*4)
                        #ser.write('s'.encode())
                        
                        if i==len(x)-1:
                            pass
                        else:
                            wifiname=Route_ip[ind]                
                            print(wifiname)
                            distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                            print(distance)
                                
                                #correct distance
                            cod=distance-1.5
                            if cod > 0.5:
                                ser.write('w'.encode())        
                                time_run=cod
                                time.sleep(time_run*4)
                                ser.write('s'.encode())
        x0=x[i]
        y0=y[i]
        print(x0)
        print(y0)
    
    time.sleep(10)
    x0=target_x
    y0=53
    print(x0) 
    a=[]
    b=[]
    c=[]
    for i in range(0,len(x)):
        #d=len(x)-i-1
        a.insert(i,x[len(x)-1-i])
        b.insert(i,y[len(x)-1-i])
        c.insert(i,Route_ip[len(x)-1-i])
    print(a)
    print(b)
    print(c)
    
    x=[]
    y=[]
    Route_ip=[]
    for i in range(0,len(a)):
        #d=len(x)-i-1
        x.insert(i,a[i])
        y.insert(i,b[i])
        Route_ip.insert(i,c[i])
    print(x)
    print(y)
    print(Route_ip)
    #adao x y va Route_ip
    #a=''
           
    print('Self-driving cart will move ...')
    #ser.write('w'.encode())        
    time_run=-x0-1
    runcart(time_run)
    #time.sleep(time_run*4)
    #ser.write('s'.encode()) 
    print('Self-driving cart have moved with ', time_run*4, ' seconds')
            
            ## check distance
    wifiname=Route_ip[0]
    print(wifiname)
    distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
    print(distance)
            #correct distance
    cod=distance-1.5
    if cod > 0.5:
        ser.write('w'.encode())        
        time_run=cod
        time.sleep(time_run*4)
        ser.write('s'.encode())
    for i in range(0,len(x)):        
            ## check distance
        print(i)
        ind=i+1
        if i==len(x)-1:            
            wifiname=Route_ip[i]
            print(wifiname)
            while wifiscan(wifiname) != 1:
                u=1
            if wifiscan(wifiname) == 1:
                print('connected ',wifiname)
            else:
                print('no signal')
            xt0=0
            yt0=0            
            target_x=0
            target_y= 0
        else:            
            xt0=x[i]
            yt0=y[i]                
            target_x=x[i+1]
            target_y=y[i+1]
            
        print('target go', target_x, ' , ',target_y)
        print('so sanh lan 1 ',i, ': ', xt0,' , ',yt0, ' voi so ', x0, ' , ', y0)
        
        if x[i] > x0:
            if target_y < y[i] and target_y != y[i]:
                    #turn right
                print('TRUONG HOP 1: Self-driving cart will turn right ...')
                ser.write('w'.encode())
                time.sleep(1)
                ser.write('r'.encode())
                time.sleep(7)
                ser.write('o'.encode())                    
                dis=yt0-target_y
                runcart(dis)
                #time.sleep(dis*4)
                #ser.write('s'.encode())
                
                if i==len(x)-1:
                    pass
                else:
                    wifiname=Route_ip[ind]               
                    print(wifiname)
                    distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                    print(distance)
                        
                        #correct distance
                    cod=distance-1.5
                    if cod > 0.5:
                        ser.write('w'.encode())        
                        time_run=cod
                        time.sleep(time_run*4)
                        ser.write('s'.encode())
                        
            else:
                if target_y > y[i] and target_y != y[i]:
                        #turn left
                    print('TRUONG HOP 2: Self-driving cart will turn left ...')
                    ser.write('w'.encode())
                    time.sleep(1)
                    ser.write('l'.encode())
                    time.sleep(7)
                    ser.write('o'.encode())                        
                    dis=target_y-yt0
                    runcart(dis)
                    #time.sleep(dis*4)
                    #ser.write('s'.encode())
                    
                    if i==len(x)-1:
                        pass
                    else:
                        wifiname=Route_ip[ind]                
                        print(wifiname)
                        distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                        print(distance)
                            
                            #correct distance
                        cod=distance-1.5
                        if cod > 0.5:
                            ser.write('w'.encode())        
                            time_run=cod
                            time.sleep(time_run*4)
                            ser.write('s'.encode())
                else:
                    if target_x > xt0 and target_y == y[i]:
                        print('TRUONG HOP 3: Self-driving cart will go straight ...')
                        #ser.write('w'.encode())        
                        time_run=target_x - xt0
                        runcart(time_run)
                        #time.sleep(time_run*4)
                        #ser.write('s'.encode())
                        
                        if i==len(x)-1:
                            pass
                        else:
                            wifiname=Route_ip[ind]                
                            print(wifiname)
                            distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                            print(distance)
                                
                                #correct distance
                            cod=distance-1.5
                            if cod > 0.5:
                                ser.write('w'.encode())        
                                time_run=cod
                                time.sleep(time_run*4)
                                ser.write('s'.encode())
        if x[i] < x0:
            print('xi= ', x[i])
            print('x0= ' ,x0)
            print('target y = ',target_y)
            if target_y < 0 and target_y != y[i]:
                    #turn right
                print('TRUONG HOP 4: Self-driving cart will turn left ...')
                ser.write('w'.encode())
                time.sleep(1)
                ser.write('l'.encode())
                time.sleep(7)
                ser.write('o'.encode())                    
                dis=yt0-target_y
                runcart(dis)
                #time.sleep(dis*4)
                #ser.write('s'.encode())                
                
                if i==len(x)-1:
                    pass
                else:
                    wifiname=Route_ip[ind]                
                    print(wifiname)
                    distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                    print(distance)
                                
                                #correct distance
                    cod=distance-1.5
                    if cod > 0.5:
                        ser.write('w'.encode())        
                        time_run=cod
                        time.sleep(time_run*4)
                        ser.write('s'.encode())
            else:
                if target_y > 0 and target_y != y[i]:
                        #turn left
                    print('TRUONG HOP 5: Self-driving cart will turn right ...')
                    ser.write('w'.encode())
                    time.sleep(1)
                    ser.write('r'.encode())
                    time.sleep(7)
                    ser.write('o'.encode())
                    time_run=int(a[0])
                    dis=target_y-yt0
                    runcart(dis)
                    #time.sleep(dis*4)
                    #ser.write('s'.encode())
                    
                    if i==len(x)-1:
                        pass
                    else:
                        wifiname=Route_ip[ind]                
                        print(wifiname)
                        distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                        print(distance)
                                
                                #correct distance
                        cod=distance-1.5
                        if cod > 0.5:
                            ser.write('w'.encode())        
                            time_run=cod
                            time.sleep(time_run*4)
                            ser.write('s'.encode())
                else:
                    if target_x < xt0 and target_y == y[i]:
                        print('TRUONG HOP 6: Self-driving cart will go straight ...')
                        #ser.write('w'.encode())        
                        time_run=xt0-target_x
                        runcart(time_run)
                        #time.sleep(time_run*4)
                        #ser.write('s'.encode())
                        
                        if i==len(x)-1:
                            pass
                        else:
                            wifiname=Route_ip[ind]                
                            print(wifiname)
                            distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                            print(distance)
                                
                                #correct distance
                            cod=distance-1.5
                            if cod > 0.5:
                                ser.write('w'.encode())        
                                time_run=cod
                                time.sleep(time_run*4)
                                ser.write('s'.encode())
        if y[i] > y0:
            if target_x > 0 and target_x != x[i]:
                    #turn right
                print('TRUONG HOP 7: Self-driving cart will turn right ...')
                ser.write('w'.encode())
                time.sleep(1)
                ser.write('r'.encode())
                time.sleep(7)
                ser.write('o'.encode())                    
                dis=target_x-xt0
                runcart(dis)
                #time.sleep(dis*4)
                #ser.write('s'.encode())
                
                if i==len(x)-1:
                    pass
                else:
                    wifiname=Route_ip[ind]                
                    print(wifiname)
                    distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                    print(distance)
                                
                                #correct distance
                    cod=distance-1.5
                    if cod > 0.5:
                        ser.write('w'.encode())        
                        time_run=cod
                        time.sleep(time_run*4)
                        ser.write('s'.encode())
            else:
                if target_x < 0 and target_x != x[i]:
                        #turn left
                    print('TRUONG HOP 8: Self-driving cart will turn left ...')
                    ser.write('w'.encode())
                    time.sleep(1)
                    ser.write('l'.encode())
                    time.sleep(7)
                    ser.write('o'.encode())                        
                    dis=xt0-target_x
                    runcart(dis)
                    #time.sleep(dis*4)
                    #ser.write('s'.encode())
                    
                    if i==len(x)-1:
                        pass
                    else:
                        wifiname=Route_ip[ind]                
                        print(wifiname)
                        distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                        print(distance)
                                
                                #correct distance
                        cod=distance-1.5
                        if cod > 0.5:
                            ser.write('w'.encode())        
                            time_run=cod
                            time.sleep(time_run*4)
                            ser.write('s'.encode())
                else:
                    if target_y > yt0 and target_x == x[i]: 
                        print('TRUONG HOP 9: Self-driving cart will go straight ...')
                        #ser.write('w'.encode())
                        #print(i)
                        #print(target_y)
                        #print(yt0)
                        #print(y[1])
                        time_run=target_y - yt0 - 1
                        runcart(time_run)
                        print(time_run)
                        #time_run=25
                        #time.sleep(time_run*4)
                        #ser.write('s'.encode())
                        print('thoi gian la: ', time_run*4)
                        
                        if i==len(x)-1:
                            pass
                        else:
                            wifiname=Route_ip[ind]                
                            print(wifiname)
                            distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                            print(distance)
                                
                                #correct distance
                            cod=distance-1.5
                            if cod > 0.5:
                                ser.write('w'.encode())        
                                time_run=cod
                                time.sleep(time_run*4)
                                ser.write('s'.encode())
        if y[i] < y0:
            if target_x > x[i] and target_x != x[i]:
                    #turn right
                print('TRUONG HOP 10: Self-driving cart will turn left ...')
                ser.write('w'.encode())
                time.sleep(1)
                ser.write('l'.encode())
                time.sleep(7)
                ser.write('o'.encode())                    
                dis=target_x-xt0
                runcart(dis)
                #time.sleep(dis*4)
                #ser.write('s'.encode())
                
                if i==len(x)-1:
                    pass
                else:
                    wifiname=Route_ip[ind]                
                    print(wifiname)
                    distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                    print(distance)
                                
                                #correct distance
                    cod=distance-1.5
                    if cod > 0.5:
                        ser.write('w'.encode())        
                        time_run=cod
                        time.sleep(time_run*4)
                        ser.write('s'.encode())
            else:
                if target_x < x[i] and target_x != x[i]:
                        #turn left
                    print('TRUONG HOP 11: Self-driving cart will turn right ...')
                    ser.write('w'.encode())
                    time.sleep(1)
                    ser.write('r'.encode())
                    time.sleep(7)
                    ser.write('o'.encode())
                    time_run=int(a[0])
                    dis=x[i]-target_x
                    runcart(dis)
                    #time.sleep(dis*4)
                    #ser.write('s'.encode())
                    
                    if i==len(x)-1:
                        pass
                    else:
                        wifiname=Route_ip[ind]                
                        print(wifiname)
                        distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                        print(distance)
                                
                                #correct distance
                        cod=distance-1.5
                        if cod > 0.5:
                            ser.write('w'.encode())        
                            time_run=cod
                            time.sleep(time_run*4)
                            ser.write('s'.encode())
                else:
                    if target_y < yt0 and target_x == x[i]:
                        print('TRUONG HOP 12: Self-driving cart will go straight ...')
                        #ser.write('w'.encode())        
                        time_run=yt0-target_x+7
                        runcart(time_run)
                        #time.sleep(time_run*4)
                        #ser.write('s'.encode())
                        
                        if i==len(x)-1:
                            pass
                        else:
                            wifiname=Route_ip[ind]                
                            print(wifiname)
                            distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
                            print(distance)
                                
                                #correct distance
                            cod=distance-1.5
                            if cod > 0.5:
                                ser.write('w'.encode())        
                                time_run=cod
                                time.sleep(time_run*4)
                                ser.write('s'.encode())
        x0=x[i]
        y0=y[i]
        print(x0)
        print(y0)
                         
    x0=target_x
 
    '''      
    wifiname='EdgeCloud1'
    while wifiscan(wifiname) != 1:
        u=1
    if wifiscan(wifiname) == 1:
        print('connected ',wifiname)
    else:
        print('no signal')
    '''
            
            
    if request.method == 'POST':
        return redirect(url_for('showBooks'))
    else:
        return render_template('editBook.html', current_position=current_position, choose_item=choose_item,
                               target=tagetpoisition)
    

# This will let us Delete our book
@app.route('/start/movingcloud/<int:book_id>/delete/', methods=['GET', 'POST'])
def deleteBook(book_id):
    bookToDelete = session.query(Book).filter_by(id=book_id).first()
    if request.method == 'POST':
        # session.delete(bookToDelete)
        # session.commit()
        print("Item is chosen: ", bookToDelete.title)
        # choose_item=bookToDelete.title
        # choose_position=bookToDelete.author
        return redirect(url_for('editBook', book_id=book_id))
    else:
        return render_template('deleteBook.html', book=bookToDelete)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=4996)
