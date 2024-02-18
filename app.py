from flask import Flask, session
from flask_restful import Api
from Database.models import db
from API.Book_section import Book_section_api
from API.Book import Book_api
from API.Image import Image_api
from API.User import User_id, User_Mail_id, User_Username
from API.User_log import User_log_api
import Controller.login

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)
app.config['SECRET_KEY'] = 'Mad-1-project'
link=Controller.login


#----------------------------------------------Add resources to the API--------------------------------------------------------
api.add_resource(Book_api, '/Api/Book', '/Api/Book/<int:book_id>','/Api/Book/All')
api.add_resource(Book_section_api, '/Api/Sections', '/Api/Sections/<int:sec_id>','/Api/Sections/All')

api.add_resource(User_log_api, '/user_logs/<int:user_id>/<int:book_id>', '/user_logs')

api.add_resource(User_id, '/user/id', '/users/id/<int:user_id>')
api.add_resource(User_Mail_id, '/user/mail/<string:mail_id>')
api.add_resource(User_Username, '/user/username/<string:username>')

api.add_resource(Image_api, '/images', '/images/<int:image_id>')



#-------------------------------------------------Routes for web pages-----------------------------------------------------------

app.add_url_rule('/', 'Home', link.Home)
app.add_url_rule('/login', 'User_login', link.User_login, methods=['GET','POST'])

app.add_url_rule('/Registration', 'Registration', link.Registration)
app.add_url_rule('/user_dashboard/<int:user_id>','user_dashboard',link.user_dashboard)
app.add_url_rule('/logout','logout',link.logout)

# Admin routes for web page
app.add_url_rule('/Admin/login', 'Admin_login', link.Admin_login, methods=['GET','POST'])
app.add_url_rule('/Admin/login/dashboard','Admin_dashboard',link.Admin_dashboard, methods=['GET','POST'])
# Section -----view_Add_Edit_Delete
app.add_url_rule('/Admin/login/dashboard/Section','Section',link.Section)
app.add_url_rule('/Admin/login/dashboard/Section/Add','Admin_add_section',link.Admin_add_section, methods=['GET','POST'])
app.add_url_rule('/Admin/login/dashboard/Section/Edit/<int:sec_id>','Admin_edit_section',link.Admin_edit_section, methods=['GET','POST'])
app.add_url_rule('/Admin/login/dashboard/Section/Delete/<int:sec_id>','Admin_delete_section',link.Admin_delete_section, methods=['POST'])
# Books--------view_Add_Edit_Delete
app.add_url_rule('/Admin/login/dashboard/book','book',link.Books)
app.add_url_rule('/Admin/login/dashboard/book/Add','Admin_add_book',link.Admin_add_book, methods=['GET','POST'])
app.add_url_rule('/Admin/login/dashboard/book/Edit/<int:book_id>','Admin_Edit_book',link.Admin_Edit_book, methods=['GET','POST'])
app.add_url_rule('/Admin/login/dashboard/book/Delete/<int:book_id>','Admin_Delete_book',link.Admin_Delete_book, methods=['POST'])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    