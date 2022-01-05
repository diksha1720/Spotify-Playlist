import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


CLIENT_ID = 'YOUR CLIENT ID'
CLIENT_SECRET = 'YOUR CLIENT SECRET'

spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                      client_secret=CLIENT_SECRET,
                                      redirect_uri='http://127.0.0.1:5500/',
                                      scope="playlist-modify-private",
                                      show_dialog=True,
                                      cache_path="token.txt"
                                      ))
user_id = spotify.current_user()["id"]
date = input("What year would you like to travel? (YYYY-MM-DD)")

url = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
song_titles = [song.getText().strip('\n') for song in soup.select('li h3')][:100]
# print(song_titles)
year = date.split("-")[0]

song_uris = []

for song in song_titles:
    result = spotify.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
playlist = spotify.user_playlist_create(user=user_id, name=f"{year} Billboard 100", public=False)


spotify.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
