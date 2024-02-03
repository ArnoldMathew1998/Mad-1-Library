from flask import render_template
import base64

def Home():
    return render_template('Login Page.html')

def User_login():
    return render_template('User login.html')

def Admin_login():
    return render_template('Admin login.html')

def Registration():
    return render_template('registration.html')