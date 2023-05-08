import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

data = json.load(open('data.json', 'r', encoding='utf-8'))

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
   	client_id=data["spotify"]["client_id"],
   	client_secret=data["spotify"]["client_secret"],
   	redirect_uri="http://localhost",
   	scope="user-modify-playback-state",
   	open_browser=False,
 	cache_path='./tokens.txt'
))

sp.start_playback(context_uri='spotify:album:2Qs2SpclDToB087fLolhCN', device_id=data["spotify"]["device_id"])
