from flask import Flask,request,render_template
from models import db
import base64

#-----------------------------------------------initialisation-----------------------------------------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


#----------------------------------------LOGIN LINKS & REGISTRATION LINKS-------------------------------------------
@app.route('/')
def Home():
    return render_template('Login Page.html')

@app.route('/User_login')
def User_login():
    return render_template('User login.html')

@app.route('/Admin_login')
def Admin_login():
    return render_template('Admin login.html')

@app.route('/Registration')
def Registration():
    return render_template('registration.html')
#--------------------------------------------------END----------------------------------------------------------------


if __name__ == '__main__':
    # Create the database and tables
    with app.app_context():
        db.create_all()

    # Run the Flask application
    app.run(debug=True)
    