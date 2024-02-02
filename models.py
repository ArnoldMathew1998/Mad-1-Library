from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'book'
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String, unique=True, nullable=False)
    author_name = db.Column(db.String, nullable=False)
    date_issued = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    language = db.Column(db.String, nullable=False)
    sec_id = db.Column(db.Integer, db.ForeignKey('book_section.sec_id'), nullable=False)
    book_section = db.relationship('Book_section', backref=backref('books', cascade='all, delete-orphan'))
    images = db.relationship('Image', backref=backref('book', cascade='all, delete-orphan'))
    user_logs = db.relationship('User_log', backref=backref('book', cascade='all, delete-orphan'))

class Image(db.Model):
    __tablename__ = 'image'
    image_id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary) 
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)

class User_log(db.Model):
    __tablename__ = 'user_log'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), primary_key=True)
    borrow_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)

class Book_section(db.Model):
    __tablename__ = 'book_section'
    sec_id = db.Column(db.Integer, primary_key=True)
    sec_name = db.Column(db.String, nullable=False)
    date_created = db.Column(db.Date, nullable=False)
    description = db.Column(db.String, nullable=False)
    books = db.relationship('Book', backref=backref('book_section', cascade='all, delete-orphan'))

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    First_name = db.Column(db.String, nullable=False)
    Middle_name = db.Column(db.String, nullable=True)
    Last_name = db.Column(db.String, nullable=True)
    Username_name = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=True)
    mail_id = db.Column(db.String, nullable=False, unique=True)
    user_logs = db.relationship('User_log', backref=backref('user', cascade='all, delete-orphan'))