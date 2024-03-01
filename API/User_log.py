from flask_restful import Resource, fields, marshal_with, reqparse
from Database.models import db, User_log
from datetime import datetime

user_log_fields = {
    'user_id': fields.Integer,
    'book_id': fields.Integer,
    'borrow_date': fields.DateTime(dt_format='iso8601'),
    'return_date': fields.DateTime(dt_format='iso8601')
}

User_log_parser = reqparse.RequestParser()
User_log_parser.add_argument('user_id', type=int, required=True, help='User ID')
User_log_parser.add_argument('book_id', type=int, required=True, help='Book ID')
User_log_parser.add_argument('borrow_date', type=str, required=True, help='Return Date (YYYY-MM-DD)')
User_log_parser.add_argument('return_date', type=str, required=True, help='Return Date (YYYY-MM-DD)')

class User_log_api(Resource):
    @marshal_with(user_log_fields)
    def get(self, user_id=None, book_id=None):
        if user_id:
            user_logs = User_log.query.filter_by(user_id=user_id).all()
            if user_logs:
                return user_logs
            else:
                return {'message': 'User logs not found for the specified user_id'}, 404
        elif book_id:
            user_log = User_log.query.filter_by(user_id=user_id, book_id=book_id).first()
            if user_log:
                return user_log
            else:
                return {'message': 'User log not found for the specified book_id'}, 404
        else:
            all_user_logs = User_log.query.all()
            if all_user_logs:
                return all_user_logs
            else:
                return {'message': 'No user logs found in the database'}, 404

    @marshal_with(user_log_fields)
    def post(self):
        User_log_args = User_log_parser.parse_args()
        borrow_date = datetime.strptime(User_log_args['borrow_date'], '%Y-%m-%dT%H:%M')
        return_date = datetime.strptime(User_log_args['return_date'], '%Y-%m-%dT%H:%M')
        new_user_log = User_log(
            user_id=User_log_args['user_id'],
            book_id=User_log_args['book_id'],
            borrow_date=borrow_date,
            return_date=return_date
        )
        db.session.add(new_user_log)
        db.session.commit()

        return new_user_log, 201

    def delete(self, user_id=None, book_id=None):
        if user_id is None and book_id is None:
            print("User auto delete")
            current_datetime = datetime.now()
            expired_logs = User_log.query.filter(User_log.return_date <= current_datetime).all()
            for log in expired_logs:
                db.session.delete(log)
                db.session.commit()
            return {'message': 'Expired logs deleted successfully'}, 201
        user_log = User_log.query.filter_by(user_id=user_id, book_id=book_id).first()
        if user_log:
            db.session.delete(user_log)
            db.session.commit()
            return {'message': 'User log deleted successfully'}
        else:
            return {'message': 'User log not found'}, 404
