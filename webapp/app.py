import hashlib
import mimetypes, os, bcrypt
import uuid

from flask_cors import CORS, cross_origin
import requests
from dns.e164 import query
from flask import Flask, render_template, request, jsonify, make_response, send_from_directory, redirect, session, \
    url_for, abort, Response
from flask.cli import load_dotenv
from pymongo import MongoClient
from urllib.parse import urlencode
# functions for routes, these should only be url
from util.spotify import search_spotify_tracks, get_spotify_track_by_id

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


def connect_to_mongo():
    # MongoDB connection
    load_dotenv()
    if os.environ.get('DOCKER_ENV'):
        # print("Docker DB")
        mongoHost = 'mongodb'
    else:
        # print("Local DB")
        mongoHost = 'localhost'
    mongo = MongoClient(mongoHost)
    return mongo.mydatabase


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
    return response


@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    db = connect_to_mongo()
    users_collection = db.users

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
        "password": hashed_password,
        "spotify_login": spotify_login
    })

    return jsonify({"message": "Registration successful"}), 200


@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    db = connect_to_mongo()
    users_collection = db.users
    username = request.json['username']
    password = request.json['password']

    match = users_collection.find_one({"username": username})
    if match is not None and bcrypt.checkpw(password.encode("utf-8"), match["password"]):
        token = str(uuid.uuid4())
        hasher = hashlib.sha256()
        hasher.update(token.encode("utf-8"))
        hashtoken = hasher.hexdigest()
        users_collection.update_one({"username": username}, {"$push": {"token": hashtoken}})
        # Store the spotify login session if available
        session['spotify_login'] = match.get("spotify_login")
        response = Response("Logged in successfully", 302)
        response.set_cookie("Token", hashtoken)
        return response
    else:
        return jsonify({"error": "Incorrect Password/Unknown Username"}), 400


# SPOTIFY URLS
# Redirect to Spotify login
@app.route('/spotify/login', methods=['POST', "OPTIONS", "GET"])
@cross_origin()
def spotify_login():
    # print(os.environ)
    auth_query_parameters = {
    "response_type": "code",
    # "client_id": os.environ.get('CLIENT_ID'),
    "client_id": "db64db9ddf1f44dda99247b7c3f39ecd",
    "redirect_uri": "http://localhost:8080/spotify/callback",
    "scope": "user-library-read",
    }
    url_args = urlencode(auth_query_parameters)
    auth_url = f'https://accounts.spotify.com/authorize/?{url_args}'
    res = requests.get(auth_url, headers={'Access-Control-Allow-Origin': "*"})
    return Response("", 302, headers={"Location": res.request.url})


# Callback to handle token exchange
@app.route('/spotify/callback')
@cross_origin()
def spotify_callback():
    auth_code = request.args.get('code')
    token_data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        "redirect_uri": "/",
        'client_id': "35aedd448433476692a91887cd06e666",
        'client_secret': os.getenv('CLIENT_SECRET'),
    }
    response = requests.post("https://accounts.spotify.com/api/token", data=token_data,
                             headers={'Content-Type': 'application/x-www-form-urlencoded',
                                      "Access-Control-Allow-Origin": "*", "Location": "/"})
    response_data = response.json()

    # Save tokens in session for further requests
    session['access_token'] = response_data.get('access_token')
    session['refresh_token'] = response_data.get('refresh_token')
    response = response
    return response


# takes the search query from the front end
@app.route('/spotify/search')
def search_song():
    query = request.args.get('query')

    results = search_spotify_tracks(query)
    return jsonify(results)


# gets the
@app.route('/song/<id>', methods=['GET'])
def get_song_by_id(id):
    song_data = get_spotify_track_by_id(id)

    return jsonify(song_data)


# add a new post
@app.route('/post', methods=['POST'])
def add_post():
    data = request.json
    # Make each post have its unique id
    post_id = str(uuid.uuid4())
    db = connect_to_mongo()
    posts_collection = db['posts']
    post = {
        "_id": post_id,
        "song_id": data.get("ID"),
        "caption": data.get("caption"),
        "comments": []
    }
    posts_collection.insert_one(post)
    return jsonify({"message": "Post added", "post_id": post_id}), 201

# retrieve all the posts with comments
@app.route('/posts', methods=['GET'])
def get_posts():
    db = connect_to_mongo()
    posts_collection = db['posts']
    posts = list(posts_collection.find({}, {'_id': 0}))
    return jsonify(posts), 200

# Route to add a comment to a specific post
@app.route('/post/<post_id>/comment', methods=['POST'])
def add_comment(post_id):
    data = request.json
    db = connect_to_mongo()
    posts_collection = db['posts']
    comment = {
        # Make each comment have its own unique id
        "comment_id": str(uuid.uuid4()),
        "text": data.get("text")
    }
    posts_collection.update_one({"_id": post_id}, {"$push": {"comments": comment}})
    return jsonify({"message": "Comment added"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
