#Import necessary modules from Flask framework
from flask import Flask, render_template,request, url_for, redirect
import mysql.connector
from PIL import Image

#Initialize the Flask Application
app = Flask(__name__)

# Set the maximum upload size to 16 MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


#Database connection configuration
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='heartattack2023',
        database='Photography'
    )
    return conn

#Defining routes

#Route to serve static files- css files and images
app.route('/static/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)

#Home route
@app.route('/')
def home():
    return render_template('home.html')

#Route for image upload
@app.route('/upload', methods =['POST', 'GET'])
def image_upload():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Retrieve the student information from the database
    query = "SELECT * FROM  Category"
    cursor.execute(query)
    categories = cursor.fetchall()
    conn.close()

    if request.method == 'POST':
        photo = request.files['image']
        caption = request.form['caption']
        category_id = int(request.form.get('category'))

        #save the image
        photo_path = 'static/Images/' + photo.filename
        photo.save(photo_path)

        #Get profile picture filename to be stored in the database
        filename = photo.filename

        #Database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        #Insert the new image to database
        insert_query = "INSERT INTO Image (filename, caption, category_id) VALUES(%s, %s, %s)"
        cursor.execute(insert_query, (filename, caption, category_id))
        conn.commit()
        conn.close()

        success = "Image uploaded successfully"

        return render_template('upload.html', success=success, categories=categories)   
    
    else:
        return render_template('upload.html', categories=categories)




#run the flask app
if __name__ == '__main__':
    app.run(port=5000)