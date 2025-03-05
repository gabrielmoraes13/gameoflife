import yt_dlp
import os
import pandas
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))


def download_youtube_audio(song, artist, output_folder="./songs"):
    os.makedirs(output_folder, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_folder}/{song}.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Searching for: {song} {artist}")
        info = ydl.extract_info(f"ytsearch:{song} {artist} lyrics", download=True)

        if "entries" in info and len(info["entries"]) > 0:
            mp3_filename = f"{output_folder}/{song}.mp3"
            print(f"Downloaded: {mp3_filename}")
        else:
            print("No results found.")


def retrieve_spotify_data(genre, start_year):
    query = f"genre:{genre} year:{start_year}-{min(start_year + 9, 2025)}"
    results = sp.search(q=query, type="track", limit=10, market="US")
    clean_results = results['tracks']['items']
    print(clean_results)
    update_database(clean_results, genre)
    # sorted_results = sorted(results['tracks']['items'], key=lambda d: d['popularity'], reverse=True)
    # for i, track in enumerate(results['tracks']['items']):
    #     print(f'Unsorted: {track['name']} {track['popularity']}')
    #     print(f'Sorted: {sorted_results[i]['name']} {sorted_results[i]['popularity']}')

def update_database(results, genre):
    songs = {
        'title': [],
        'artist': [],
        'album': [],
        'genre': [],
        'popularity': [],
        }
     
    for track in results:
        songs['title'].append(track['name'])
        songs['artist'].append(track['artists'][0]["name"])
        songs['album'].append(track['album']['name'].replace(" (Deluxe)", "").replace(" (Expanded Edition)", ""))
        songs['genre'].append(genre)
        songs['popularity'].append(track['popularity'])

    songs_df = pandas.DataFrame(songs)
    try:
        pandas.read_csv('data/songs_database.csv')
        songs_df.to_csv('data/songs_database.csv', mode='a', index=False, header=False, float_format='%.0f')
    except FileNotFoundError:
        songs_df.to_csv('data/songs_database.csv', mode='a', index=False, float_format='%.0f')
    finally:
        print('Song added successfully.\n')
