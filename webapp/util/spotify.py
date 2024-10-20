import requests
from flask import session, abort

# user logins in
# user searches
# user selects song
# user get returned song


def get_spotify_session_token():
    if 'access_token' not in session:
        abort(401, description="User not logged in.")
    return session['access_token']


def make_spotify_request(url, headers):
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        abort(401, description="Unauthorized. Token may be invalid or expired.")
    elif response.status_code == 404:
        abort(404, description="Resource not found.")
    elif response.status_code != 200:
        abort(response.status_code, description=f"Spotify API Error: {response.text}")

    return response.json()


# this is the search api | API: https://developer.spotify.com/documentation/web-api/reference/search
# will return a list of dicts from this response. each index has the song name, artists name, spotify track id
def search_spotify_tracks(query):
    if not query:
        abort(400, description="Missing query parameter.")

    access_token = get_spotify_session_token()
    headers = {'Authorization': f"Bearer {access_token}"}
    search_url = f"https://api.spotify.com/v1/search?q={query}&type=track&market=US&limit=10"

    response = make_spotify_request(search_url, headers)
    result = []
    for track in response['tracks']['items']:
        result.append({"name": track['name'], "artists": track['artists'][0]['name'], "id": track['id']})
    return result


# this will get the song by id | API: https://developer.spotify.com/documentation/web-api/reference/get-track
# will return a dict from this response. the dict has the song name, artist name, spotify id, playback url, and album image url
def get_spotify_track_by_id(track_id):
    access_token = get_spotify_session_token()
    headers = {'Authorization': f"Bearer {access_token}"}
    track_url = f"https://api.spotify.com/v1/tracks/{track_id}"

    response = make_spotify_request(track_url, headers)
    return {"name": response['name'], "artists": response['artists'][0]["name"], "id": response['id'],
            "playback": response['playback_mode', "image": response['album']['images'][0]['url']]}
