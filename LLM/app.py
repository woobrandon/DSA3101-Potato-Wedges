from flask import Flask, render_template, jsonify
from src.messageOllama import send_message_to_ollama, get_random_description
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("data/amazon.csv")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/optimise-description', methods=['POST'])
def optimise_description():
    product_description = get_random_description(df)
    response = send_message_to_ollama(product_description)
    # response = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Unde repellat in harum, eligendi nam ex minima quidem dolorem laborum asperiores porro deleniti a eveniet, illum fuga reprehenderit voluptates sequi officia beatae ducimus eaque repudiandae non. Magni quos accusantium perspiciatis modi! Unde, vitae eveniet maiores facilis fugiat non ducimus voluptatum sequi praesentium dolorem inventore ex sapiente. Similique, quisquam! Provident sunt, cumque sapiente ratione ullam expedita accusamus quas. Quidem suscipit nihil optio quas, dolores, facilis magnam nostrum facere, assumenda nemo tempore quo eaque commodi. Rem pariatur obcaecati non saepe illo ipsum unde asperiores, provident voluptatum cupiditate nemo maxime iste sit quibusdam corporis."
    return jsonify(product_description=product_description, response=response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
