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

    url = 'http://nguyenvandung.pythonanywhere.com/'
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
    current_position = '(0,0)'
    choose_item = editedBook.title
    # print(choose_item)
    # else:
    # print(session.query(Book.title).all())
    current_ip='117.113.128.23'

    url = "http://nguyendung85.pythonanywhere.com/booksApi/"
    url = url + choose_item
    # print(url)
    resp = requests.get(url)
    # print(resp.status_code)
    if resp.status_code == 200:
        target_ip=current_ip
        pass
    else:
        url = "http://nguyenvandung.pythonanywhere.com/booksApi/"
        url = url + choose_item
        resp = requests.get(url)
    jsonobj = resp.json()
    tagetpoisition=jsonobj ['books'] ['author']
    # return "information is " + jsonobj ['books'] ['author']

    url = 'http://nguyenvandung.pythonanywhere.com/'
    url = url + '/booksApi'
    # print(url)
    resp = requests.get(url)
    # print(resp.status_code)
    listwifi = []
    listwifipo = []
    a = 1
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
            if '.com' in listname:
                pass
            else:
                if '.' in listname:
                    if listposition==tagetpoisition:
                        target_ip=listname

    ''''  '''
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
    url = 'http://nguyenvandung.pythonanywhere.com/'
    url = url + '/booksApi'
    # print(url)
    resp = requests.get(url)
    # print(resp.status_code)
    listwifi = []
    listwifipo = []
    a = 1
    if resp.status_code == 200:
        jsonobj = resp.json()
        y_string = json.dumps(jsonobj)
        y_store = json.loads(y_string)
        #print(jsonobj)
        for element in y_store ["books"]:
            listname = element ['title']
            listposition = element ['author']
            liststatus = element ['genre']
            #print(listname)
            if '.com' in listname:
                pass
            else:
                if '.' in listname:
                    listwifi.insert(a,listname)
                    listwifipo.insert(a,listposition)
                    a = a + 1
    #print(len(listwifi))
    #print(listwifipo)
    #print(listwifi)
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
                    if distance<60:
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
        for ai in range(0,len(Route_ip)):
            #print(Route_ip[ai])
            for bj in range(0,len(listwifi)):
                if Route_ip[ai]==listwifi[bj]:
                    Route_po.insert(aj,listwifipo[bj])
                    aj=aj+1
        #print(Route_po)
    else:
        print('Local processing')
        Route_po=''
        Route_ip=''
    '''
    save file Dictwrite
    '''
    import csv

    header=['id','item','current','target','Route_ip','Route_po']

    rows=[{
            'id':1,
            'item':choose_item,
            'current':current_position,
            'target':tagetpoisition,
            'Route_ip':Route_ip ,
            'Route_po':Route_po
        }]
    with open('savedata.csv','wt') as f:
        csv_writer = csv.DictWriter(f, fieldnames=header)
        csv_writer.writeheader()
        csv_writer.writerows(rows)

    with open('savedata.csv') as f:
        fields = ['id', 'item', 'current', 'target', 'Route_ip', 'Route_po']
        csv_reader=csv.DictReader(f,fieldnames=fields)
        for row in csv_reader:
            xa=row['Route_ip']
            ya=row['Route_po']
            #print(row['Route_ip'])
        #print(type(xa))
        #print(xa)
        #print(type(ya))
        #print(ya)
        a=0
        ab=0
        xa_save=[]
        for i in range(0,len(xa)):
            savesa=''
            i=ab
            if(i)>len(xa):
                break
            if xa[i]== "'":
                i=i+1
                #print(i)
                #print(len(xa))
                if i > len(xa) - 3:
                    break
                while xa[i] != "'":
                    savesa=savesa+xa[i]
                    i=i+1
                    if i > len(xa)-3:
                        break
                    ab=i
                #print(savesa)
                if ',' in savesa:
                    pass
                else:
                    xa_save.insert(a,savesa)
            else:
                ab=ab+1
            a=a+1

        a = 0
        ab = 0
        ya_save = []
        for i in range(0, len(ya)):
            savesa = ''
            i = ab
            if (i) > len(ya):
                break
            if ya[i] == "'":
                i = i + 1
                # print(i)
                # print(len(xa))
                if i > len(ya) - 3:
                    break
                while ya [i] != "'":
                    savesa = savesa + ya[i]
                    i = i + 1
                    if i > len(ya) - 3:
                        break
                    ab = i
                #print(savesa)
                if len(savesa) < 3:
                    pass
                else:
                    ya_save.insert(a,savesa)
            else:
                ab = ab + 1
            a = a + 1
        #print(xa_save)
        #print(ya_save)        
        list_name_ip=[]
        ia=0
        for i in range(0,len(xa_save)):
            if xa_save[i] == '192.168.4.1':
                list_name_ip.insert(ia,'EdgeCloud1')
            if xa_save[i] == '192.168.5.1':
                list_name_ip.insert(ia,'EdgeCloud2')
            if xa_save[i] == '192.168.6.1':
                list_name_ip.insert(ia,'EdgeCloud3')
            ia=ia+1

        print('Chosen item %s is being taken' %choose_item)
        print('From:           ',current_position)
        print('To:             ',tagetpoisition)
        print('Route IP:       ',xa_save)
        print('Route position: ', ya_save)
    def decision(arg1, arg2):
        if arg1 + 0.35 < arg2:
            d=arg2-arg1
            deci=0
        else:
            if arg1 > arg2 +0.35:
                d = arg1-arg2
                deci=1
            else:
                deci=2
        return d,deci

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

    
   # Creating Scheme with my SSID.
