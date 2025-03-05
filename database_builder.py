import yt_dlp
import os

songs = ["Bad Romance", "Just dance", "Poker Face", "Abracadabra", "G.U.Y.", "Million Reasons", "Shallow", "Always remember you this way", "Telephone", "Born This Way", "Rain on Me"]

def download_youtube_audio(video_name, complement, output_folder="./songs"):
    os.makedirs(output_folder, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_folder}/{video_name}.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Searching for: {video_name} {complement}")
        info = ydl.extract_info(f"ytsearch:{video_name} {complement} lyrics", download=True)

        if "entries" in info and len(info["entries"]) > 0:
            mp3_filename = f"{output_folder}/{video_name}.mp3"
            print(f"Downloaded: {mp3_filename}")
        else:
            print("No results found.")


for song in songs:
    download_youtube_audio(song, 'Lady Gaga')
