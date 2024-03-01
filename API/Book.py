from flask_restful import Resource, fields, marshal_with, reqparse,request
from Database.models import db, Book 

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
        book_name = request.args.get('book_name')
        author_name = request.args.get('author_name')
        year = request.args.get('year')
        content = request.args.get('content')
        language = request.args.get('language')
        sec_id = request.args.get('sec_id')

        query = Book.query

        if book_id:
            book = query.get(book_id)
            if book:
                return book
            else:
                return {'message': 'Book not found'}, 404

        if book_name:
            query = query.filter_by(book_name=book_name)

        if author_name:
            query = query.filter_by(author_name=author_name)

        if year:
            query = query.filter(Book.date_issued.like(f'{year}%'))

        if content:
            query = query.filter(Book.content.like(f'%{content}%'))

        if language:
            query = query.filter_by(language=language)

        if sec_id:
            query = query.filter_by(sec_id=sec_id)

        books = query.all()

        if books:
            return books
        else:
            return {'message': 'Book not found'}, 404

    
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

        return {'message': 'Book added successfully', 'book_id': new_book.book_id}, 201

    def put(self, book_id):
        book_args = book_parser.parse_args()
        book = Book.query.get(book_id)
        if book:
            book.book_name = book_args['book_name']
            book.author_name = book_args['author_name']
            book.date_issued = book_args['date_issued']
            book.content = book_args['content']
            book.language = book_args['language']

            db.session.commit()
            return {'message': 'Book updated successfully', 'book_id': book_id}, 201
        return {'message': 'Book not found'}, 404

    def delete(self, book_id=None):
        sec_id = request.args.get('sec_id')
        if sec_id:
            Book.query.filter_by(sec_id=sec_id).delete()
            db.session.commit()
            return {'message': 'Book deleted successfully'}, 201
        if book_id:
            book = Book.query.get(book_id)
            if book:
                db.session.delete(book)
                db.session.commit()
                return {'message': 'Book deleted successfully'}, 201
        return {'message': 'Book not found'}, 404

