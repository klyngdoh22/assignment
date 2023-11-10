from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import sqlite3
from db_setup import init_db

app = Flask(__name__)

# Configure the upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.before_first_request
def initialize_database():
    init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/formpage')
def formpage():
    return render_template('formpage.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/add_project', methods=['POST'])
def add_project():
    title = request.form['title']
    description = request.form['description']
    image = request.files['image']

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_file_name = filename
    else:
        return "File not allowed", 400

    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO projects (Title, Description, ImageFileName)
        VALUES (?, ?, ?)
    ''', (title, description, image_file_name))

    conn.commit()
    conn.close()

    return redirect(url_for('projects'))

@app.route('/projects')
def projects():
    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM projects')
    projects = cursor.fetchall()

    conn.close()

    return render_template('projects.html', projects=projects)

# Add other routes and functions as needed

if __name__ == '__main__':
    app.run(debug=True)
