import yt_dlp
import os
import pandas
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import sys

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
            artist = df[df['title'] == song_title]['artists'].values[0].split(" | ")[0]

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


def retrieve_spotify_data(genre, start_year, limit=30):
    query = f"genre:{genre} year:{start_year}-{min(start_year + 9, 2025)}"
    try:
        results = sp.search(q=query, type="track", limit=limit, market="US")
    except Exception as e:
        sys.exit(f'An error occured: {e}')
    clean_results = results['tracks']['items']
    update_database(clean_results, genre, start_year)


def update_database(results, genre, year):
    filtered_df = []
    try:
        df = pandas.read_csv('data/songs_database.csv')
        filtered_df = df[df['genre'] == genre]['title'].values.tolist()

    except FileNotFoundError:
        pass

    songs = {
        'title': [],
        'artists': [],
        'album': [],
        'genre': [],
        'popularity': [],
        'year': [],
        'album_cover': [],
        }
     
    for track in results:
        title_index = track['name'].find(" (")
        album_index = track['album']['name'].find(" (")
        if title_index > -1:
            clean_track_title = track['name'][0:title_index]
        else:
            clean_track_title = track['name']
        if album_index > -1:
            clean_album_title = track['album']['name'][0:album_index]
        else:
            clean_album_title = track['album']['name']
        if clean_track_title not in filtered_df:
            songs['title'].append(clean_track_title)
            artists = track['artists'][0]["name"]
            try:
                artists += " | " + track['artists'][1]["name"]
            except IndexError:
                pass
            songs['artists'].append(artists)
            songs['album'].append(clean_album_title)
            songs['genre'].append(genre)
            songs['popularity'].append(track['popularity'])
            songs['year'].append(year)
            songs['album_cover'].append(track['album']['images'][1]["url"])

    songs_df = pandas.DataFrame(songs)
    try:
        pandas.read_csv('data/songs_database.csv')
        songs_df.to_csv('data/songs_database.csv', mode='a', index=False, header=False, float_format='%.0f')
    except FileNotFoundError:
        songs_df.to_csv('data/songs_database.csv', mode='a', index=False, float_format='%.0f')
    finally:
            print('Songs added successfully.\n')
            download_youtube_audio()
        
    


