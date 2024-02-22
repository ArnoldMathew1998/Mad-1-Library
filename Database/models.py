from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from datetime import datetime


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
    

class Image(db.Model):
    __tablename__ = 'image'
    image_id = db.Column(db.Integer, primary_key=True)
    image_data = db.Column(db.Text)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
    sec_id = db.Column(db.Integer, db.ForeignKey('book_section.sec_id'), nullable=False)

class User_log(db.Model):
    __tablename__ = 'user_log'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), primary_key=True)
    borrow_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)

class Book_section(db.Model):
    __tablename__ = 'book_section'
    sec_id = db.Column(db.Integer, primary_key=True)
    sec_name = db.Column(db.String, unique=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String, nullable=False)


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    First_name = db.Column(db.String, nullable=False)
    Middle_name = db.Column(db.String, nullable=True)
    Last_name = db.Column(db.String, nullable=True)
    Username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=True)
    mail_id = db.Column(db.String, nullable=False, unique=True)
    
