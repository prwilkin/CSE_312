import mimetypes

from flask import Flask, render_template, make_response, send_from_directory
from pymongo import MongoClient

app = Flask(__name__)

# This sets the No sniff for every request
# I might add the content type here as well if the project structure grows
@app.after_request
def apply_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route('/static/<path:filename>')
def custom_static(filename):
    # Get the file's type based on its extension
    mimetype, _ = mimetypes.guess_type(filename)
    response = make_response(send_from_directory('static', filename))

    # Set if it found one, not sure if always does, might make it throw error if it cant find type
    if mimetype:
        response.headers['Content-Type'] = mimetype

@app.route('/')
def index():
    return render_template('index.html')



def connect_to_mongo():
    # MongoDB connection
    client = MongoClient("mongodb://mongo:27017/")
    db = client.mydatabase


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
