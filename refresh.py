import requests
from requests.auth import HTTPBasicAuth
import configparser
import os

conf_file = os.path.expanduser('~/.spotify')
config = configparser.ConfigParser()
config.read(conf_file)

refresh = config['token']['refresh']
client_id = config['oauth']['client_id']
client_secret = config['oauth']['client_secret']

r = requests.post(
    'https://accounts.spotify.com/api/token',
    auth=HTTPBasicAuth(client_id, client_secret),
    data={"refresh_token": refresh, "grant_type": "refresh_token"}
)

config['token']['bearer'] = r.json()["access_token"]

with open(conf_file, "w") as f:
    config.write(f)
