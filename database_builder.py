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


def download_youtube_audio(output_folder="./songs"):
    os.makedirs(output_folder, exist_ok=True)
    downloaded_songs = []
    directory = os.fsencode('songs')
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        downloaded_songs.append(filename.replace('.mp3', ""))

    df = pandas.read_csv('data/songs_database.csv')
    existing_song_titles = df['title'].values.tolist()
    for song_title in existing_song_titles:
        if song_title not in downloaded_songs:
            artist = df[df['title'] == song_title]['artist'].values[0]

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": f"{output_folder}/{song_title}.%(ext)s",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Searching for: {song_title} {artist}")
                info = ydl.extract_info(f"ytsearch:{song_title} {artist} lyrics", download=True)

                if "entries" in info and len(info["entries"]) > 0:
                    mp3_filename = f"{output_folder}/{song_title}.mp3"
                    print(f"Downloaded: {mp3_filename}")
                else:
                    print("No results found.")


def retrieve_spotify_data(genre, start_year, limit=10):
    query = f"genre:{genre} year:{start_year}-{min(start_year + 9, 2025)}"
    results = sp.search(q=query, type="track", limit=limit, market="US")
    clean_results = results['tracks']['items']
    print(clean_results)
    update_database(clean_results, genre, start_year)
    # sorted_results = sorted(results['tracks']['items'], key=lambda d: d['popularity'], reverse=True)
    # for i, track in enumerate(results['tracks']['items']):
    #     print(f'Unsorted: {track['name']} {track['popularity']}')
    #     print(f'Sorted: {sorted_results[i]['name']} {sorted_results[i]['popularity']}')

def update_database(results, genre, year):
    filtered_database = []
    skipped_songs = 0
    try:
        df = pandas.read_csv('data/songs_database.csv')
        filtered_database = df[df['genre'] == genre]['title'].values.tolist()
    except FileNotFoundError:
        pass

    songs = {
        'title': [],
        'artist': [],
        'album': [],
        'genre': [],
        'popularity': [],
        }
     
    for track in results:
        if track['name'] not in filtered_database:
            songs['title'].append(track['name'])
            songs['artist'].append(track['artists'][0]["name"])
            songs['album'].append(track['album']['name'].replace(" (Deluxe)", "").replace(" (Expanded Edition)", ""))
            songs['genre'].append(genre)
            songs['popularity'].append(track['popularity'])
        else:
            skipped_songs += 1

    songs_df = pandas.DataFrame(songs)
    try:
        pandas.read_csv('data/songs_database.csv')
        songs_df.to_csv('data/songs_database.csv', mode='a', index=False, header=False, float_format='%.0f')
    except FileNotFoundError:
        songs_df.to_csv('data/songs_database.csv', mode='a', index=False, float_format='%.0f')
    finally:
        print('Song added successfully.\n')
    
    if skipped_songs > 0:
        retrieve_spotify_data(genre, year, 10+skipped_songs)
    else:
        download_youtube_audio()

