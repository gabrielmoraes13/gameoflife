import random
import pygame
import time
from math import floor
import os

def play_song(song):
    pygame.mixer.init()
    file = pygame.mixer.Sound(f"./songs/{song}")
    start_time = random.randint(10, floor(file.get_length()) - 20)
    pygame.mixer.music.load(f"./songs/{song}")
    pygame.mixer.music.play(start=start_time)
    time.sleep(7)
    pygame.mixer.music.stop()

directory = os.fsencode('songs')
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    play_song(filename)

