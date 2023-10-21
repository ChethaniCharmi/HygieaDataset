import os
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import tensorflow as tf
from tensorflow import keras
from werkzeug.utils import secure_filename
import numpy as np

app = Flask(__name__)
app.secret_key = 'demo'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ch@rmi444'
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)

# Loading Trained Model
model = keras.models.load_model('modelClassification.h5')

# Preprocessing the image
def preprocess_input(image_path):
    image = tf.keras.preprocessing.image.load_img(image_path, target_size=(150, 150))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = image / 255.0
    image = tf.expand_dims(image, axis=0)
    return image

# Define class labels
class_labels = ["Covid-19", "Normal", "Pneumonia", "Tuberculosis"]

# Define route for HTML page
@app.route('/')
def home():
    session.clear()
    return render_template("login.html")


@app.route('/login', methods=['GET','POST'])
def login():
    #message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM login WHERE email = %s AND password = %s', (email,password)) 
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['email'] = user['email']
            flash('Logged in successfully', 'success')
            return redirect(url_for('prediction'))
        else:
            flash('Please enter correct email or password', 'error')
            return render_template('login.html')


@app.route('/register')
def register():
    return render_template("register.html")  

@app.route('/registerAction', methods=['POST'])
def register_action():
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    contact = request.form['contact']
    password = request.form['password']

    # Check if the username already exists in the registration database
    existing_user = UserRegister.query.filter_by(fname=fname).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'})

    # Create a new user and add it to the registration database
    new_user = UserRegister(fname=fname, lname=lname, email=email,contact=contact,password=password)
    db_register.session.add(new_user)
    db_register.session.commit()

    return jsonify({'message': 'User registered successfully'})


@app.route('/prediction')
def prediction():
    return render_template("prediction.html") 

# Define route for prediction handling
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)

        processed_input = preprocess_input(file_path)

        # Getting predictions from the model
        predictions = model.predict(processed_input)

        # Find the index (class) with the highest probability
        predicted_index = int(np.argmax(predictions))

        # Get the predicted class label
        predicted_class = class_labels[predicted_index]

        # Interpret the results
        prediction_results = {
            'predictions': predictions.tolist(),
            'predicted_class': predicted_class
        }

        # Returning prediction as a JSON response
        return jsonify(prediction_results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
