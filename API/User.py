from flask_restful import Resource, fields, marshal_with, reqparse
from Database.models import db, User
from flask import redirect,url_for
from datetime import datetime
from Controller.login import User_login
User_parser = reqparse.RequestParser()
User_parser.add_argument('First_name', type=str, location='form', help='First name of the user')
User_parser.add_argument('Middle_name', type=str, location='form', help='Middle name of the user')
User_parser.add_argument('Last_name', type=str, location='form', help='Last name of the user')
User_parser.add_argument('Username', type=str, location='form', help='Username of the user')
User_parser.add_argument('password', type=str, location='form', help='Password of the user')
User_parser.add_argument('mail_id', type=str, location='form', help='Mail ID of the user')


user_output = {
    'id': fields.Integer,
    'First_name': fields.String,
    'Middle_name': fields.String,
    'Last_name': fields.String,
    'Username': fields.String,
    'password': fields.String,
    'mail_id': fields.String
}


class User_id(Resource):

    @marshal_with(user_output)
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return user
        else:
            return {'message': 'User not found'}, 404
        
    @marshal_with(user_output)
    def post(self):
        User_args = User_parser.parse_args()
        new_user = User(
        First_name=User_args['First_name'],
        Middle_name=User_args['Middle_name'],
        Last_name=User_args['Last_name'],
        Username=User_args['Username'],
        password=User_args['password'],
        mail_id=User_args['mail_id'])

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user_dashboard', user_id=new_user.id))

    
    @marshal_with(user_output)
    def put(self, user_id):
        User_args = User_parser.parse_args()
        user = User.query.get(user_id)
        if user:
            user.First_name = User_args['First_name']
            user.Middle_name = User_args['Middle_name']
            user.Last_name = User_args['Last_name']
            user.Username = User_args['Username']
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
        
class User_Mail_id(Resource):

    @marshal_with(user_output)
    def get(self, mail_id):
        user = User.query.filter_by(mail_id=mail_id).first()
        if user:
            return user
        else:
            return {'message': 'User not found'}, 404
        
class User_Username(Resource):

    @marshal_with(user_output)
    def get(self, username):
        user = User.query.filter_by(Username=username).first()
        if user:
            return user
        else:
            return {'message': 'User not found'}, 404
