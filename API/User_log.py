from flask_restful import Resource, fields, marshal_with, reqparse
from Database.models import db,User_log
from datetime import datetime


User_log_parser = reqparse.RequestParser()
User_log_parser.add_argument('user_id', type=int, required=True, help='User ID')
User_log_parser.add_argument('book_id', type=int, required=True, help='Book ID')
User_log_parser.add_argument('borrow_date', type=str, required=True, help='Borrow Date (YYYY-MM-DD)')
User_log_parser.add_argument('return_date', type=str, required=True, help='Return Date (YYYY-MM-DD)')


class User_log_api(Resource):
    def get(self, user_id, book_id):
        user_log = User_log.query.filter_by(user_id=user_id, book_id=book_id).first()
        if user_log:
            return user_log
        else:
            return {'message': 'User log not found'}, 404
    def post(self):
        User_log_args = User_log_parser.parse_args()
        new_user_log = User_log(
            user_id=User_log_args['user_id'],
            book_id=User_log_args['book_id'],
            borrow_date=datetime.strptime(User_log_args['borrow_date'], '%Y-%m-%d'),
            return_date=datetime.strptime(User_log_args['return_date'], '%Y-%m-%d')
        )
        db.session.add(new_user_log)
        db.session.commit()
        return new_user_log, 201

    def delete(self, user_id, book_id):
        user_log = User_log.query.filter_by(user_id=user_id, book_id=book_id).first()
        if user_log:
            db.session.delete(user_log)
            db.session.commit()
            return {'message': 'User log deleted successfully'}
        else:
            return {'message': 'User log not found'}, 404
        
