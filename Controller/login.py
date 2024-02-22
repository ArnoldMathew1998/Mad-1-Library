from flask import render_template,request,redirect,url_for,session, flash,jsonify
from datetime import datetime
import pycountry
from werkzeug.utils import secure_filename
import io
import base64
import requests
#-----------------------------------------------Common to both admin and user---------------------------------------------------
def Home():
    return render_template('Login Page.html')

def User_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_api = f'http://127.0.0.1:5000/user/username/{username}'
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
    if request.method == 'POST':
        Search = request.form.get('SearchTerm')
        SearchType = request.form.get('SearchType') # Use a different name for the radio button
        print(Search,SearchType)
        if SearchType == 'Book_Name':
            Book_get_all = f'http://127.0.0.1:5000/Api/Book/All?book_name={Search}'
        elif SearchType == 'Author':
            Book_get_all = f'http://127.0.0.1:5000/Api/Book/All?author_name={Search}'
        elif SearchType == 'Year':
            Book_get_all = f'http://127.0.0.1:5000/Api/Book/All?year={Search}'
        elif SearchType == 'Section_ID':
            Book_get_all = f'http://127.0.0.1:5000/Api/Book/All?sec_id={Search}'
        elif SearchType == 'Book_ID':
            Book_get_all = f'http://127.0.0.1:5000/Api/Book/{Search}'
        elif SearchType == 'Language':
            Book_get_all = f'http://127.0.0.1:5000/Api/Book/All?language={Search}'
        elif SearchType == 'Content':
            Book_get_all = f'http://127.0.0.1:5000/Api/Book/All?content={Search}'
        else:
            Book_get_all = f'http://127.0.0.1:5000/Api/Book/All'

        response = requests.get(Book_get_all)
        if response.status_code == 200:
            print('Book_Name')
            books = response.json()
        else:
            books = []
        return render_template('Admin dashboard.html', books=books)
    return render_template('Admin dashboard.html', books=[])


def Section():
    Book_section_get_all = f'http://127.0.0.1:5000/Api/Sections/All'
    response = requests.get(Book_section_get_all)
    session['sec_id'] = None
    session['section_name'] = None
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
        Book_section_get_all = f'http://127.0.0.1:5000/Api/Sections'
        requests.post(Book_section_get_all, json=data)
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
        api_url = f'http://127.0.0.1:5000/Api/Sections/{sec_id}'
        response = requests.put(api_url, json=data)
        return redirect(url_for('Section'))
    else:
        section_details_url = f'http://127.0.0.1:5000/Api/Sections/{sec_id}'
        response = requests.get(section_details_url)

        if response.status_code == 200:
            section = response.json()
            return render_template('edit section.html', section=section)
        return  redirect(url_for('Section'))

def Admin_delete_section(sec_id):
    if request.method == 'POST':
        section_details_url = f'http://127.0.0.1:5000/Api/Sections/{sec_id}'
        requests.delete(section_details_url)
        return redirect(url_for('Section'))
    
def Books():
    sec_id = request.args.get('section_id')
    sec_name = request.args.get('section_name')
    if sec_id is not None and sec_name is not None:
        session['sec_id'] = sec_id
        session['section_name'] = sec_name
    Book_get_all = f'http://127.0.0.1:5000/Api/Book/All?sec_id={session['sec_id']}'
    response = requests.get(Book_get_all)

    if response.status_code == 200:
        books = response.json()
    else:
        books = []
    return render_template('books.html', books=books, sec_id=session['sec_id'],sec_name=session['section_name'])


def upload_image(book_id, book_image,sec_id):
    pic = book_image
    if not pic:
        return 'No pic uploaded', 400

    image_data_base64 = base64.b64encode(pic.read()).decode('utf-8')

    image_api_url = f'http://127.0.0.1:5000/Api/images/{book_id}/{sec_id}'   # Update the URL with the correct address
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
    pic = image_data
    if not pic:
        return 'No pic', 400

    image_data_base64 = base64.b64encode(pic.read()).decode('utf-8')

    image_api_url = f'http://127.0.0.1:5000/Api/images/bi/{book_id}'  # Update the URL with the correct address
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

        Books_url = 'http://127.0.0.1:5000/Api/Book'

        # Make API request to add book
        book_response = requests.post(Books_url, json=book_data)

        if book_response.status_code == 201:
            # Successfully added Book, now get the book_id
            book_id = book_response.json()['book_id']

            # Get file data from request
            book_image = request.files.get('book_image')
            
            secure_filename(book_image.filename)
            
            # Upload image and pdf
            upload_image(book_id, book_image,sec_id)
            return redirect(url_for('book'))

    else:
        all_languages = list(pycountry.languages)
        language_names = [lang.name for lang in all_languages]
        return render_template('add book.html', languages=language_names)

    

def Admin_Edit_book(book_id):
    if request.method == 'POST':
        book_name = request.form.get('book_name')
        author_name = request.form.get('author_name')
        date_issued = request.form.get('date_issued')
        language = request.form.get('language')
        Content = request.form.get('Content')

        edit_book_url = f'http://127.0.0.1:5000/Api/Book/{book_id}'
        
       
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
        
        # Upload image and pdf
        edit_image(book_id, book_image)
        return redirect(url_for('book'))

    
    else:
        get_book_url = f'http://127.0.0.1:5000/Api/Book/{book_id}'
        response = requests.get(get_book_url)

        if response.status_code == 200:
            book_details = response.json()
            all_languages = list(pycountry.languages)
            language_names = [lang.name for lang in all_languages]
            return render_template('edit book.html', book=book_details, languages=language_names)
        else:
            return redirect(url_for('book'))

    
def Admin_Delete_book(book_id):
    if request.method == 'POST':
        delete_book_url = f'http://127.0.0.1:5000/Api/Book/{book_id}'
        requests.delete(delete_book_url)
        return redirect(url_for('book'))