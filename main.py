import random
import pygame
import time
from math import floor
import os
from database_builder import download_youtube_audio
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '300f0b2f4048447c972f2a730fe455dc'
client_secret = '55f5c8fa86af46378dbb4591bbb250fd'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))


def play_song(song):
    pygame.mixer.init()
    file = pygame.mixer.Sound(f"./songs/{song}")
    start_time = random.randint(10, floor(file.get_length()) - 20)
    pygame.mixer.music.load(f"./songs/{song}")
    pygame.mixer.music.play(start=start_time)
    time.sleep(7)
    pygame.mixer.music.stop()

def retrieve_spotify_data(genre, start_year):
    query = f"genre:{genre} year:{start_year}-{start_year + 9}"
    results = sp.search(q=query, type="track", limit=50, market="US")
    
    
    sorted_results = sorted(results['tracks']['items'], key=lambda d: d['popularity'], reverse=True)
    for i, track in enumerate(results['tracks']['items']):
        print(f'Unsorted: {track['name']} {track['popularity']}')
        print(f'Sorted: {sorted_results[i]['name']} {sorted_results[i]['popularity']}')


retrieve_spotify_data('rock', 1990)


# directory = os.fsencode('songs')
# for file in os.listdir(directory):
#     filename = os.fsdecode(file)
#     play_song(filename)

