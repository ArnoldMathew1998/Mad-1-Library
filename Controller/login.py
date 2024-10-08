from flask import render_template,request,redirect,url_for,session
from datetime import datetime,timedelta
import pycountry
from werkzeug.utils import secure_filename
import base64
import requests
import pandas as pd
import plotly.express as px
#-----------------------------------------------Common to both admin and user---------------------------------------------------
def Home():
    return render_template('Login Page.html')

def Section():
    Book_section_get_all = f'http://127.0.0.1:5000/Api/Sections/All/'
    response = requests.get(Book_section_get_all)
    session['sec_id'] = None
    session['section_name'] = None
    if response.status_code == 200:
        sections = response.json()
        for section in sections:
            section['date_created'] = datetime.strptime(section['date_created'][:-7], '%Y-%m-%d %H:%M:%S')
    else:
        sections = []

    return render_template('Section.html', sections=sections,User=session['user_id'])

def Books():
    sec_id = request.args.get('section_id')
    sec_name = request.args.get('section_name')
    if sec_id is not None and sec_name is not None:
        session['sec_id'] = sec_id
        session['section_name'] = sec_name
    Book_get_all = f'http://127.0.0.1:5000/Api/Book/All/?sec_id={session['sec_id']}'
    response = requests.get(Book_get_all)
    if response.status_code == 200:
        books = response.json()
    else:
        books = []
    return render_template('books.html', books=books, sec_id=session['sec_id'],sec_name=session['section_name'],User=session['user_id'])


def logout():
    session.clear()
    return redirect(url_for('Home'))

def Book_details(book_id):
    Book_get = f'http://127.0.0.1:5000/Api/Book/{book_id}/'
    Image_get = f'http://127.0.0.1:5000/Api/images/bi/{book_id}/'

    response_book = requests.get(Book_get)
    if response_book.status_code == 200:
        book = response_book.json()
    else:
        book = {}

    response_image = requests.get(Image_get)
    if response_image.status_code == 200:
        image_data = response_image.json().get('image_data')
    else:
        image_data = None

    return render_template('book details.html', book=book, image_data=image_data,User=session['user_id'])


#----------------------------------------------------Admin Area-----------------------------------------------------------------
def Admin_login():
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')

        if password=="password" and username=="Admin":
            session['user_id']=None
            session['admin']=True
            return redirect(url_for('Admin_dashboard'))
        else:
            return "Invalid username or password"
    return render_template('Admin login.html')


def Admin_dashboard():
    if session.get('admin')==True:
        if request.method == 'POST':
            Search = request.form.get('SearchTerm')
            SearchType = request.form.get('SearchType')
            if SearchType == 'Book_Name':
                Book_get_all = f'http://127.0.0.1:5000/Api/Book/All/?book_name={Search}'
            elif SearchType == 'Author':
                Book_get_all = f'http://127.0.0.1:5000/Api/Book/All/?author_name={Search}'
            elif SearchType == 'Year':
                Book_get_all = f'http://127.0.0.1:5000/Api/Book/All/?year={Search}'
            elif SearchType == 'Section_ID':
                Book_get_all = f'http://127.0.0.1:5000/Api/Book/All/?sec_id={Search}'
            elif SearchType == 'Language':
                Book_get_all = f'http://127.0.0.1:5000/Api/Book/All/?language={Search}'
            elif SearchType == 'Content':
                Book_get_all = f'http://127.0.0.1:5000/Api/Book/All/?content={Search}'
            else:
                Book_get_all = f'http://127.0.0.1:5000/Api/Book/All/'

            response = requests.get(Book_get_all)
            if response.status_code == 200:
                print('Book_Name')
                books = response.json()
            else:
                books = []
            return render_template('Admin dashboard.html', books=books)
        return render_template('Admin dashboard.html', books=[])
    else:
        return redirect(url_for('Home'))


def Admin_add_section():
    if session.get('admin')==True:
        if request.method == 'POST':
            section_name = request.form.get('section_name')
            section_description = request.form.get('section_description')
            data = {
                'sec_name': section_name,
                'description': section_description
            }
            Book_section_get_all = f'http://127.0.0.1:5000/Api/Sections/'
            requests.post(Book_section_get_all, json=data)
            return redirect(url_for('Section'))
        return render_template('add Section.html')

