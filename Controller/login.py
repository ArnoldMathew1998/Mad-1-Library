from flask import render_template,request,redirect,url_for,session
import requests

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

def Admin_login():
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')

        if password=="password" and username=="Admin":
            return redirect(url_for('Admin_dashboard'))
        else:
            return "Invalid username or password"
    return render_template('Admin login.html')

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

def Admin_dashboard():
    return render_template('Admin dashboard.html')
    