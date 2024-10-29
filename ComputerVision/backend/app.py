import sqlite3
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
from scipy.spatial.distance import cosine
from PIL import Image
from io import BytesIO
import logging
logging.basicConfig(level=logging.INFO)
import base64

app = Flask(__name__)
CORS(app)

app.logger.setLevel(logging.INFO)

model = ResNet50(weights='resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5',
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


def find_similar_features(query_features) -> int:
    """
    Find the most similar image based on features extracted from ResNet50 model and returns the ID of the most similar image
    """
    conn = sqlite3.connect('feature_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, features FROM features')
    rows = cursor.fetchall()

    similar_items = []
    for row in rows:
        id, features_blob = row
        features = np.frombuffer(features_blob, dtype=np.float32)
        distance = cosine(query_features[0], features)
        similar_items.append([id, distance])
    similar_items.sort(key=lambda x: x[1])
    conn.close()
    if similar_items:
        return similar_items[0][0]
    else:
        return None


def get_image(id: int):
    """
    Get the base64 image based on the id
    """
    conn = sqlite3.connect('feature_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT filename FROM features WHERE id=?', (id,))
    filename = cursor.fetchone()

    conn.close()
    print(filename)
    if filename:
        image_path = f'../amazon_images/{filename[0]}'  # Update with actual path
        img = Image.open(image_path)

        # Convert image to base64
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        response = {
            'image': img_base64,
        }
        return jsonify(response)
    else:
        return jsonify({'error': 'Image not found'}), 404

@app.route('/process-image/image-search', methods=['POST'])
def processImage():
    image_data = request.get_json().get('image')
    if not image_data:
        return jsonify({"error: ", "No image found"}), 400
    img_features = extract_features(image_data)
    print("Image Features: ", img_features)
    img_similar = find_similar_features(img_features)
    print("Similar Image Data: ", img_similar)
    if img_similar:
        response = get_image(img_similar)
        print("Response from get_image:", response.get_json()) 
        return response
    else:
        return jsonify({"error": "No similar images found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
