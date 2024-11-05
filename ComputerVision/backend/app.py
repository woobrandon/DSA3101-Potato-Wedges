import sqlite3
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
from scipy.spatial.distance import cosine
from PIL import Image
from io import BytesIO
import pickle
import base64
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

# If there is an error of being unable to find the weights file, try changing the directory in the terminal to /backend.
model = ResNet50(weights='./resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5',
                 include_top=False, pooling='avg')


def extract_features(image_data: str):
    """
    Extract the features the a base64 image
    """
    # Decode the Base64 string
    img_data = base64.b64decode(image_data.split(
        ',')[1])
    img = Image.open(BytesIO(img_data))
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize((224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model.predict(x)
    return features


def find_similar_features(query_features, n: int, threshold: float) -> int:
    """
    Find the most similar image based on features extracted from ResNet50 model and returns the product_id of the most similar image
    """
    
    conn = sqlite3.connect('feature_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT product_id, features, product_name FROM features')
    rows = cursor.fetchall()

    similar_items = []
    for row in rows:
        product_id, features_blob, name = row
        features = np.frombuffer(features_blob, dtype=np.float32)
        distance = cosine(query_features[0], features)
        similar_items.append([product_id, distance, name])
    similar_items.sort(key=lambda x: x[1])
    conn.close()
    products = []
    result = []
    if similar_items:
        while len(products) < n+1:
            curr_img = similar_items.pop(0)
            if curr_img[1] >= threshold:
                break
            if curr_img[2] not in products:
                result.append(curr_img[0])
                products.append(curr_img[2])
        return result
    else:
        return None


def get_image(ids: int):
    """
    Get the base64 image based on the product_id
    """
    conn = sqlite3.connect('feature_database.db')
    cursor = conn.cursor()

    image_data = []

    for product_id in ids:
        cursor.execute(
            'SELECT product_name, product_price, filename, productUrl, about_product, category, product_desc FROM features WHERE product_id=?', (product_id,))
        data = cursor.fetchall()[0]
        if data:
            product_name, product_price, filename, productUrl, about_product, category, product_desc = data
            # Update with actual path
            image_path = f'../amazon_images/{filename}'
            img = Image.open(image_path)

            # Convert image to base64
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            image_data.append({
                'name': product_name,
                'product_price': product_price,
                'image': img_base64,
                'product_url': productUrl,
                'about': about_product,
                'category': category,
                'product_desc': product_desc
            })
        else:
            conn.close()
            return jsonify({'error': 'Image not found'}), 404
    conn.close()
    return image_data


def cross_sell_and_up_sell(product_id) -> tuple[list, list]:
    """
    Find the most similar products based on product_desc
    """

    def decode_pickle_array(pickle_bytes):
        # Decode the pickle encoded column, 'vector'
        return pickle.loads(pickle_bytes)

    def convertToBase64Image(filename: str) -> str:
        image_path = f'../amazon_images/{filename}'
        img = Image.open(image_path)

        if img.mode != 'RGB':
            img = img.convert('RGB')

        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return img_base64

    conn = sqlite3.connect('feature_database.db')
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT product_name, product_price, filename, productUrl, about_product, category, product_desc, vector 
        FROM features WHERE product_id=?
        """, (product_id,))
    data_base = cursor.fetchall()
    data_base_df = pd.DataFrame(
        data_base, columns=[desc[0] for desc in cursor.description])
    data_base_df['vector'] = data_base_df['vector'].apply(decode_pickle_array)
    base_vec = np.array([data_base_df['vector'][0]])
    # print(base_vec, '\n')

    cursor.execute(
        """
        SELECT product_name, product_price, filename, productUrl, about_product, category, product_desc, vector
        FROM features WHERE product_id!=?
        """, (product_id,))
    data = cursor.fetchall()
    data_df = pd.DataFrame(
        data, columns=[desc[0] for desc in cursor.description])
    data_df['vector'] = data_df['vector'].apply(decode_pickle_array)
    mat = np.vstack(data_df['vector'])
    # print(mat)
    conn.close()

    data_df['image'] = data_df['filename'].apply(convertToBase64Image)

    cos_sim = cosine_similarity(base_vec, mat).flatten()
    # print(cos_sim)
    df = data_df.copy()
    df['similarity'] = cos_sim

    # Cross_sell
    cross_sell_similarity = df.sort_values(
        'similarity', ascending=False).head(10)
    cross_sell_data = []
    for i in range(10):
        cross_sell_data.append({
            'name': cross_sell_similarity.iloc[i]['product_name'],
            'product_price': cross_sell_similarity.iloc[i]['product_price'],
            'product_url': cross_sell_similarity.iloc[i]['productUrl'],
            'about': cross_sell_similarity.iloc[i]['about_product'],
            'category': cross_sell_similarity.iloc[i]['category'],
            'product_desc': cross_sell_similarity.iloc[i]['product_desc'],
            'image': cross_sell_similarity.iloc[i]['image']
        })

    # Up_sell
    up_sell_similarity = df.query(f'product_price > {data_base_df.loc[0, "product_price"]} & similarity >= 0.8').sort_values(
        'similarity', ascending=False).head(10)
    up_sell_data = []
    for i in range(10):
        up_sell_data.append({
            'name': up_sell_similarity.iloc[i]['product_name'],
            'product_price': up_sell_similarity.iloc[i]['product_price'],
            'product_url': up_sell_similarity.iloc[i]['productUrl'],
            'about': up_sell_similarity.iloc[i]['about_product'],
            'category': up_sell_similarity.iloc[i]['category'],
            'product_desc': up_sell_similarity.iloc[i]['product_desc'],
            'image': up_sell_similarity.iloc[i]['image']
        })
    return cross_sell_data, up_sell_data


@app.route('/process-image/image-search', methods=['POST'])
def processImage():
    image_data = request.get_json().get('image')
    if not image_data:
        return jsonify({"error: ", "No image found"}), 400
    img_features = extract_features(image_data)
    similar_imgs = find_similar_features(img_features, 4, 0.3)
    if similar_imgs:
        response_img = get_image(similar_imgs)
        response_sell = cross_sell_and_up_sell(similar_imgs[0])
        return jsonify({'image_search': response_img, 'cross_sell': response_sell[0], 'up_sell': response_sell[1]})
    else:
        return jsonify({"error": "No similar images found"}), 404


@app.route('/process-image/image-categorization', methods=['POST'])
def categorization():
    image_data = request.get_json().get('image')
    if not image_data:
        return jsonify({"error: ", "No image found"}), 400
    img_features = extract_features(image_data)
    similar_imgs_id = find_similar_features(img_features, 100)
    if similar_imgs_id:
        categories = {}
        result = []
        i = 0
        similar_imgs = get_image(similar_imgs_id)
        for img in similar_imgs:
            try:
                position = categories[img["category"]]
                result[position][1] += 1
            except:
                categories[img["category"]] = i
                result.append([img["category"], 1])
                i += 1
        result.sort(key=lambda x: x[1], reverse=True)
        return result[0][0]


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
