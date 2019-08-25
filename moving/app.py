from flask import Flask, render_template, request, redirect, url_for
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
        #print(request.form)
        #if request.form.get('action') == 'Cancel':
            #print(request.form.get('action'))
        return render_template('start.html')
    #else:
        #print(request.form.get('action'))
    #bookToDelete = session.query(Book).filter_by(id=book_id).first()
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
        y_string=json.dumps(jsonobj)
        y_store=json.loads(y_string)
        print(jsonobj)
        for element in y_store["books"]:
            listname=element['title']
            listposition = element['author']
            liststatus =element['genre']
            #print(element['title'])
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
        newBook = Book(title=request.form['name'], author=request.form['author'], genre=request.form['genre'])
        session.add(newBook)
        session.commit()
        return redirect(url_for('showBooks'))
    else:
        return render_template('newBook.html')

# This will let us Update our books and save it in our database
@app.route("/start/movingcloud/<int:book_id>/edit/", methods=['GET', 'POST'])
def editBook(book_id):
    editedBook = session.query(Book).filter_by(id=book_id).first()
    #if request.method == 'POST':
        #return redirect(url_for('showBooks'))
    current_position='(35,5)'
    choose_item=editedBook.title
    #print(choose_item)
    #else:
    #print(session.query(Book.title).all())

    url = "http://nguyendung85.pythonanywhere.com/booksApi/"
    url = url + choose_item
    # print(url)
    resp = requests.get(url)
    #print(resp.status_code)
    if resp.status_code == 200:
        pass
    else:
        url = "http://nguyenvandung.pythonanywhere.com/booksApi/"
        url = url + choose_item
        resp = requests.get(url)
    jsonobj = resp.json()

    #return "information is " + jsonobj ['books'] ['author']

    if request.method == 'POST':
        return redirect(url_for('showBooks'))
    else:
        return render_template('editBook.html',current_position=current_position,choose_item=choose_item,target=jsonobj ['books'] ['author'])



# This will let us Delete our book
@app.route('/start/movingcloud/<int:book_id>/delete/', methods=['GET', 'POST'])
def deleteBook(book_id):
    bookToDelete = session.query(Book).filter_by(id=book_id).first()
    if request.method == 'POST':
        #session.delete(bookToDelete)
        #session.commit()
        print("Item is chosen: ", bookToDelete.title)
        #choose_item=bookToDelete.title
        #choose_position=bookToDelete.author
        return redirect(url_for('editBook', book_id=book_id))
    else:
        return render_template('deleteBook.html', book=bookToDelete)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=4996)
