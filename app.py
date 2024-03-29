# Import necessary libraries
from flask import Flask, request, jsonify, render_template
import easyocr
import cv2
import io
import ssl
import re
import os
import numpy as np
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import FileField, SubmitField
import secrets
import base64
import streamlit as st
from PIL import Image
import pandas as pd
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import sqlite3

# Initialize Flask app
app = Flask(__name__, template_folder='/Users/jayaasri/Desktop/pro/templates')

csrf = CSRFProtect(app)
# Generate a secure secret key
app.config['SECRET_KEY'] = secrets.token_hex(16)  # Use an appropriate length for your application

# Create a Flask-WTF form
class ImageUploadForm(FlaskForm):
    image = FileField('Image')
    submit = SubmitField('Analyze Image')

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Disable SSL certificate verification for the EasyOCR model download
def disable_ssl_verification():
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

disable_ssl_verification()

@app.route('/home.html')
def cosmetic_analyze():
    return render_template('home.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

# Define your routes and functions
@app.route('/')
def index():
    form = ImageUploadForm()
    return render_template('CosmeticAnalyze.html', form=form, results=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return "No file part"
        
    file = request.files['image']

    if file.filename == '':
        return "No selected file"

    if file and allowed_file(file.filename):
        filename = "test2.jpeg"  # Set the desired filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "File uploaded successfully" 
        
    else:
        return "Invalid file type. Allowed extensions are png, jpg, jpeg, gif."

@app.route('/get_image_and_text', methods=['GET'])
def get_image_and_text():
    IMAGE_PATH = 'static/images/test2.jpeg'
    
    with open(IMAGE_PATH, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    reader = easyocr.Reader(['en'])
    results = reader.readtext(IMAGE_PATH, paragraph=False)
    
    # Convert results to a list of strings
    results_str = [result[1] for result in results]
    
    results_df = search_ingredients_in_dataset(results_str)
    matched_columns = []
    for col in results_df.columns:
        if results_df[col].any() == 1:
            matched_columns.append(col)
    return jsonify(results=results_str, matched_data=results_df.to_dict(orient='records'))

def search_ingredients_in_dataset(search_keywords): 
    df = pd.read_excel('Cosmeticsdataset.xlsx') 
    results_df = pd.DataFrame(columns=df.columns) 
    for keyword in search_keywords: 
        keyword = keyword.strip() 
        keyword_escaped = re.escape(keyword) 
        keyword_match = df[df['Ingredients'].str.contains(keyword_escaped, case=False, na=False)] 
        results_df = pd.concat([results_df, keyword_match])

    results_df = results_df.drop_duplicates() 
    return results_df 




@app.route('/get_search_info', methods=['GET'])
def get_search_info():
    brand_name = request.args.get('brandName')
    product_name = request.args.get('productName')

    # Perform some logic to get information based on brand and product names
    result = f"Information for {brand_name} {product_name}"

    return jsonify({'result': result})
if __name__ == '__main__':
    app.run(debug=False,host=0.0.0.0)
    
    
    
    
