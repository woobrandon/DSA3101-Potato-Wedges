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
import numpy as np
import sqlite3
import time
import os
import gensim.downloader as api
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import requests
import pickle

# nltk.download('wordnet')
# nltk.download('punkt_tab')

# initialise the model using the weights obtained from training
model = ResNet50(weights='resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5',
                 include_top=False, pooling='avg')

amazon_df = pd.read_csv("../amazon.csv")


def clean_descriptions(amazon_df):
    """
    Extract and clean the product_name, category and about_product into the col 'product_desc'
    """
    df = amazon_df.copy()
    # Removing special characters and leading whitespace
    amazon_df['product_name'] = amazon_df['product_name'].str.replace(
        r"[\'&]", '', regex=True)
    amazon_df['product_name'] = amazon_df['product_name'].str.replace(
        r"[-/]", " ", regex=True)
    amazon_df['product_name'] = amazon_df['product_name'].str.replace(
        r"\$\{.*?\}", '', regex=True)
    amazon_df['product_name'] = amazon_df['product_name'].str.replace(
        '/', ' ')
    amazon_df['product_name'] = amazon_df['product_name'].str.replace(
        r"[\'-]", '', regex=True)
    amazon_df['about_product'] = amazon_df['about_product'].str.replace(
        r"[\'&]", '', regex=True)
    amazon_df['about_product'] = amazon_df['about_product'].str.replace(
        r"[-/]", " ", regex=True)
    amazon_df['about_product'] = amazon_df['about_product'].str.replace(
        r"\$\{.*?\}", '', regex=True)
    amazon_df['about_product'] = amazon_df['about_product'].str.replace(
        '/', ' ')
    amazon_df['about_product'] = amazon_df['about_product'].str.replace(
        r"[\'-]", '', regex=True)

    # NA fields will not contribute anything to the product description
    amazon_df['product_name'].fillna('', inplace=True)
    amazon_df['category'].fillna('', inplace=True)
    amazon_df['about_product'].fillna('', inplace=True)

    # Join product category, brand, name and variant into single string
    amazon_df['product_desc'] = amazon_df.apply(lambda x: ' '.join(
        [x['product_name'], x['category'], x['about_product']]), axis=1)
    df['product_desc'] = amazon_df['product_desc']
    return df


def tokenize_descriptions(cleaned_amazon_df):
    """
    Tokenize product_desc into a new column 'tokens' and lemmatize it into another column 'lemma'
    """
    # Tokenize and lemmatize product descriptions
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    cleaned_amazon_df['tokens'] = cleaned_amazon_df['product_desc'].apply(
        lambda x: word_tokenize(x))

    def lemmatize(l):
        lemmatized = [word.lower()
                      for word in l if word not in stop_words and word.isalpha()]
        return [lemmatizer.lemmatize(word) for word in lemmatized]

    cleaned_amazon_df['lemma'] = cleaned_amazon_df['tokens'].apply(
        lambda x: lemmatize(x))
    return cleaned_amazon_df


def generate_word_embeddings(tokenized_amazon_df):
    """
    Generate the word embeddings for the description and add them into the column 'vector'
    """
    model = api.load('glove-wiki-gigaword-100')

    def mean_vector(desc, model, vocab, id_map, vector_dim):
        vec = np.zeros(vector_dim)
        word_count = 0

        for word in desc:
            # verify that there is a vector embedding for that word
            if word in id_map:
                vec = np.add(vec, model[word])
                word_count += 1
        # find mean of vectors representing words in product description
        vec = np.divide(vec, word_count)
        return np.array(vec)

    vocab = set(tokenized_amazon_df['lemma'].sum())
    id_map = model.key_to_index
    tokenized_amazon_df['vector'] = tokenized_amazon_df.apply(lambda x: mean_vector(
        x['lemma'], model, vocab, id_map, 100), axis=1)
    return tokenized_amazon_df


def process_data_desc(amazon_df):
    cleaned_df = clean_descriptions(amazon_df)
    tokenized_df = tokenize_descriptions(cleaned_df)
    df = generate_word_embeddings(tokenized_df)
    return df


