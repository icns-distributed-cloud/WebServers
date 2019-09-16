from flask import Flask, render_template, request, redirect, url_for
import requests
import json
from flask import jsonify

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
@app.route('/corecloud', methods=['GET', 'POST'])
def showBooks():
    # newBook = Book(title=request.form['name'], author=request.form['author'], genre=request.form['genre'])
    # session.add(newBook)
    # session.commit()
    # qyr = '''DELETE FROM book WHERE book.title = ?'''
    #try:
    #cur = session.cursor()
    engine.execute("DELETE FROM book WHERE book.title NOT LIKE '%.com%';")
    ac = session.query(Book.title).filter(Book.title.like('%.com%')).all()
    if len(ac) == 0:
        engine.execute("DELETE FROM book;")
        ##engine.execute("SELECT * FROM book WHERE book.title='cola'")
        ##sengine.execute("UPDATE book SET book.author WHERE book.title='cola'")
        # print("cola deleted")
    session.commit()
    #except:
        #session.rollback()
        # print("cola no delete")
    # session.close()
    # editedBook = session.query(Book).filter_by(title='cola').first()
    # editedBook.author = "hello"
    # session.add(editedBook)
    # session.commit()
    if request.method == 'POST':
        ten = request.form['name']
        try:
            resp=urlopen('http://%s' %ten)
        except HTTPError as e:
                print(e.code)
        except URLerror as e:
                print(e.code)
        ## check link exit or not
        print(ten)
        if ':8000' in ten:
            code = urlopen('http://%s' %ten).code
            print(code)
            if code == 200:
            # editedBook = session.query(Book).filter_by(title=ten).first()
            # editedBook.author = listposition
            # editedBook.genre = liststatus
            # session.add(editedBook)
            # session.commit()
                try:
                    # update data
                    editedBook = session.query(Book).filter_by(title=ten).first()
                    editedBook.name = ten
                    # editedBook.genre = liststatus
                    # session.add(editedBook)
                    # session.commit()
                    # print("Update URL")
                except:
                    newBook = Book(title=ten, author='', genre='')
                    session.add(newBook)
                    session.commit()
    # print(session.query(Book).all())
    # print("\n")
    #listBook = session.query(Book).filter_by(author=aaaa).first()
    #resp=req.get('http://%s' %listurl)
        #print(resp)
        #if resp.status_code == 200:
          # print('Success!')
       # else:
           #print(" An erroe has occurd")
    #print(listBook.title)
    #for listurl in aaaa:
    #print(listurl,"\n")
    #for ida in aaaa:
      #  listurl = session.query(Book).filter_by(id=ida).first()
    # bookToDelete = session.query(Book).filter_by(title='cola')
    # print(bookToDelete)
    #################### show URL
    # x=aaaa.find("cola")
    # x=Book.find("cola")
    # prin(x)
    # session.delete(bookToDelete)
    # session.commit()
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

    aaaa = session.query(Book.title).filter(Book.title.like('%:8000%')).all()
    bc = [item[0] for item in aaaa]
    print(bc)
    if len(bc) > 0:
        for listurl in bc:
            #print('http://%s' %listurl)
            url = 'http://%s' %listurl
            url=url+'/booksApi'
            # print(url)
            resp = requests.get(url)
            savepositon=''
            # print(resp.status_code)
            if resp.status_code == 200:
                jsonobj = resp.json()
                y_string = json.dumps(jsonobj)
                y_store = json.loads(y_string)
                #print(jsonobj)
                for element in y_store ["books"]:
                    listname = element ['title']
                    listposition = element ['author']
                    if '.' in listname:
                        savepositon=listposition
                    liststatus = element ['genre']
                    # print(element['title'])
                    try:
                        editedBook = session.query(Book).filter_by(title=listname).first()
                        editedBook.author = savepositon
                        editedBook.genre = liststatus
                        session.add(editedBook)
                        session.commit()
                        # print("Update cola")
                    except:
                        newBook = Book(title=listname, author=savepositon, genre=liststatus)
                        session.add(newBook)
                        session.commit()
    books = session.query(Book).all()
    return render_template("books.html", books=books)


@app.route('/fixedcloud/new/', methods=['GET', 'POST'])
def newBook():
    if request.method == 'POST':
        newBook = Book(title=request.form['name'], author=request.form['author'], genre=request.form['genre'])
        session.add(newBook)
        session.commit()
        return redirect(url_for('showBooks'))
    else:
        return render_template('newBook.html')


# This will let us Update our books and save it in our database
@app.route("/fixedcloud/<int:book_id>/edit/", methods=['GET', 'POST'])
def editBook(book_id):
    editedBook = session.query(Book).filter_by(id=book_id).first()
    if request.method == 'POST':
        if request.form['name']:
            if request.form['name'].find('.com'):
                editedBook.title = request.form['name']
                # session.add(editedBook)
                # session.commit()
            else:
                render_template('editBook.html', book=editedBook)
            return redirect(url_for('showBooks'))
    else:
        return render_template('editBook.html', book=editedBook)


# This will let us Delete our book
@app.route('/fixedcloud/<int:book_id>/delete/', methods=['GET', 'POST'])
def deleteBook(book_id):
    bookToDelete = session.query(Book).filter_by(id=book_id).first()
    if request.method == 'POST':
        if request.form['name'] == 'Delete':
            session.delete(bookToDelete)
            session.commit()
        return redirect(url_for('showBooks', book_id=book_id))
    else:
        return render_template('deleteBook.html', book=bookToDelete)

"""
api functions
"""
from flask import jsonify


def get_books():
    books = session.query(Book).all()
    return jsonify(books=[b.serialize for b in books])


def get_book(book_id):
    books = session.query(Book).filter_by(title=book_id).one()
    return jsonify(books=books.serialize)


def makeANewBook(title, author, genre):
    addedbook = Book(title=title, author=author, genre=genre)
    session.add(addedbook)
    session.commit()
    return jsonify(Book=addedbook.serialize)


def updateBook(id, title, author, genre):
    updatedBook = session.query(Book).filter_by(id=id).one()
    if not title:
        updatedBook.title = title
    if not author:
        updatedBook.author = author
    if not genre:
        updatedBook.genre = genre
    session.add(updatedBook)
    session.commit()
    return 'Updated a Book with id %s' % id


def deleteABook(id):
    bookToDelete = session.query(Book).filter_by(id=id).one()
    session.delete(bookToDelete)
    session.commit()
    return 'Removed Book with id %s' % id


@app.route('/')
@app.route('/booksApi', methods=['GET', 'POST'])
def booksFunction():
    if request.method == 'GET':
        return get_books()
    elif request.method == 'POST':
        title = request.args.get('title', '')
        author = request.args.get('author', '')
        genre = request.args.get('genre', '')
        return makeANewBook(title, author, genre)


@app.route('/booksApi/<id>', methods=['GET', 'PUT', 'DELETE'])
def bookFunctionId(id):
    if request.method == 'GET':
        return get_book(id)

    elif request.method == 'PUT':
        title = request.args.get('title', '')
        author = request.args.get('author', '')
        genre = request.args.get('genre', '')
        return updateBook(id, title, author, genre)

    elif request.method == 'DELETE':
        return deleteABook(id)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=4996)
