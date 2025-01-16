from dotenv import load_dotenv
import os
import base64
import requests
import json

# Load environment variables
load_dotenv()

# Retrieve CLIENT_ID and CLIENT_SECRET from .env file
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    
    # Make the POST request
    result = requests.post(url, headers=headers, data=data)
    
    # Check for successful response
    if result.status_code != 200:
        raise Exception(f"Failed to retrieve token: {result.status_code} {result.text}")
    
    # Parse JSON response
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = requests.get(query_url, headers=headers)
    
    # Check for successful response
    if result.status_code != 200:
        raise Exception(f"Failed to search for artist: {result.status_code} {result.text}")
    
    # Parse JSON response
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist can be found with this name...")
        return None
    return json_result[0]["id"]

def get_top_tracks(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = get_auth_header(token)
    params = {"market": "US"}  # Specify the market for localized results

    result = requests.get(url, headers=headers, params=params)
    
    # Check for successful response
    if result.status_code != 200:
        raise Exception(f"Failed to retrieve top tracks: {result.status_code} {result.text}")
    
    # Parse JSON response
    json_result = json.loads(result.content)["tracks"]
    top_tracks = [{"name": track["name"], "preview_url": track["preview_url"]} for track in json_result[:10]]
    return top_tracks

# Main execution
try:
    token = get_token()
    artist_id = search_for_artist(token, "Michel Jackson")
    if artist_id:
        top_tracks = get_top_tracks(token, artist_id)
        print("Top 10 Songs by Eminem:")
        for idx, track in enumerate(top_tracks, 1):
            print(f"{idx}. {track['name']} - Preview URL: {track['preview_url']}")
except Exception as e:
    print(f"Error: {e}")
