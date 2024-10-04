
from flask import Flask ,render_template,redirect,url_for,request
import os
import mysql.connector

print(os.getcwd())
# Create a Flask application object
app = Flask(__name__)

# Mysql databse connection
def my_connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',  # replace with your MySQL username
        password='1106@MySql',  # replace with your MySQL password
        database='my_flask_app'  # replace with your database name
    )

# Home page route ("/")
@app.route('/')     # this will redirect to http://127.0.0.1:5000

def home():
    # return "Welcome to home page"
    # return render_template('index.html')    ## Renders the index.html file from the templates folder    
    connection = my_connect_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users')           # fetching all the data which is there in MySql table
    user_data = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', data=user_data)        # we are passing the data to index.html

@app.route('/about')        # this will redirect to http://127.0.0.1:5000/about

def about():
    # return "This is about page"
    return render_template('about.html')    ## Renders the about.html file from the templates folder

@app.route('/submit', methods=['POST'])  # Accepts only POST requests

def submit():

    # Retrieve data from the submitted form
    name = request.form.get('name')  # Get the name from the form
    age = request.form.get('age')      # Get the age from the form
    location = request.form.get('location')  # Get the location from the form

    # Validate age
    if int(age) <= 0:
        error_message = "Age must be greater than 0."
        cursor.execute('SELECT * FROM users')  # Fetch user data to display on the page
        user_data = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('index.html', error=error_message, data=user_data)
    
    # Check if any of the fields are None or empty
    if not name or not age or not location:
        return "Error: All fields are required!", 400  # Return an error response if any field is empty


    connection = my_connect_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('INSERT INTO users (name, age, location) VALUES (%s, %s, %s)', (name, age, location))
    # User_data = cursor.fetchall()
    connection.commit()  # Commit the changes
    cursor.close()
    connection.close()
    return redirect(url_for('home'))  # Redirect to home after submission


# Edit User route
@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    connection = my_connect_db()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        location = request.form['location']
        
        cursor.execute('UPDATE users SET name=%s, age=%s, location=%s WHERE id=%s', (name, age, location, user_id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('home'))

    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit.html', user=user)

# Delete User route
@app.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    connection = my_connect_db()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('home'))


# Start the Flask development server
if __name__ == '__main__':
    app.run(debug=True)     #, port=8080)