def Admin_edit_section(sec_id):
    if session.get('admin')==True:
        if request.method == 'POST':
            section_name = request.form.get('section_name')
            section_description = request.form.get('section_description')
            data = {
                'sec_name': section_name,
                'description': section_description
            }
            api_url = f'http://127.0.0.1:5000/Api/Sections/{sec_id}/'
            response = requests.put(api_url, json=data)
            return redirect(url_for('Section'))
        else:
            section_details_url = f'http://127.0.0.1:5000/Api/Sections/{sec_id}/'
            response = requests.get(section_details_url)

            if response.status_code == 200:
                section = response.json()
                return render_template('edit section.html', section=section)
            return  redirect(url_for('Section'))

def Admin_delete_section(sec_id):
    if session.get('admin')==True:
        if request.method == 'POST':
            section_details_url = f'http://127.0.0.1:5000/Api/Sections/{sec_id}/'
            requests.delete(section_details_url)
            return redirect(url_for('Section'))
        



def upload_image(book_id, book_image,sec_id):
    if session.get('admin')==True:
        pic = book_image
        if not pic:
            return 'No pic uploaded', 400

        image_data_base64 = base64.b64encode(pic.read()).decode('utf-8')

        image_api_url = f'http://127.0.0.1:5000/Api/images/{book_id}/{sec_id}/'  
        image_api_data = {
            'image_data': image_data_base64,
            'book_id': book_id
        }

        response = requests.post(image_api_url, json=image_api_data)

        if response.status_code == 201:
            print('Image updated successfully')
            print(response.json())
            return 'Image has been updated', 200
        else:
            print('Image update failed')
            print(response.text)
            return 'Image update failed', 500

def edit_image(book_id, image_data):
    if session.get('admin')==True:
        pic = image_data
        if not pic:
            return 'No pic', 400

        image_data_base64 = base64.b64encode(pic.read()).decode('utf-8')

        image_api_url = f'http://127.0.0.1:5000/Api/images/bi/{book_id}/' 
        image_api_data = {
            'image_data': image_data_base64,
        }

        response = requests.put(image_api_url, json=image_api_data)

        if response.status_code == 201:
            print('Image uploaded successfully')
            print(response.json())
            return 'Image has been uploaded', 200
        else:
            print('Image upload failed')
            print(response.text)
            return 'Image upload failed', 500
            


def Admin_add_book():
    if session.get('admin')==True:
        if request.method == 'POST':
            sec_id = int(session.get('sec_id'))
            book_name = request.form.get('book_name')
            author_name = request.form.get('author_name')
            date_issued = request.form.get('date_issued')
            language = request.form.get('language')
            Content = request.form.get('Content')

            book_data = {
                'book_name': book_name,
                'author_name': author_name,
                'date_issued': date_issued,
                'content': Content,
                'language': language,
                'sec_id': sec_id
            }

            Books_url = 'http://127.0.0.1:5000/Api/Book/'

            book_response = requests.post(Books_url, json=book_data)

            if book_response.status_code == 201:
                book_id = book_response.json()['book_id']
                book_image = request.files.get('book_image')
                
                secure_filename(book_image.filename)
                upload_image(book_id, book_image,sec_id)
                return redirect(url_for('book'))

        else:
            all_languages = list(pycountry.languages)
            language_names = [lang.name for lang in all_languages]
            return render_template('add book.html', languages=language_names)

    

def Admin_Edit_book(book_id):
    if session.get('admin')==True:
        if request.method == 'POST':
            book_name = request.form.get('book_name')
            author_name = request.form.get('author_name')
            date_issued = request.form.get('date_issued')
            language = request.form.get('language')
            Content = request.form.get('Content')

            edit_book_url = f'http://127.0.0.1:5000/Api/Book/{book_id}/'
            
        
            data = {
                'book_name': book_name,
                'author_name': author_name,
                'date_issued': date_issued,
                'content': Content,
                'language': language,
                'sec_id': session.get('sec_id')
            }
    
            requests.put(edit_book_url, json=data)
            
            book_image = request.files.get('book_image')
            secure_filename(book_image.filename)
            edit_image(book_id, book_image)
            return redirect(url_for('book'))

        
        else:
            get_book_url = f'http://127.0.0.1:5000/Api/Book/{book_id}/'
            response = requests.get(get_book_url)

            if response.status_code == 200:
                book_details = response.json()
                all_languages = list(pycountry.languages)
                language_names = [lang.name for lang in all_languages]
                return render_template('edit book.html', book=book_details, languages=language_names)
            else:
                return redirect(url_for('book'))

    
