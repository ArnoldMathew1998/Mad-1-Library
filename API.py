from flask_restful import Resource, Api, fields, marshal_with, reqparse
from models import db,Book,Book_section,Image,User_log,User
import datetime
api=Api()

#------------------------------------------------BOOK_SECTION_API-----------------------------------------------------------------

# Parser for parsing incoming data
Book_section_parser = reqparse.RequestParser()
Book_section_parser.add_argument('sec_name', type=str, help='Name of the book section')
Book_section_parser.add_argument('description', type=str, help='Description of the book section')
Book_section_args = Book_section_parser.parse_args()

# Resource for Book_section
class Book_section_api(Resource):
    def get(self, sec_id):
        book_section = Book_section.query.get(sec_id)
        if book_section:
            return book_section
        else:
            return {'message': 'Book section not found'}, 404
    def put(self, sec_id):
        book_section = Book_section.query.get(sec_id)
        if book_section:
            book_section.sec_name = Book_section_args['sec_name'] if Book_section_args['sec_name'] else book_section.sec_name
            book_section.description = Book_section_args['description'] if Book_section_args['description'] else book_section.description
            db.session.commit()
            return book_section
        else:
            return {'message': 'Book section not found'}, 404
    def post(self):
        new_book_section = Book_section(
            sec_name=Book_section_args['sec_name'],
            description=Book_section_args['description'],
            date_created=datetime.now()
        )
        db.session.add(new_book_section)
        db.session.commit()
        return new_book_section, 201

    def delete(self, sec_id):
        book_section = Book_section.query.get(sec_id)
        if book_section:
            db.session.delete(book_section)
            db.session.commit()
            return {'message': 'Book section deleted successfully'}
        else:
            return {'message': 'Book section not found'}, 404


#----------------------------------------------------BOOK_API---------------------------------------------------------------------
book_parser = reqparse.RequestParser()
book_parser.add_argument('book_name', type=str, required=True, help='Book name cannot be blank')
book_parser.add_argument('author_name', type=str, required=True, help='Author name cannot be blank')
book_parser.add_argument('date_issued', type=str, required=True, help='Date issued cannot be blank')
book_parser.add_argument('content', type=str, required=True, help='Content cannot be blank')
book_parser.add_argument('language', type=str, required=True, help='Language cannot be blank')
book_parser.add_argument('sec_id', type=int, required=True, help='Section ID cannot be blank')
book_args = book_parser.parse_args()

class Book_api(Resource):
    def get(self, book_id):
        book = Book.query.get(book_id)
        if book:
            return {
                'book_id': book.book_id,
                'book_name': book.book_name,
                'author_name': book.author_name,
                'date_issued': book.date_issued,
                'content': book.content,
                'language': book.language,
                'sec_id': book.sec_id
            }
        return {'message': 'Book not found'}, 404

    def post(self):
        new_book = Book(
            book_name = book_args['book_name'],
            author_name = book_args['author_name'],
            date_issued = book_args['date_issued'],
            content = book_args['content'],
            language = book_args['language'],
            sec_id = book_args['sec_id']
        )

        db.session.add(new_book)
        db.session.commit()

        return {'message': 'Book added successfully'}

    def put(self, book_id):
        book = Book.query.get(book_id)
        if book:
            book.book_name = book_args['book_name']
            book.author_name = book_args['author_name']
            book.date_issued = book_args['date_issued']
            book.content = book_args['content']
            book.language = book_args['language']
            book.sec_id = book_args['sec_id']

            db.session.commit()
            return {'message': 'Book updated successfully'}
        return {'message': 'Book not found'}, 404

    def delete(self, book_id):
        book = Book.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return {'message': 'Book deleted successfully'}
        return {'message': 'Book not found'}, 404
#---------------------------------------------------------USER_LOG_API--------------------------------------------------------------
class User_log_api():
    def get():
        pass
    def put():
        pass
    def post():
        pass
    def delete():
        pass
#--------------------------------------------------------------USER_API--------------------------------------------------------------
class User_api():
    def get():
        pass
    def put():
        pass
    def post():
        pass
    def delete():
        pass
#-------------------------------------------------------------IMAGE_API---------------------------------------------------------------
class Image_api():
    def get():
        pass
    def put():
        pass
    def post():
        pass
    def delete():
        pass
#----------------------------------------------------------RESOURCES_LINK--------------------------------------------------------------
api.add_resource(Book_api, '/books', '/books/<int:book_id>')
api.add_resource(Book_section_api, '/book_sections', '/book_sections/<int:sec_id>')