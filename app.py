from flask import Flask, session
from flask_restful import Api
from Database.models import db
from API.Book_section import Book_section_api
from API.Book import Book_api
from API.Image import Image_api
from API.User import User_id, User_Mail_id, User_Username
from API.User_log import User_log_api
import Controller.login

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)
app.config['SECRET_KEY'] = 'Mad-1-project'
link=Controller.login

#----------------------------------------------Add resources to the API--------------------------------------------------------
api.add_resource(Book_api, '/books', '/books/<int:book_id>','/books/all')

api.add_resource(Book_section_api, '/book_sections', '/book_sections/<int:sec_id>','/book_sections/all')
api.add_resource(User_log_api, '/user_logs/<int:user_id>/<int:book_id>', '/user_logs')

api.add_resource(User_id, '/user/id', '/users/id/<int:user_id>')
api.add_resource(User_Mail_id, '/user/mail/<string:mail_id>')
api.add_resource(User_Username, '/user/username/<string:username>')

api.add_resource(Image_api, '/images', '/images/<int:image_id>')



#-------------------------------------------------Routes for web pages-----------------------------------------------------------

app.add_url_rule('/', 'Home', link.Home)
app.add_url_rule('/User_login', 'User_login', link.User_login, methods=['GET','POST'])

app.add_url_rule('/Registration', 'Registration', link.Registration)
app.add_url_rule('/user_dashboard/<int:user_id>','user_dashboard',link.user_dashboard)
app.add_url_rule('/logout','logout',link.logout)

# Admin routes for web page
app.add_url_rule('/Admin_login', 'Admin_login', link.Admin_login)
app.add_url_rule('/Admin_dashboard','Admin_dashboard',link.Admin_dashboard, methods=['GET','POST'])
# Section -----view_Add_Edit_Delete
app.add_url_rule('/Section','Section',link.Section)
app.add_url_rule('/Section/Add','/Section/Add',link.Admin_add_section, methods=['GET','POST'])
app.add_url_rule('/Section/Edit/<int:sec_id>','/Section/edit/',link.Admin_edit_section, methods=['GET','POST'])
app.add_url_rule('/Section/Delete/<int:sec_id>','/Section/Delete/',link.Admin_delete_section, methods=['GET','POST'])
# Books--------view_Add_Edit_Delete
app.add_url_rule('/book','book',link.Books)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    