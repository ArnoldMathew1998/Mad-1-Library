from flask_restful import Resource, fields, marshal_with, reqparse
from Database.models import db, User
from datetime import datetime

User_parser = reqparse.RequestParser()
User_parser.add_argument('First_name', type=str, help='First name of the user')
User_parser.add_argument('Middle_name', type=str, help='Middle name of the user')
User_parser.add_argument('Last_name', type=str, help='Last name of the user')
User_parser.add_argument('Username_name', type=str, help='Username of the user')
User_parser.add_argument('password', type=str, help='Password of the user')
User_parser.add_argument('mail_id', type=str, help='Mail ID of the user')

class User_api(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return user
        else:
            return {'message': 'User not found'}, 404
        
    def post(self):
        User_args = User_parser.parse_args()
        new_user = User(
            First_name=User_args['First_name'],
            Middle_name=User_args['Middle_name'],
            Last_name=User_args['Last_name'],
            Username_name=User_args['Username_name'],
            password=User_args['password'],
            mail_id=User_args['mail_id']
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201
    
    def put(self, user_id):
        User_args = User_parser.parse_args()
        user = User.query.get(user_id)
        if user:
            user.First_name = User_args['First_name']
            user.Middle_name = User_args['Middle_name']
            user.Last_name = User_args['Last_name']
            user.Username_name = User_args['Username_name']
            user.password = User_args['password']
            user.mail_id = User_args['mail_id']
            db.session.commit()
            return user
        else:
            return {'message': 'User not found'}, 404
        
    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}
        else:
            return {'message': 'User not found'}, 404
        
