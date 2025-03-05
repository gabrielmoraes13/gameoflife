import pandas
import random
import sys
import tkinter
from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime

MAIN_COLOR = "#222831"
SECONDARY_COLOR = "#393E46"
COLOR_3 = "#00ADB5"
COLOR_4 = "#EEEEEE"
SECONDARY_TEXT = ('Arial', 12, 'bold')

class GameScreen:
    def __init__(self):
        self.window = Tk()
        self.window.minsize(height=600, width=920)
        self.window.title("Quizzer")
        self.window.config(padx=60, pady=20, bg=COLOR_3)

    def create_board(self):
        frame = Frame(self.window)
        frame.pack()
        self.window.mainloop()


def main():
    screen = GameScreen()
    screen.create_board()

main()