def extract_features(img_path):
    """
    Extract the features from each image
    """
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = preprocess_input(x)
    features = model.predict(x[None, ...])
    return features


def create_table():
    """
    Create a table with the columns id, filename, features and productUrl
    """
    # Connect to the SQLite database
    conn = sqlite3.connect('feature_database.db')
    cursor = conn.cursor()

    # Drop the table if it exists
    cursor.execute('DROP TABLE IF EXISTS features')

    # Create the table with the correct schema
    cursor.execute('''
    CREATE TABLE features (
        id INTEGER PRIMARY KEY,
        product_id TEXT,
        product_name TEXT,
        filename TEXT,
        features BLOB,
        productUrl TEXT,
        about_product TEXT,
        category TEXT, 
        product_desc TEXT, 
        tokens BLOB,
        lemma BLOB,
        vector BLOB
    )
    ''')
    conn.commit()
    conn.close()
    print("Table initialized!")
    return


def insert_features(id, product_id, productname, filename, features, productUrl, about, category, product_desc, tokens, lemma, vector):
    """
    Inserts features into database after extracting it with the extract function
    """
    about = about.replace("|", ", ")
    category = category.replace("|", ", ")
    conn = sqlite3.connect('feature_database.db')
    cursor = conn.cursor()

    # Convert features to binary format
    features_blob = features.tobytes()
    tokens = pickle.dumps(tokens)
    lemma = pickle.dumps(lemma)
    vector = pickle.dumps(vector)

    cursor.execute('''
    INSERT INTO features (id, product_id, product_name, filename, features, productUrl, about_product, category, product_desc, tokens, lemma, vector) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (id, product_id, productname, filename, features_blob, productUrl, about, category, product_desc, tokens, lemma, vector))

    conn.commit()
    conn.close()
    return


def scrape_amzn_images():
    """
    Downloads the images from the amazon csv file either through the image url or scraping the amazon website
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    images = amazon_df[["img_link", "product_link"]]
    n = len(images)
    service = Service('./chromedriver')
    driver = webdriver.Chrome(service=service)

    for i in range(i, n+1):
        response = requests.get(images.iloc[i-1]["img_link"])
        if response.status_code == 200:
            with open("../amazon_images/image_" + str(i) + ".jpg", "wb") as file:
                file.write(response.content)
        else:
            response = requests.get(images.iloc[i-1]["product_link"])
            product_link = images.iloc[i-1]["product_link"]
            driver.get(product_link)
            time.sleep(1.5)
            try:
                image_tag = driver.find_element(By.ID, 'landingImage')
                soup = BeautifulSoup(response.content, 'html.parser')
                image_url = image_tag.get_attribute('src')

                if image_url:
                    img_response = requests.get(image_url)
                    img_response.raise_for_status()
                    with open("../amazon_images/image_" + str(i) + ".jpg", "wb") as file:
                        file.write(img_response.content)
            except Exception as e:
                print("file number" + str(i) + "did not print")
    print("Scraping complete!")
    return


create_table()

folder_path = '../amazon_images'

amazon_df = process_data_desc(amazon_df)

# Scrapes the amazon website
# if not os.path.exists(folder_path):
#     os.makedirs(folder_path)
#     scrape_amzn_images()
# else:
#     scrape_amzn_images()

db_id = 0

for img in os.listdir(folder_path):
    try:
        img_path = os.path.join(folder_path, img)
        img_features = extract_features(img_path)
        insert_features(db_id, amazon_df["product_id"][int(img[6:-4])-1], amazon_df["product_name"][int(img[6:-4])-1], img, img_features, amazon_df["product_link"][int(
            img[6:-4])-1], amazon_df["about_product"][int(img[6:-4])-1], amazon_df["category"][int(img[6:-4])-1],
            amazon_df["product_desc"][int(
                img[6:-4])-1], amazon_df["tokens"][int(img[6:-4])-1],
            amazon_df["lemma"][int(img[6:-4])-1], amazon_df["vector"][int(img[6:-4])-1])
        db_id += 1
    except Exception as e:
        print(str(img) + " was unable to be inserted: ", e)
