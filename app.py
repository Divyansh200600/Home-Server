from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, PasswordField
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.validators import InputRequired
from flask import Flask, render_template

import os

app = Flask(__name__)

app.secret_key = 'your_secret_key'

app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/mf')
def media_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('mf.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return redirect('/mf')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@app.route('/delete/<filename>')
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect('/mf')




# Store notifications in a list for demonstration purposes
notifications = []

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/static/images/<filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == '1234':
            session['logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Try again.', 'error')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logout successful!', 'info')
    return redirect(url_for('login'))

@app.route('/index')
def index():
    if 'logged_in' in session and session['logged_in']:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return render_template('index.html', files=files, notifications=notifications)
    else:
        return redirect(url_for('login'))

@app.route('/db')
def db_page():
    # Add logic for your db page here
    return render_template('db.html', notifications=notifications)

@app.route('/profile')
def profile():
    # Add logic for your db page here
    return render_template('profile.html', notifications=notifications)

@app.route('/setting')
def setting():
    # Add logic for your db page here
    return render_template('setting.html', notifications=notifications)


@app.route('/mf')
def mf():
    return render_template('mf.html', notifications=notifications)



@app.route('/wishes_center')
def wishes_center():
    return render_template('wishes_center.html', notifications=notifications)

@app.route('/add_news', methods=['POST'])
def add_news():
    if request.method == 'POST':
        news_text = request.form.get('news_text')
        if news_text:
            notifications.append(f"📣 Admin added news: {news_text}")
            flash('News added successfully!', 'success')
    return redirect(url_for('index'))  # Redirect to the wishes center page after adding news



if __name__ == '__main__':

        app.run(host='0.0.0.0', port=5000, debug=True)
    