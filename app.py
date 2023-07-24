#Import necessary modules from Flask framework
from flask import Flask, render_template
import mysql.connector

#Initialize the Flask Application
app = Flask(__name__)

#Database connection configuration
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root'
        password='heartattack2023',
        database='Photography'
    )
    return conn

#Defining routes

#Home route
@app.route('/')
def home():
    return render_template('home.html')


#Route to serve static files- css files and images
app.route('/static/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)


#run the flask app
if __name__ == '__main__':
    app.run(port=5000)