#    myssid= Scheme.for_cell('wlan0','home', myssid, 'qwer1234') # qwer1234 is the password to my wifi myssid is the wifi name 
# 
#    print(myssid, type(myssid))
#    myssid.save()
#    myssid.activate()     
    x0=0
    y0=0
    '''
    task 1: move (0,0) to (3,0)

    '''
    x=4
    y=0
    a=decision(x0,x)
    print(a)
    if a[1]==0:
        print('Self-driving cart will move ...')
        ser.write('w'.encode())        
        time_run=int(a[0])
        time.sleep(time_run*4)
        ser.write('s'.encode()) 
        print('Self-driving cart have moved with ', time_run*5, ' seconds')
        '''
        print('Self-driving cart will move ...')
        ser.write('l'.encode())
        time.sleep(7)
        ser.write('o'.encode())
        time_run=int(a[0])
        time.sleep(time_run*4)
        ser.write('s'.encode()) 
        print('Self-driving cart have moved with ', time_run*5, ' seconds')
        ''' 
        
        ''' step 2: check connect'''
        wifiname='EdgeCloud1'
        if wifiscan(wifiname) == 1:
            print('connected ',wifiname)
        else:
            print('no signal')
        #for signalAttenuation in range(1,4,0.1):
        distance = getDistanceFromAP(wifiname, signalAttenuation, ref_distance, ref_signal, n_iter)
        print(distance)
            
        cod=distance-1.5
        if cod > 0.5:
            ser.write('w'.encode())        
            time_run=cod
            time.sleep(time_run*4)
            ser.write('s'.encode()) 
        
        print('Self-driving cart will turn left ...')
        ser.write('w'.encode())
        time.sleep(1)
        ser.write('l'.encode())
        time.sleep(7)
        ser.write('o'.encode())
        time_run=int(a[0])
        time.sleep(time_run*4)
        ser.write('s'.encode()) 
        
        wifiname='DistCloud'
        while wifiscan(wifiname)!=1:
            u=1            
        #os.system('sudo ./switchwifi DistCloud')
    '''
    check location 1
    '''
    x=[]
    y=[]
    i=0
    #print(len(ya_save))
    #print(ya_save [1])
    #print(int(ya_save [1].split(",") [0]))
    #print(int(ya_save [1].split(",") [1]))
    for aj in range(0, len(ya_save)):
        # print(listwifi[aj])
        x.insert(i,int(ya_save [aj].split(",") [0]))
        y.insert(i, int(ya_save [aj].split(",") [1]))
        i=i+1
    #print(x)
    #print(y)

    '''
    check x_axis
    
    '''
    for i in range(0,len(x)):
        a=decision(x0,x[i])
        b=decision(y0,y[i])
        while a[1]==2 and b[1] ==2:
            a = decision(x0, x [i])
            b = decision(y0, y [i])
            if a[1]==0:
                print("go straight ahead")
                time=a[0]
                print("time == ", time)
                '''run'''

                '''update position'''
                #x0=
            if a[1]==1:
                print("go straight back")
                time = a[0]
                print("time == ", time)
                '''run'''

                '''update position'''
                # x0=
            if a[1] ==2:
                b=decision(y0,y[1])
                if b[1] == 0:
                    print("turn left")
                    '''control turn'''
                    time = b[0]
                    print("time == ", time)
                    '''run'''

                    '''update position'''
                    # y0=
                if b[1] == 1:
                    print("turn right")
                    '''control turn'''
                    time = b[0]
                    print("time == ", time)
                    '''run'''

                    '''update position'''
                    # y0=


            #if bc==1:
                #xa_save[a]=savexa
        #print(xa_save)



        #print(csv_reader['Route_ip'])

    #import pandas
    #df=pandas.read_csv('savedata.csv')
    #print(df)

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
