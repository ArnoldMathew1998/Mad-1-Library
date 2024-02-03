from flask_restful import Resource, fields, marshal_with, reqparse
from Database.models import db,Book


book_parser = reqparse.RequestParser()
book_parser.add_argument('book_name', type=str, required=True, help='Book name cannot be blank')
book_parser.add_argument('author_name', type=str, required=True, help='Author name cannot be blank')
book_parser.add_argument('date_issued', type=str, required=True, help='Date issued cannot be blank')
book_parser.add_argument('content', type=str, required=True, help='Content cannot be blank')
book_parser.add_argument('language', type=str, required=True, help='Language cannot be blank')
book_parser.add_argument('sec_id', type=int, required=True, help='Section ID cannot be blank')


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

        return {'message': 'Book added successfully'}

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
            return {'message': 'Book updated successfully'}
        return {'message': 'Book not found'}, 404

    def delete(self, book_id):
        book = Book.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return {'message': 'Book deleted successfully'}
        return {'message': 'Book not found'}, 404

