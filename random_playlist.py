import random
import datetime
import requests
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.expanduser('~/.spotify'))

auth = config['token']['bearer']

host = "api.spotify.com"

headers = {"Authorization": "Bearer " + auth}

print("Grabbing user")
resp = requests.get("https://api.spotify.com/v1/me", headers=headers)
user = resp.json()["id"]

next_url = "https://api.spotify.com/v1/me/albums?limit={limit}&offset={offset}".format(limit=50, offset=0)
albums = []
while next_url:
    print("Retrieving next set of albums")
    resp = requests.get(next_url, headers=headers)
    body = resp.json()
    next_url = body["next"]
    for item in body["items"]:
        albums.append(item["album"])

print("Creating playlist")
now = datetime.date.today().isoformat()
playlist_request = {"name": "10 Random Albums", "public": False, "description": "Generated " + now}
resp = requests.post(
    "https://api.spotify.com/v1/users/{user}/playlists".format(user=user),
    headers=headers,
    json=playlist_request)

playlist = resp.json()["id"]

random.shuffle(albums)

def pick(album):
    print("Adding {count} tracks from album {name} by {artist}".format(
        count=len(album["tracks"]["items"]),
        name=album["name"],
        artist=album["artists"][0]["name"]
    ))
    tracks = [item["uri"] for item in album["tracks"]["items"]]
    return {"uris": tracks}

def add(tracks):
    resp = requests.post(
        "https://api.spotify.com/v1/users/{user}/playlists/{playlist}/tracks".format(user=user, playlist=playlist),
        headers=headers,
        json=tracks)

for album in albums[0:10]:
    add(pick(album))