def Admin_Delete_book(book_id):
    if session.get('admin')==True:
        if request.method == 'POST':
            delete_book_url = f'http://127.0.0.1:5000/Api/Book/{book_id}/'
            requests.delete(delete_book_url)
            return redirect(url_for('book'))
    
def Admin_User_revoke():
    if session.get('admin')==True:
        if request.method == 'POST':
            user_id = request.args.get('user_id')
            book_id= request.args.get('book_id')
            delete_userlog_url = f'http://127.0.0.1:5000/Api/user/logs/{user_id}/{book_id}/'
            requests.delete(delete_userlog_url)
            return redirect(url_for('Admin_User_revoke'))
        else:
            user_log_url = f'http://127.0.0.1:5000/Api/user/logs/'
            response = requests.get(user_log_url)
            orders=[]
            user_logs = []
            if response.status_code == 200:
                user_logs = response.json()

            for user_log in user_logs:
                user_id=user_log['user_id']
                book_id=user_log['book_id']
                book_url = f'http://127.0.0.1:5000/Api/Book/{book_id}/'
                user_url = f'http://127.0.0.1:5000/Api/user/{user_id}/'
                book_response=requests.get(book_url)
                user_response=requests.get(user_url)
                book=book_response.json()
                user=user_response.json()
                orders.append({'user_id':user_log['user_id'],'user_name':user['Username'],'book_id':user_log['book_id'],'book_name':book['book_name'],'borrowed_date':user_log['borrow_date'],'return_date':user_log['return_date']})
            book_count=0
            user_count=0
            Book_get_all = 'http://127.0.0.1:5000/Api/Book/All/'
            user_get_all= 'http://127.0.0.1:5000/Api/user/'
            Book_get_response= requests.get(Book_get_all)
            user_get_response=requests.get(user_get_all)
            Books=Book_get_response.json()
            users=user_get_response.json()
            for book in Books:
                book_count+=1
            for user in users:
                user_count+=1
            return render_template("orders.html",orders=orders, user_count=user_count, book_count=book_count)

def Admin_overview():
    if session.get('admin')==True:
        user_logs=[{'user_id': 0, 'book_id': 0, 'borrow_date': 0, 'return_date': 0}]
        book_count=0
        user_count=0
        Book_get_all = 'http://127.0.0.1:5000/Api/Book/All/'
        user_get_all= 'http://127.0.0.1:5000/Api/user/'
        user_log_all= 'http://127.0.0.1:5000/Api/user/logs/'
        Book_get_response= requests.get(Book_get_all)
        user_get_response=requests.get(user_get_all)
        user_log_response=requests.get(user_log_all)
        
        Books=Book_get_response.json()
        users=user_get_response.json()
        graph_html="No User log"
        if user_log_response.status_code == 200:
            user_logs=user_log_response.json()
            user_logs_df = pd.DataFrame(user_logs)
            fig = px.pie(user_logs_df, names='user_id', title='User Distribution by Books Brought')
            graph_html = fig.to_html(full_html=False)
        for book in Books:
            book_count+=1
        for user in users:
            user_count+=1
        return render_template('piechart.html',user_count=user_count, book_count=book_count, graph_html=graph_html)
#----------------------------------------------------User Area-----------------------------------------------------------------

def Registration():
    if request.method == 'POST':
        First_name = request.form.get('First_name')
        Middle_name = request.form.get('Middle_name')
        Last_name = request.form.get('Last_name')
        mail_id = request.form.get('mail_id')
        Username = request.form.get('Username')
        password = request.form.get('password')
        User_data = {
            'First_name': First_name,
            'Middle_name': Middle_name,
            'Last_name': Last_name,
            'Username': Username,
            'password': password,
            'mail_id': mail_id
        }

        User_url = 'http://127.0.0.1:5000/Api/user/'
        User_response = requests.post(User_url, json=User_data)

        if User_response.status_code == 201:
            user_id = User_response.json()['user_id']
            session["Username"]=Username
            session['user_id']=user_id
            return redirect(url_for('user_dashboard'))
    return render_template('registration.html')

