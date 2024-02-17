from flask_restful import Resource, fields, marshal_with, reqparse,request
from Database.models import db,Book


book_parser = reqparse.RequestParser()
book_parser.add_argument('book_name', type=str, required=True, help='Book name cannot be blank')
book_parser.add_argument('author_name', type=str, required=True, help='Author name cannot be blank')
book_parser.add_argument('date_issued', type=str, required=True, help='Date issued cannot be blank')
book_parser.add_argument('content', type=str, required=True, help='Content cannot be blank')
book_parser.add_argument('language', type=str, required=True, help='Language cannot be blank')
book_parser.add_argument('sec_id', type=int, required=True, help='Section ID cannot be blank')

Book_fields={
    'book_id': fields.Integer,
    'book_name': fields.String,
    'author_name': fields.String,
    'date_issued': fields.String,
    'content' : fields.String,
    'language': fields.String,
    'sec_id' : fields.Integer
    }

class Book_api(Resource):
    @marshal_with(Book_fields)
    def get(self, book_id=None):
        section_id = request.args.get('section_id')

        if section_id:
            books = Book.query.filter_by(sec_id=section_id).all()
            if books:
                return books
            else:
                return {'message': 'No books found for the given section ID'}, 404
        elif book_id:
            book = Book.query.get(book_id)
            if book:
                return book
            else:
                return {'message': 'Book not found'}, 404
        else:
            books = Book.query.all()
            if books:
                return books
            else:
                return {'message': 'Books not found'}, 404
    
    def post(self):
        book_args = book_parser.parse_args()
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

        return {'message': 'Book added successfully'}, 201

    def put(self, book_id):
        book_args = book_parser.parse_args()
        book = Book.query.get(book_id)
        if book:
            book.book_name = book_args['book_name']
            book.author_name = book_args['author_name']
            book.date_issued = book_args['date_issued']
            book.content = book_args['content']
            book.language = book_args['language']
            book.sec_id = book_args['sec_id']

            db.session.commit()
            return {'message': 'Book updated successfully'}, 201
        return {'message': 'Book not found'}, 404

    def delete(self, book_id):
        book = Book.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return {'message': 'Book deleted successfully'}, 201
        return {'message': 'Book not found'}, 404

