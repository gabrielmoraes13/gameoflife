import yt_dlp
import os
import ffmpeg
import pygame

songs = ["Bad Romance", "Just dance", "Poker Face", "Abracadabra", "G.U.Y.", "Million Reasons", "Shallow", "Always remember you this way", "Telephone", "Born This Way", "Rain on Me"]

def download_youtube_audio(video_name, complement, output_folder="./songs"):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # yt-dlp options
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_folder}/{video_name}.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    # Download audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Searching for: {video_name} {complement}")
        info = ydl.extract_info(f"ytsearch:{video_name} {complement} lyrics", download=True)

        # Extract the downloaded filename
        if "entries" in info and len(info["entries"]) > 0:
            mp3_filename = f"{output_folder}/{video_name}.mp3"
            print(f"Downloaded: {mp3_filename}")
        else:
            print("No results found.")


for song in songs:
    download_youtube_audio(song, 'Lady Gaga')


# def play_audio(file_path):
#     pygame.mixer.init()
#     pygame.mixer.music.load(file_path)
#     pygame.mixer.music.play()
#
#     while pygame.mixer.music.get_busy():
#         continue  # Keep playing until the song ends
#
#
# play_audio("Queen – Bohemian Rhapsody (Official Video Remastered).mp3")