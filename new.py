# streamlit_app.py

import streamlit as st
from PIL import Image
import requests
from bs4 import BeautifulSoup
from googlesearch import search

def search_product_description(product_name):
    try:
        # Search for the product on Google and extract the description from the Wikipedia link
        for url in search(product_name + ' Wikipedia', num=1, stop=1, pause=2):
            if 'wikipedia' in url:
                req = requests.get(url).text
                scrap = BeautifulSoup(req, 'html.parser')
                description_tag = scrap.find('p')
                description = description_tag.text.strip() if description_tag else 'No information found'
                return description
        return 'No information found'
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit app
st.title("Product Description Search")
product_name = st.text_input("Enter the product name:")
if product_name:
    result = search_product_description(product_name)
    st.write(result)
