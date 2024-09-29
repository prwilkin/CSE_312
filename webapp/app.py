from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def connect_to_mongo():
    # MongoDB connection
    client = MongoClient("mongodb://mongo:27017/")
    db = client.mydatabase


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
