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

#Method to get categories information from db
def category():

    #Get database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # Retrieve the Category information from the database
    cursor.execute('SELECT * FROM Category')
    categories = cursor.fetchall()
    conn.close()

    return categories


#Defining routes

#Route to serve static files- css files and images
@app.route('/static/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)

#Home route
@app.route('/')
def home():
    #fetch categories
    categories = category()

    return render_template('home.html', categories=categories)

# Route to add a new category
@app.route('/add_category', methods=['POST', 'GET'])
def add_category():
    if request.method == 'POST':
        new_category = request.form['category_name']

        # Get Database Connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the category exists
        categories = category()

        # First, assume the category doesn't exist
        category_exists = False

        for cat in categories:
            if cat[1] == new_category:
                category_exists = True
                error = 'Category already exists'
                break  # Exit the loop if the category is found

        if category_exists:
            conn.close()
            return redirect(url_for('add_category', error=error))
        else:
            add_category_query = "INSERT INTO Category (name) VALUES(%s)"
            cursor.execute(add_category_query, (new_category,))
            conn.commit()
            conn.close()
            message = "Category Added!"
            return redirect(url_for('add_category', message=message))
    else:
        return render_template('add_category.html')

#Route for image upload
@app.route('/upload', methods =['POST', 'GET'])
def image_upload():
    #categories
    categories = category()

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

#Route to display photos
@app.route('/gallery/<int:category_id>')
def gallery(category_id):

    #categories
    categories = category()
    
    #Get Database Connection
    conn = get_db_connection()
    cursor = conn.cursor()

    #Execute image query from specific category
    images_query= "SELECT * FROM Image WHERE category_id = %s" 
    cursor.execute(images_query, (category_id,))
    images = cursor.fetchall()
    category_name_query = "SELECT * FROM Category WHERE id = %s"
    cursor.execute(category_name_query, (category_id,))
    category_name = cursor.fetchone()
    conn.close()

    return render_template('gallery.html', images=images, categories=categories, category_name=category_name)

#Admin routes

#Admin login route
@app.route('/admin', methods=['POST', 'GET'])
def admin_login():
    if request.method == 'POST':
        #Admin credentials
        name = 'kelvin'
        passw = '12345'

        #Inputs from login form

        username = request.form['username']
        password = request.form['password']

        #Check if login credentials are correct

        if name == username and passw == password:
            return redirect(url_for('admin_dashboard'))
        else:
            error = "Invalid credentials!"
            return render_template('admin_login.html', error=error)
        
    else:
        return render_template('admin_login.html')
    
#Admin dashboard
@app.route('/admin_dashboard', methods=['POST', 'GET'])
def admin_dashboard():
    return render_template('admin_dashboard.html')



#run the flask app
if __name__ == '__main__':
    app.run( host="0.0.0.0", port=5000)