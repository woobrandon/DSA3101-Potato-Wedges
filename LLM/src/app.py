from flask import Flask, render_template, jsonify
from messageOllama import get_random_description
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("data/amazon.csv")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get-description', methods=['POST'])
def optimise_description():
    product_description = get_random_description(df)
    return jsonify(product_description=product_description)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
