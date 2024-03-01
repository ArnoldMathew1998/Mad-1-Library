from flask import Flask, session
from flask_restful import Api
from Database.models import db
from API.Book_section import Book_section_api
from API.Book import Book_api
from API.Image import Image_api
from API.User import User_id
from API.User_log import User_log_api
import Controller.login
import requests
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)
app.config['SECRET_KEY'] = 'Mad-1-project'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
link=Controller.login
scheduler = BackgroundScheduler()

def delete_User_log_auto():
    user_log_api = 'http://127.0.0.1:5000/Api/user/logs/'
    response = requests.delete(user_log_api)
    if response.status_code == 200:
        print("User auto delete")
    return

scheduler.add_job(delete_User_log_auto, 'interval', seconds=60)
scheduler.start()

#----------------------------------------------Add resources to the API--------------------------------------------------------
api.add_resource(Book_api, '/Api/Book/', '/Api/Book/<int:book_id>/','/Api/Book/All/')

api.add_resource(Book_section_api, '/Api/Sections/', '/Api/Sections/<int:sec_id>/','/Api/Sections/All/')

api.add_resource(Image_api, '/Api/images/', '/Api/images/bi/<int:book_id>/','/Api/images/<int:book_id>/<int:sec_id>/','/Api/images/si/<int:sec_id>/')

api.add_resource(User_id, '/Api/user/', '/Api/user/<int:user_id>/','/Api/user/<string:Username>/')

api.add_resource(User_log_api, '/Api/user/logs/<int:user_id>/<int:book_id>/', '/Api/user/logs/','/Api/user/logs/<int:user_id>/')







#-------------------------------------------------Routes for web pages-----------------------------------------------------------

app.add_url_rule('/', 'Home', link.Home)
app.add_url_rule('/login/', 'User_login', link.User_login, methods=['GET','POST'])
app.add_url_rule('/Registration/', 'Registration', link.Registration, methods=['GET','POST'])
app.add_url_rule('/user/dashboard/','user_dashboard',link.user_dashboard, methods=['GET','POST'])
app.add_url_rule('/logout/','logout',link.logout)
app.add_url_rule('/Admin/login/', 'Admin_login', link.Admin_login, methods=['GET','POST'])
app.add_url_rule('/Admin/login/dashboard/','Admin_dashboard',link.Admin_dashboard, methods=['GET','POST'])
app.add_url_rule('/login/dashboard/Section/','Section',link.Section)
app.add_url_rule('/Admin/login/dashboard/Section/Add/','Admin_add_section',link.Admin_add_section, methods=['GET','POST'])
app.add_url_rule('/Admin/login/dashboard/Section/Edit/<int:sec_id>/','Admin_edit_section',link.Admin_edit_section, methods=['GET','POST'])
app.add_url_rule('/Admin/login/dashboard/Section/Delete/<int:sec_id>/','Admin_delete_section',link.Admin_delete_section, methods=['POST'])
app.add_url_rule('/login/dashboard/book/','book',link.Books)
app.add_url_rule('/Admin/login/dashboard/book/Add/','Admin_add_book',link.Admin_add_book, methods=['GET','POST'])
app.add_url_rule('/Admin/login/dashboard/book/Edit/<int:book_id>/','Admin_Edit_book',link.Admin_Edit_book, methods=['GET','POST'])
app.add_url_rule('/Admin/login/dashboard/book/Delete/<int:book_id>/','Admin_Delete_book',link.Admin_Delete_book, methods=['POST'])
app.add_url_rule('/Admin/login/user/revoke','Admin_User_revoke',link.Admin_User_revoke, methods=['GET','POST'])
app.add_url_rule('/Admin/login/distribution','Admin_overview',link.Admin_overview)
app.add_url_rule('/login/dashboard/book/details/<int:book_id>/','Book_details',link.Book_details)
app.add_url_rule('/login/dashboard/book/buy/','User_request_book',link.User_request_book,methods=['GET','POST'])
app.add_url_rule('/login/dashboard/mybook/','User_My_Books',link.User_My_Books)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    