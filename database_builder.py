import yt_dlp
import os


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



