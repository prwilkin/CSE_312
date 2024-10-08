import mimetypes
import bcrypt
from flask import Flask, render_template, request, jsonify, make_response, send_from_directory
from pymongo import MongoClient

app = Flask(__name__)

def connect_to_mongo():
    # MongoDB connection
    client = MongoClient("mongodb://mongo:27017/")
    db = client.mydatabase
    return db

db = connect_to_mongo()

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

users_collection = db.users

@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password1 = request.json['password']
    password2 = request.json['password2']

    if not username or not password1 or not password2:
        return jsonify({"error": "All fields are required"}), 400

    # Password matching
    if password1 != password2:
        return jsonify({"error": "Passwords do not match"}), 400
    
    # Check if username exists
    if users_collection.find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 400

    # Hash and salt the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password1.encode('utf-8'), salt)

    # Store in the database
    users_collection.insert_one({
        "username": username,
        "password": hashed_password
    })

    return jsonify({"message": "Registration successful"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
