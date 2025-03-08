import random
import pygame
import time
from math import floor
from database_builder import retrieve_spotify_data
import pandas
import sys
from spotify_genres import available_genres
from screen import UserInterface


def main():
    game_window = UserInterface()
    game_window.open_starting_window()


main()



