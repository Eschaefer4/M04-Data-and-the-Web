import sys
sys.path.append('D:\\ivytech\\M04-Data-and-the-Web\\.venv\\Lib\\site-packages\\flask')
sys.path.append('D:\\ivytech\\M04-Data-and-the-Web\\.venv\\Lib\\site-packages\\flask_sqlalchemy')
sys.path.append('D:\\ivytech\\M04-Data-and-the-Web\\.venv\\Lib\\site-packages\\sqlalchemy')
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    publisher = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"{self.book_name} by {self.author}, published by {self.publisher}"
    

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