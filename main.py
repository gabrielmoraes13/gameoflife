import random
import pygame
import time
from math import floor
import os
from database_builder import download_youtube_audio, retrieve_spotify_data


def play_song(song):
    pygame.mixer.init()
    file = pygame.mixer.Sound(f"./songs/{song}")
    start_time = random.randint(10, floor(file.get_length()) - 20)
    pygame.mixer.music.load(f"./songs/{song}")
    pygame.mixer.music.play(start=start_time)
    time.sleep(7)
    pygame.mixer.music.stop()


def main():
    genre_options = ["Rock", "Pop", "Jazz", "Country", "R&B"]
    decade_options = [1970, 1980, 1990, 2000, 2010, 2020]
    genre = input(f"Please select the genre of music you'd like to guess. Available options: {", ".join(genre_options)}\n"
                  f"Choice: ").title()
    if genre not in genre_options:
        print("Sorry, that's an invalid input")
    else:
        decade = int(input(f"Now please select the decade from the following options: {", ".join(str(decade) for decade in decade_options)}."
                           f"\nAfter this input the program will download the mp3 files needed for you to play the game, please give it a few minutes.\n"
                           f"Choice: "))
        if decade not in decade_options:
            print("Sorry, that's an invalid input")
        else:
            retrieve_spotify_data(genre, decade)


main()


