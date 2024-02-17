from flask import render_template,request,redirect,url_for,session, flash,jsonify
import requests
from datetime import datetime


#-----------------------------------------------Common to both admin and user---------------------------------------------------
def Home():
    return render_template('Login Page.html')

def User_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_api = f'http://localhost:5000/user/username/{username}'
        response = requests.get(user_api)
        if response.status_code == 200:
            # Parse the JSON data
            user_info = response.json()

            # Check if the provided password matches the stored password
            if 'password' in user_info and user_info['password'] == password:
                session['username'] = user_info['Username']
                return redirect(url_for('user_dashboard', user_id=user_info['id']))
            else:
                return "Invalid username or password"
        else:
            # Print an error message if the request was not successful
            return f"Error: {response.status_code}"
    return render_template('User login.html')



def Registration():
    return render_template('registration.html')

def user_dashboard(user_id):
    username = session.get('username')
    print(username)
    if username:
        return render_template('User dashboard.html')
    else:
        return redirect(url_for('Home'))

def logout():
    session.clear()
    return redirect(url_for('Home'))


#----------------------------------------------------Admin Area-----------------------------------------------------------------
def Admin_login():
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')

        if password=="password" and username=="Admin":
            return redirect(url_for('Admin_dashboard'))
        else:
            return "Invalid username or password"
    return render_template('Admin login.html')


def Admin_dashboard():
    return render_template('Admin dashboard.html')


def Section():
    Book_section_get_all = 'http://127.0.0.1:5000/book_sections/all'
    response = requests.get(Book_section_get_all)

    if response.status_code == 200:
        sections = response.json()
        for section in sections:
            section['date_created'] = datetime.strptime(section['date_created'][:-7], '%Y-%m-%d %H:%M:%S')
    else:
        sections = []

    return render_template('Section.html', sections=sections)


def Admin_add_section():
    if request.method == 'POST':
        section_name = request.form.get('section_name')
        section_description = request.form.get('section_description')
        data = {
            'sec_name': section_name,
            'description': section_description
        }
        api_url = 'http://127.0.0.1:5000/book_sections'
        response = requests.post(api_url, json=data)
        success = response
        flash('success' if success else 'danger')
        if success:
            return redirect(url_for('Section'))
    return render_template('add Section.html')

def Admin_edit_section(sec_id):
    if request.method == 'POST':
        section_name = request.form.get('section_name')
        section_description = request.form.get('section_description')
        data = {
            'sec_name': section_name,
            'description': section_description
        }
        api_url = f'http://127.0.0.1:5000/book_sections/{sec_id}'
        response = requests.put(api_url, json=data)
        success = response.status_code == 200
        flash('success' if success else 'danger')
        if success:
            return redirect(url_for('Section'))
        else:
            return redirect(url_for('Admin_dashboard'))
    else:
        section_details_url = f'http://127.0.0.1:5000/book_sections/{sec_id}'
        response = requests.get(section_details_url)

        if response.status_code == 200:
            section = response.json()
            return render_template('edit section.html', section=section)
        return  redirect(url_for('Section'))

def Admin_delete_section(sec_id):
    if request.method == 'POST':
        section_details_url = f'http://127.0.0.1:5000/book_sections/{sec_id}'
        requests.delete(section_details_url)
        return redirect(url_for('Section'))
    return redirect(url_for('Section'))

def Books():
    sec_id = request.args.get('section_id')
    sec_name = request.args.get('section_name')
    Book_get_all = f'http://127.0.0.1:5000/books/all?section_id={sec_id}'
    response = requests.get(Book_get_all)

    if response.status_code == 200:
        books = response.json()
    else:
        books = []
    return render_template('books.html', books=books, sec_id=sec_id,sec_name=sec_name)