def user_dashboard():
    if session['user_id'] and request.method == 'POST':
        Search = request.form.get('SearchTerm')
        SearchType = request.form.get('SearchType') 
        if SearchType == 'Book_Name':
            Book_get_all = f'http://127.0.0.1:5000/Api/Book/All/?book_name={Search}'
        elif SearchType == 'Author':
            Book_get_all = f'http://127.0.0.1:5000/Api/Book/All/?author_name={Search}'
        elif SearchType == 'Year':
            Book_get_all = f'http://127.0.0.1:5000/Api/Book/All/?year={Search}'
        elif SearchType == 'Section_ID':
            Book_get_all = f'http://127.0.0.1:5000/Api/Book/All/?sec_id={Search}'
        elif SearchType == 'Language':
            Book_get_all = f'http://127.0.0.1:5000/Api/Book/All/?language={Search}'
        elif SearchType == 'Content':
            Book_get_all = f'http://127.0.0.1:5000/Api/Book/All/?content={Search}'
        else:
            Book_get_all = f'http://127.0.0.1:5000/Api/Book/All/'

        response = requests.get(Book_get_all)
        if response.status_code == 200:
            print('Book_Name')
            books = response.json()
        else:
            books = []
        return render_template('User dashboard.html', books=books)
    if session['user_id'] and request.method == 'GET':
        return render_template('User dashboard.html')
    else:
        return redirect(url_for('Home'))


def User_login():
    if request.method == 'POST':
        Username = request.form.get('Username')
        password = request.form.get('password')
        user_api = f'http://127.0.0.1:5000/Api/user/{Username}/'
        response = requests.get(user_api)
        
        if response.status_code == 200:
            user_info = response.json()
            if 'password' in user_info and user_info['password'] == password:
                session['Username'] = user_info['Username']
                session['user_id'] = user_info['user_id']
                return redirect(url_for('user_dashboard'))
            else:
                return "Invalid username or password"
        elif response.status_code == 404:
            return "User not found"
    return render_template('User login.html')

def User_request_book():
    if request.method == 'GET':
        book_id = request.args.get('book_id')
        Book_get = f'http://127.0.0.1:5000/Api/Book/{book_id}/'
        response_book = requests.get(Book_get)
        current_datetime = datetime.now().strftime('%Y-%m-%dT%H:%M')
        future_datetime = (datetime.now() + timedelta(minutes=3)).strftime('%Y-%m-%dT%H:%M')
        if response_book.status_code == 200:
            book = response_book.json()
            book_name = book.get('book_name')  
        else:
            book_name = "Book not found"
        return render_template('request book.html', book_id=book_id, book_name=book_name,current_datetime=current_datetime,future_datetime=future_datetime)

    elif request.method == 'POST':
        borrow_date = datetime.now().strftime('%Y-%m-%dT%H:%M')
        return_date = request.form.get('return_date')
        user_log_url = 'http://127.0.0.1:5000/Api/user/logs/'
        user_log = {
            'user_id': session.get('user_id'),  
            'book_id': request.args.get('book_id'),
            'borrow_date':borrow_date,
            'return_date': return_date
        }
        response = requests.post(user_log_url, json=user_log)
        if response.status_code == 201:
            return redirect(url_for('user_dashboard'))
        else:
            return f"Error: {response.status_code}"

def User_My_Books():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))  

    user_log_url = f'http://127.0.0.1:5000/Api/user/logs/{user_id}/'
    user_log_response = requests.get(user_log_url)

    books = []
    book_ids=[]

    if user_log_response.status_code == 200:
        user_log_data = user_log_response.json()
        book_ids = [book_id['book_id'] for book_id in user_log_data]

    for book_id in book_ids:
        book_url = f'http://127.0.0.1:5000/Api/Book/{book_id}/'
        book_response = requests.get(book_url)
        if book_response.status_code == 200:
            book = book_response.json()
            books.append(book)
        
    return render_template('My books.html', books=books)
