from flask import Flask, session
from flask_restful import Api
from Database.models import db
from API.Book_section import Book_section_api
from API.Book import Book_api
from API.Image import Image_api
from API.User import User_id, User_Mail_id, User_Username
from API.User_log import User_log_api
from Controller.login import Home, User_login, Admin_login, Registration,user_dashboard,logout,Admin_dashboard
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)
app.config['SECRET_KEY'] = 'Mad-1-project'

# Add resources to the API
api.add_resource(Book_api, '/books', '/books/<int:book_id>')
api.add_resource(Book_section_api, '/book_sections', '/book_sections/<int:sec_id>')
api.add_resource(User_log_api, '/user_logs/<int:user_id>/<int:book_id>', '/user_logs')

api.add_resource(User_id, '/user/id', '/users/id/<int:user_id>')
api.add_resource(User_Mail_id, '/user/mail/<string:mail_id>')
api.add_resource(User_Username, '/user/username/<string:username>')




api.add_resource(Image_api, '/images', '/images/<int:image_id>')

# Routes for web pages
app.add_url_rule('/', 'Home', Home)
app.add_url_rule('/User_login', 'User_login', User_login, methods=['GET','POST'])
app.add_url_rule('/Admin_login', 'Admin_login', Admin_login)
app.add_url_rule('/Registration', 'Registration', Registration)
app.add_url_rule('/user_dashboard/<int:user_id>','user_dashboard',user_dashboard)
app.add_url_rule('/logout','logout',logout)
app.add_url_rule('/Admin_dashboard','Admin_dashboard',Admin_dashboard, methods=['GET','POST'])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    