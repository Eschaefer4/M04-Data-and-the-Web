import sys
sys.path.append('.venv\\Lib\\site-packages\\')

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    publisher = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"{self.book_name} by {self.author}, published by {self.publisher}"
    
db.create_all()

@app.route('/')
def index():
    return 'Hello!'

@app.route('/books')
def get_books():
    books = Book.query.all()
    output = []
    for book in books:
        book_data = {'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher}
        output.append(book_data)
    return {"books": output}

@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher})

@app.route('/books', methods=['POST'])
def add_book():
    book = Book(book_name=request.json['book_name'], author=request.json['author'], publisher=request.json['publisher'])
    db.session.add(book)
    db.commit()
    return {"id":book.id}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book():
    book = Book.query.get(id)
    if book is None:
        return {"Error":"not found"}
    db.session.delete(book)
    db.session.commit()
    return {"message":"deleted"}