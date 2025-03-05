import random
import pygame
import time
from math import floor
import os
from database_builder import download_youtube_audio
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
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
    query = f"genre:{genre} year:{start_year}-{min(start_year + 9, 2025)}"
    results = sp.search(q=query, type="track", limit=50, market="US")
    
    
    sorted_results = sorted(results['tracks']['items'], key=lambda d: d['popularity'], reverse=True)

    # for i, track in enumerate(results['tracks']['items']):
    #     print(f'Unsorted: {track['name']} {track['popularity']}')
    #     print(f'Sorted: {sorted_results[i]['name']} {sorted_results[i]['popularity']}')


def main():
    genre_options = ["Rock", "Pop", "Jazz", "Country", "R&B"]
    decade_options = [1970, 1980, 1990, 2000, 2010, 2020]
    genre = input(f"Please select the genre of music you'd like to guess. Available options: {", ".join(genre_options)}\n"
                  f"Choice: ").title()
    if genre not in genre_options:
        print("Sorry, that's an invalid input")
    else:
        decade = int(input(f'Now please select the decade from the following options: {", ".join(str(decade) for decade in decade_options)}.\nChoice: '))
        if decade not in decade_options:
            print("Sorry, that's an invalid input")
        else:
            retrieve_spotify_data(genre, decade)


main()



# directory = os.fsencode('songs')
# for file in os.listdir(directory):
#     filename = os.fsdecode(file)
#     play_song(filename)

