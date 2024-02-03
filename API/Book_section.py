from flask_restful import Resource, fields, marshal_with, reqparse
from Database.models import db,Book_section
from datetime import datetime


# Parser for parsing incoming data
Book_section_parser = reqparse.RequestParser()
Book_section_parser.add_argument('sec_name', type=str, help='Name of the book section')
Book_section_parser.add_argument('description', type=str, help='Description of the book section')

book_fields = {
    'sec_name': fields.String,
    'description': fields.String,
    'date_created': fields.String,
}

# Resource for Book_section
class Book_section_api(Resource):
    @marshal_with(book_fields)
    def get(self, sec_id):
        book_section = Book_section.query.get(sec_id)
        if book_section:
            return book_section
        else:
            return {'message': 'Book section not found'}, 404
        
    @marshal_with(book_fields)
    def put(self, sec_id):
        Book_section_args = Book_section_parser.parse_args()
        book_section = Book_section.query.get(sec_id)
        if book_section:
            book_section.sec_name = Book_section_args['sec_name'] if Book_section_args['sec_name'] else book_section.sec_name
            book_section.description = Book_section_args['description'] if Book_section_args['description'] else book_section.description
            db.session.commit()
            return book_section
        else:
            return {'message': 'Book section not found'}, 404
        
    @marshal_with(book_fields)
    def post(self):
        Book_section_args = Book_section_parser.parse_args()
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
