import pandas
import random
import sys
from tkinter import *
from tkinter import ttk
from spotify_genres import available_genres
from PIL import ImageTk, Image
import io
import urllib.request
import pygame
import time
from math import floor
from database_builder import retrieve_spotify_data

MAIN_COLOR = "#00ADB5"
SECONDARY_COLOR = "#EEEEEE"
PRIMARY_FONT = ('Arial', 10, 'bold')
SECONDARY_FONT = ('Arial', 12, 'bold')
TERTIARY_FONT = ('Arial', 10)

class UserInterface:
    def __init__(self):
        self.window = Tk()
        self.window.minsize(height=600, width=920)
        self.window.title("Guess the song!")
        self.window.config(padx=60, pady=20, bg=MAIN_COLOR)
        self.score = 0


    def open_starting_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        game_start_lb = Label(
            text="Choose the options for your guessing game.",
            fg=SECONDARY_COLOR,
            bg=MAIN_COLOR,
            font=SECONDARY_FONT
        )
        game_start_lb.place(x=220, y=50)

        easy_lb = Label(
            text="Easy: You select the genre and the decade, and the first 4 letters of each guess will be revealed.",
            fg='black',
            bg=MAIN_COLOR,
            font=TERTIARY_FONT
        )
        easy_lb.place(x=110, y=80)

        
        normal_lb = Label(
            text="Normal: You select the genre and the decade, and you won't get any hints.",
            fg='black',
            bg=MAIN_COLOR,
            font=TERTIARY_FONT
        )
        normal_lb.place(x=110, y=100)

        hard_lb = Label(
            text="Hard: You can select only the genre, the decade will be random, ranging from the 90s to 2020.",
            fg='black',
            bg=MAIN_COLOR,
            font=TERTIARY_FONT
        )
        hard_lb.place(x=110, y=120)

        difficulty_lb = Label(
            text="Choose the level",
            fg=SECONDARY_COLOR,
            bg=MAIN_COLOR,
            font=SECONDARY_FONT
        )
        difficulty_lb.place(x=150, y=220)

        difficulty_cb = ttk.Combobox(self.window, width=30, state='readonly')
        difficulty_cb['values'] = ['Easy', 'Normal', 'Hard']
        difficulty_cb.current(1)
        difficulty_cb.place(x=320, y=220)

        genre_lb = Label(
            text="Choose a genre",
            fg=SECONDARY_COLOR,
            bg=MAIN_COLOR,
            font=SECONDARY_FONT
        )
        genre_lb.place(x=150, y=270)

        genre_cb = ttk.Combobox(self.window, width=30, state='readonly')
        genre_cb['values'] = available_genres
        genre_cb.current(54)
        genre_cb.place(x=320, y=270)

        year_lb = Label(
            text="Choose the decade",
            fg=SECONDARY_COLOR,
            bg=MAIN_COLOR,
            font=SECONDARY_FONT
        )
        year_lb.place(x=150, y=320)

        year_cb = ttk.Combobox(self.window, width=30, state='readonly')
        year_cb['values'] = ['1970', '1980', '1990', '2000', '2010', '2020']
        year_cb.current(5)
        year_cb.place(x=320, y=320)

        disclaimer_lb = Label(
            text="Please wait until the download is complete. It might take up to 5 minutes.\nIf you have downloaded the songs before, the game will skip to the next window.",
            fg=SECONDARY_COLOR,
            bg=MAIN_COLOR,
            font=PRIMARY_FONT
        )
        disclaimer_lb.place(x=150, y=450)

        add_songs_btn = Button(
            text="Add questions",
            width=25,
            command=lambda: self.retrieve_data(
                difficulty_cb.get(),
                genre_cb.get(),
                int(year_cb.get()),
            )
        )

        add_songs_btn.place(x=300, y=500)

        self.window.mainloop()


    def retrieve_data(self, difficulty, genre, year):
        retrieve_spotify_data(genre, year) 
        if difficulty == 'Hard':
            year = random.choice(1990, 2000, 2010, 2020)
        self.fetch_songs(difficulty, genre, year)
        

    def fetch_songs(self, difficulty, genre, year):
        self.difficulty = difficulty
        self.df = pandas.read_csv('data/songs_database.csv')
        self.filtered_df = self.df.loc[(self.df['genre'] == genre) & (self.df['year'] == year)]
        self.songs_to_play = self.filtered_df['title'].values.tolist()
        random.shuffle(self.songs_to_play)
        self.songs_played = 0
        self.open_guess_window()
        

    def open_guess_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        image = PhotoImage(file="assets/question-mark.png").subsample(2, 2)
        self.label = Label(self.window, image=image, bg=MAIN_COLOR)
        self.label.place(x=3000, y=3000)
        self.label.place(x=260, y=60)

        score_lb = Label(
        text=f"Current score: {self.score}/{self.songs_played*3}",
        fg=SECONDARY_COLOR,
        bg=MAIN_COLOR,
        font=SECONDARY_FONT
        )
        score_lb.place(x=50, y=180)

        song_lb = Label(
        text="What's the song?",
        fg=SECONDARY_COLOR,
        bg=MAIN_COLOR,
        font=SECONDARY_FONT
        )
        song_lb.place(x=60, y=390)

        song_et = Entry(width=30)
        song_et.place(x=40, y=420)

        artist_lb = Label(
        text="What's the artist?",
        fg=SECONDARY_COLOR,
        bg=MAIN_COLOR,
        font=SECONDARY_FONT
        )
        artist_lb.place(x=320, y=380)

        artist_disc_lb = Label(
        text="(If there's more than 1, please input only 1)",
        fg='black',
        bg=MAIN_COLOR,
        font=TERTIARY_FONT
        )
        artist_disc_lb.place(x=270, y=400)

        artist_et = Entry(width=30)
        artist_et.place(x=300, y=420)

        album_lb = Label(
            text="What's the album?",
            fg=SECONDARY_COLOR,
            bg=MAIN_COLOR,
            font=SECONDARY_FONT
        )
        album_lb.place(x=580, y=390)

        album_et = Entry(width=30)
        album_et.place(x=560, y=420)

        play_song_btn = Button(
            text="Play song",
            width=25,
            command=lambda: self.play_song()
        )
        play_song_btn.place(x=200, y=500)

        self.register_answer_btn = Button(
            text="Register guesses",
            width=25,
            state='disabled',
            command=lambda: self.check_guesses(
                song_et.get(),
                artist_et.get(),
                album_et.get(),
            )
        )
        self.register_answer_btn.place(x=400, y=500)

        self.quit_game_btn = Button(
            text="Quit game",
            width=25,
            command=self.quit_game
        )
        self.quit_game_btn.place(x=300, y=530)

        if self.difficulty == 'Easy':
            song_hint = Label(
            text=f"Hint: {self.songs_to_play[self.songs_played][0:4]}...",
            fg='black',
            bg=MAIN_COLOR,
            font=TERTIARY_FONT
            )
            song_hint.place(x=70, y=450)

            artists = [artist[0:4] for artist in self.df[self.df['title'] == self.songs_to_play[self.songs_played]]['artists'].values[0].split(" | ")]
            artist_hint = Label(
            text=f"Hint: {', '.join(artists)}...",
            fg='black',
            bg=MAIN_COLOR,
            font=TERTIARY_FONT
            )
            artist_hint.place(x=350, y=450)

            artist_hint = Label(
            text=f"Hint: {self.df[self.df['title'] == self.songs_to_play[self.songs_played]]['album'].values[0][0:4]}...",
            fg='black',
            bg=MAIN_COLOR,
            font=TERTIARY_FONT
            )
            artist_hint.place(x=610, y=450)
        self.window.mainloop()


    def open_answer_window(self, answers):
        emojis = []
        for answer in answers:
            if answer:
                emojis.append("✅")
            else:
                emojis.append("❌")
        for widget in self.window.winfo_children():
            widget.destroy()

        with urllib.request.urlopen(self.df[self.df['title'] == self.songs_to_play[self.songs_played]]['album_cover'].values[0]) as u:
            raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        photo = ImageTk.PhotoImage(image)

        self.bg_lb = Label(self.window, image=photo, bg=MAIN_COLOR)
        self.bg_lb.place(x=260, y=60)

        song_text = f"The song was: {self.songs_to_play[self.songs_played]} {emojis[0]}"
        artist_text = f"The artist was: {' & '.join(self.df[self.df['title'] == self.songs_to_play[self.songs_played]]['artists'].values[0].split(" | "))} {emojis[1]}"
        album_text = f"The album was: {self.df[self.df['title'] == self.songs_to_play[self.songs_played]]['album'].values[0]} {emojis[2]}"
        song_answer = Label(
        text=song_text,
        fg=SECONDARY_COLOR,
        bg=MAIN_COLOR,
        font=SECONDARY_FONT
        )
        song_answer.place(x=260, y=390)
        
        artist_answer = Label(
        text=artist_text,
        fg=SECONDARY_COLOR,
        bg=MAIN_COLOR,
        font=SECONDARY_FONT
        )
        artist_answer.place(x=260, y=420)
        
        album_answer = Label(
        text=album_text,
        fg=SECONDARY_COLOR,
        bg=MAIN_COLOR,
        font=SECONDARY_FONT
        )
        album_answer.place(x=260, y=450)
        
        self.songs_played += 1

        if self.songs_played < len(self.songs_to_play):
            next_song_btn = Button(
                text="Skip results.",
                width=25,
                command=self.open_guess_window,
            )
            
        else:
            next_song_btn = Button(
                text="You reached the end. Quit game.",
                width=25,
                command=self.quit_game,
            )
        next_song_btn.place(x=300, y=500)
        score_lb = Label(
        text=f"Current score: {self.score}/{self.songs_played*3}",
        fg=SECONDARY_COLOR,
        bg=MAIN_COLOR,
        font=SECONDARY_FONT
        )
        score_lb.place(x=50, y=180)
        
        self.window.mainloop()


    def check_guesses(self, g_song, g_artist, g_album):
        song_right = False
        artist_right = False
        album_right = False
        if str(g_song).lower().strip() == self.songs_to_play[self.songs_played].lower():
            self.score += 1
            song_right = True
        if str(g_artist).lower().strip() in  self.df[self.df['title'] == self.songs_to_play[self.songs_played]]['artists'].values[0].lower().split(" | "):
            self.score += 1
            artist_right = True
        if str(g_album).lower().strip() ==  self.df[self.df['title'] == self.songs_to_play[self.songs_played]]['album'].values[0].lower():
            self.score += 1
            album_right = True

        self.open_answer_window(answers=(song_right, artist_right, album_right))
        

    def play_song(self):
        song = self.songs_to_play[self.songs_played]
        pygame.mixer.init()
        file = pygame.mixer.Sound(f"./songs/{song}.mp3")
        start_time = random.randint(10, floor(file.get_length()) - 20)
        pygame.mixer.music.load(f"./songs/{song}.mp3")
        pygame.mixer.music.play(start=start_time)
        time.sleep(7)
        pygame.mixer.music.stop()
        self.register_answer_btn.config(state='normal')
        

    def display_image_from_url(self, url):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()

        image = Image.open(io.BytesIO(raw_data))
        photo = ImageTk.PhotoImage(image)
        label = Label(self.window, image=photo)
        label.place(x=60, y=60)

    def quit_game(self):
        sys.exit()
