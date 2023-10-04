import spotipy
from datetime import datetime, timedelta
import schedule
from spotipy.oauth2 import SpotifyOAuth
import json

scopes = ["user-read-playback-state", "user-modify-playback-state", "user-library-read", "streaming",
          "playlist-modify-private", "playlist-read-collaborative", "playlist-read-private", "playlist-modify-public",
          "user-read-currently-playing", "user-read-recently-played"]
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="411aec8d0b624329be309a03a3246931",
                                                    client_secret="51e12096ff2b4834951ac8060e3cb477",
                                                    redirect_uri="http://localhost:8080",
                                                    scope=scopes))

today = datetime.now()
monday = today - timedelta(days=today.weekday())

data = open('data.json')
data = json.load(data)


def saveDiscoverWeekly(username, playlist_id):
    """
    Main logic of the script
    Saves the discover weekly into a variable, then looping through to get the uri's of each track and saves it a list
    Creates a new playlist, then adds the songs from the list into the playlist
    """

    playlistItems = spotify.playlist_items(playlist_id=playlist_id,
                                           fields='items.track.uri',
                                           additional_types=['track'])

    songs = []
    for tracks in playlistItems['items']:
        for song in tracks:
            songs.append(tracks[song]['uri'])

    playlistName = 'Discover Weekly: {}'.format(monday.date())
    newPlaylist = spotify.user_playlist_create(user=username, name=playlistName, public=False,
                                               collaborative=False)
    spotify.playlist_add_items(newPlaylist['id'], songs)
    spotify.playlist_add_items('6YbNRmoXgG66XGD5yj0FaD', songs)

    print("Just duplicated the this week's Discover Weekly!")


def save_playlist_link(playlist_link):
    playlist_id = str(playlist_link)[34:56]
    data['playlist_id'] = playlist_id
    print(data)
    with open('data.json', 'w') as f:
        json.dump(data, f)


def save_username(username):
    data['username'] = username
    with open('data.json', 'w') as f:
        json.dump(data, f)


if not data['username']:
    username = input("Enter your Spotify username...\n")
    save_username(username)
    print("Username has been saved.")

if not data['playlist_id']:
    playlist_id = input("Enter your Spotify playlist link...\n")
    save_playlist_link(str(playlist_id))
    print("Username has been saved.")


saveDiscoverWeekly(data['username'], data['playlist_id'])

"""
Schedules the task every tuesday at 12 AM, to call the saveDiscoverWeekly function
Only needs to be used if the script is ran 24/7, otherwise you can run it schedule it through Windows scheduler.
"""

"""
schedule.every().tuesday.at('00:00').do(saveDiscoverWeekly)

while True:
    schedule.run_pending()
"""
