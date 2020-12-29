import requests
import json

ACCOUNTS_SERVICE = "https://accounts.spotify.com/authorize"
GET_TOKENS = "https://accounts.spotify.com/api/token"
BASE_URL = "https://api.spotify.com/v1"
album_api = "/albums/"
play_api = "/me/player/play"

configs = json.load(open('configs.json', 'r', encoding='utf-8'))
# Example: https://www.google.com/?code=CODE
CODE = configs['code']
CLIENT_ID = configs['client_id']
CLIENT_SECRET = configs['client_secret']
ACCESS_TOKEN = configs['access_token']
REFRESH_TOKEN = configs['refresh_token']


def new_account_get_url():
    print(ACCOUNTS_SERVICE + '?' + '&'.join([f'{param[0]}={param[1]}' for param in [
        ('client_id', CLIENT_ID),
        ('response_type', 'code'),
        ('redirect_uri', 'https%3A%2F%2Fwww.google.com%2F'),
        ('scope', 'user-modify-playback-state')
    ]]))


def get_tokens():
    response = requests.post(GET_TOKENS, data={
        'grant_type': 'authorization_code',
        'code': CODE,
        'redirect_uri': 'https://www.google.com/',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    print(response, response.text)


def get_album(album_id):
    """
    Sample album: 7acEEWUWq2GVgeS9tr9cOp
    """
    full_url = BASE_URL + album_api + album_id
    print(full_url)
    resp = requests.get(full_url, headers={
        'Authorization': 'Bearer ' + ACCESS_TOKEN
    })
    print(resp.text)


def play_album(album_id):
    import json
    full_url = BASE_URL + play_api
    resp = requests.put(full_url, data=json.dumps({
        'context_uri': f'spotify:album:{album_id}'
    }), headers={
        'Authorization': 'Bearer ' + ACCESS_TOKEN
    })
    print(resp, resp.text)

# new_account_get_url()
# get_tokens()
# play_album(configs['album_id'])
