from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
from scipy.spatial.distance import cosine
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import sqlite3
import time
import os
import requests

model = ResNet50(weights='resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5',
                 include_top=False, pooling='avg')

amazon_df = pd.read_csv("amazon.csv")

# function extracts the features from each image
def extract_features(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = preprocess_input(x)
    features = model.predict(x[None, ...])
    return features

# creating a table with the columns id, filename and features
def create_table():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('feature_database.db')
    cursor = conn.cursor()

    # Create the table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS features (
        id INTEGER PRIMARY KEY,
        filename TEXT,
        features BLOB
    )
    ''')
    conn.commit()
    conn.close()


create_table()

# downloadng the images from the amazon csv file either through the image url or scraping the amazon website
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
images = amazon_df[["img_link", "product_link"]]
n = len(images)
temp = 0
service = Service('./chromedriver')
driver = webdriver.Chrome(service=service)

for i in range(1, n+1):
    response = requests.get(images.iloc[i-1]["img_link"])
    if response.status_code == 200:
        with open("amazon_images/image_" + str(temp) + ".jpg", "wb") as file:
            file.write(response.content)
        temp += 1
    else:
        response = requests.get(images.iloc[i-1]["product_link"])
        product_link = images.iloc[i-1]["product_link"]
        driver.get(product_link)
        time.sleep(3)

        try:
            image_tag = driver.find_element(By.ID, 'landingImage')
            soup = BeautifulSoup(response.content, 'html.parser')
            image_url = image_tag.get_attribute('src')

            if image_url:

                img_response = requests.get(image_url)
                img_response.raise_for_status()
                with open("amazon_images/image_" + str(temp) + ".jpg", "wb") as file:
                    file.write(img_response.content)
                temp += 1
        except Exception as e:
            print("file number" + str(i) + "did not print")

def insert_features(id, filename, features):
    conn = sqlite3.connect('feature_database.db')
    cursor = conn.cursor()

    # Convert features to binary format
    features_blob = features.tobytes()

    cursor.execute('''
    INSERT INTO features (id, filename, features) VALUES (?, ?, ?)
    ''', (id, filename, features_blob))

    conn.commit()
    conn.close()


folder_path = 'amazon_images/'
temp = 0

for img in os.listdir(folder_path):
    try:
        img_path = os.path.join(folder_path, img)
        img_features = extract_features(img_path)
        insert_features(temp, img, img_features)
        temp += 1
    except:
        print(str(img) + " was unable to be inserted")