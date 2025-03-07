import pandas
import random
import sys
import tkinter
# from tabulate import tabulate
from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime
from spotify_genres import available_genres

MAIN_COLOR = "#222831"
SECONDARY_COLOR = "#393E46"
COLOR_3 = "#00ADB5"
COLOR_4 = "#EEEEEE"
SECONDARY_FONT = ('Arial', 12, 'bold')

class UserInterface:
    def __init__(self):
        self.window = Tk()
        self.window.minsize(height=600, width=920)
        self.window.title("Quizzer")
        self.window.config(padx=60, pady=20, bg=COLOR_3)
        self.enter_test_button: type[tkinter.Button]
        self.enter_practice_button: type[tkinter.Button]
        self.edit_button: type[tkinter.Button]
        self.delete_database_button: type[tkinter.Button]
        self.view_statistics_button: type[tkinter.Button]


    def open_starting_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        difficulty_lb = Label(
            text="Choose the level",
            fg=COLOR_4,
            bg=COLOR_3,
            font=SECONDARY_FONT
        )
        difficulty_lb.place(x=150, y=120)

        difficulty_cb = ttk.Combobox(self.window, width=30, state='readonly')
        difficulty_cb['values'] = ['Easy', 'Normal', 'Hard']
        difficulty_cb.current(1)
        difficulty_cb.place(x=320, y=120)

        genre_lb = Label(
            text="Choose a genre",
            fg=COLOR_4,
            bg=COLOR_3,
            font=SECONDARY_FONT
        )
        genre_lb.place(x=150, y=200)

        genre_cb = ttk.Combobox(self.window, width=30, state='readonly')
        genre_cb['values'] = available_genres
        genre_cb.current(86)
        genre_cb.place(x=320, y=200)

        year_lb = Label(
            text="Choose the decade",
            fg=COLOR_4,
            bg=COLOR_3,
            font=SECONDARY_FONT
        )
        year_lb.place(x=150, y=280)

        year_cb = ttk.Combobox(self.window, width=30, state='readonly')
        year_cb['values'] = ['1970', '1980', '1990', '2000', '2010', '2020']
        year_cb.current(5)
        year_cb.place(x=320, y=280)


        # add_questions_button = Button(
        #     text="Add questions",
        #     width=25,
        #     command=lambda: self.check_entries(
        #         difficulty_cb.get(),
        #         genre_cb.get(),
        #         year_cb.get(),
        #     )
        # )
        add_questions_button = Button(
            text="Add questions",
            width=25,
            command=self.open_game_window
            
        )
        add_questions_button.place(x=300, y=500)


        self.window.mainloop()


    def retrieve_data(self, difficulty, genre, year):
        retrieve_spotify_data(genre, year) 
        confirmation = messagebox.askyesno('Do you want to start the game?')
        if confirmation == True:
            start_game(genre, decade, difficulty)
        else:
            sys.exit('The program has been shut down.')


    def open_wait_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        wait_lb = Label(
            text="Please wait until the download is complete.\nIt might take up to 5 minutes.",
            fg=COLOR_4,
            bg=COLOR_3,
            font=('Arial', 15, 'bold')
        )
        wait_lb.place(x=200, y=250)


    def open_game_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        
        song_lb = Label(
        text="Choose the level",
        fg=COLOR_4,
        bg=COLOR_3,
        font=SECONDARY_FONT
        )
        song_lb.place(x=60, y=400)

        song_et = Entry(width=30)
        song_et.place(x=60, y=450)

        artist_lb = Label(
        text="Choose the level",
        fg=COLOR_4,
        bg=COLOR_3,
        font=SECONDARY_FONT
        )
        artist_lb.place(x=320, y=400)

        artist_et = Entry(width=30)
        artist_et.place(x=320, y=450)

        album_lb = Label(
            text="Choose the decade",
            fg=COLOR_4,
            bg=COLOR_3,
            font=SECONDARY_FONT
        )
        album_lb.place(x=580, y=400)

        album_et = Entry(width=30)
        album_et.place(x=580, y=450)

        register_answer_btn = Button(
            text="Register guesses",
            width=25,
            command=lambda: self.check_entries(
                difficulty_cb.get(),
                genre_cb.get(),
                year_cb.get(),
            )
        )
        register_answer_btn.place(x=300, y=500)
        # subtitle_label = Label(
        #     text="You can ignore the 'incorrect answer fields' in case you want to add a freeform question",
        #     fg=COLOR_4,
        #     bg=COLOR_3,
        #     font=('Arial', 12)
        # )
        # subtitle_label.place(x=110, y=90)

        # question_text_label = Label(
        #     text="Question text",
        #     fg=MAIN_COLOR,
        #     bg=COLOR_3,
        #     font=self.font_secondary_text
        # )
        # question_text_label.place(x=60, y=140)

        # question_text_entry = Entry(width=80)
        # question_text_entry.place(x=230, y=140)

        # question_answer_label = Label(
        #     text="Question answer",
        #     fg=MAIN_COLOR,
        #     bg=COLOR_3,
        #     font=self.font_secondary_text
        # )
        # question_answer_label.place(x=60, y=200)

        # question_answer_entry = Entry(width=80)
        # question_answer_entry.place(x=230, y=200)

        # incorrect_answer1_label = Label(
        #     text="1st incorrect answer",
        #     fg=MAIN_COLOR,
        #     bg=COLOR_3,
        #     font=self.font_secondary_text
        # )
        # incorrect_answer1_label.place(x=60, y=260)

        # incorrect_answer1_entry = Entry(width=80)
        # incorrect_answer1_entry.place(x=230, y=260)

        # incorrect_answer2_label = Label(
        #     text="2nd incorrect answer",
        #     fg=MAIN_COLOR,
        #     bg=COLOR_3,
        #     font=self.font_secondary_text
        # )
        # incorrect_answer2_label.place(x=60, y=320)

        # incorrect_answer2_entry = Entry(width=80)
        # incorrect_answer2_entry.place(x=230, y=320)

        # incorrect_answer3_label = Label(
        #     text="3rd incorrect answer",
        #     fg=MAIN_COLOR,
        #     bg=COLOR_3,
        #     font=self.font_secondary_text
        # )
        # incorrect_answer3_label.place(x=60, y=380)

        # incorrect_answer3_entry = Entry(width=80)
        # incorrect_answer3_entry.place(x=230, y=380)

        # add_multiple_choice_button = Button(
        #     text=f"Add multiple choice question",
        #     width=25,
        #     command=lambda: self.add_question(
        #         'multiple choice',
        #         question_text_entry.get(),
        #         question_answer_entry.get(),
        #         incorrect_answer1_entry.get(),
        #         incorrect_answer2_entry.get(),
        #         incorrect_answer3_entry.get())
        # )
        # add_multiple_choice_button.place(x=180, y=440)

        # add_freeform_button = Button(
        #     text=f"Add as freeform question",
        #     width=25,
        #     command=lambda: self.add_question(
        #         'free form',
        #         question_text_entry.get(),
        #         question_answer_entry.get())
        # )
        # add_freeform_button.place(x=400, y=440)

        # self.enter_practice_button = Button(
        #     text=f"Enter practice mode",
        #     width=25,
        #     command=lambda: self.initialize_test_window(
        #         number=1,
        #         weight='Yes')
        # )
        # self.enter_practice_button.place(x=180, y=490)

        # self.enter_test_button = Button(
        #     text=f"Enter test mode",
        #     width=25,
        #     command=self.enter_test_mode
        # )
        # self.enter_test_button.place(x=400, y=490)

        # return_home_button = Button(
        #     text='Return to home page',
        #     width=32,
        #     command=self.open_starting_window
        # )
        # return_home_button.place(x=260, y=540)

        # self.update_buttons(add_questions_window=True)

    # def open_enable_disable_window(self):
    #     for widget in self.window.winfo_children():
    #         widget.destroy()

    #     enable_disable_label = Label(
    #         text="Please type in the ID (as provided when viewing the statistics)\n"
    #              "of the questions you would like to disable or enable.\n"
    #              "In case you want to edit multiple questions,\n"
    #              "please separate the values with commas.",
    #         fg=MAIN_COLOR,
    #         bg=COLOR_3,
    #         font=('Arial', 12, 'bold')
    #     )
    #     enable_disable_label.place(x=160, y=100)

    #     enable_disable_entry = Entry(width=43)
    #     enable_disable_entry.place(x=260, y=220)
    #     enable_disable_entry.focus()

    #     disable_button = Button(
    #         text='Disable',
    #         width=28,
    #         font=('Arial', 10),
    #         command=lambda: self.quiz_features.edit_question(
    #             state='No',
    #             indexes=enable_disable_entry.get().split(','))
    #     )
    #     disable_button.place(x=120, y=250)

    #     enable_button = Button(
    #         text='Enable',
    #         width=28,
    #         font=('Arial', 10),
    #         command=lambda: self.quiz_features.edit_question(
    #             state='Yes',
    #             indexes=enable_disable_entry.get().split(','))
    #     )
    #     enable_button.place(x=380, y=250)

    #     return_home_button = Button(
    #         text='Return to home page',
    #         width=32,
    #         font=('Arial', 10),
    #         command=self.open_starting_window
    #     )
    #     return_home_button.place(x=240, y=300)

    # def enter_test_mode(self):
    #     for widget in self.window.winfo_children():
    #         widget.destroy()

    #     question_number_label = Label(
    #         text=f"Choose how many questions you\n would like to have in this test.\n\n"
    #              f"There are {self.quiz_features.get_questions_available()} questions available.",
    #         fg=MAIN_COLOR,
    #         bg=COLOR_3,
    #         font=('Arial', 14, 'bold')
    #     )
    #     question_number_label.place(x=240, y=80)

    #     question_number_entry = Entry(width=43)
    #     question_number_entry.place(x=260, y=200)
    #     question_number_entry.focus()

    #     question_number_button = Button(
    #         text='Confirm',
    #         width=32,
    #         font=('Arial', 10),
    #         command=lambda: self.initialize_test_window(
    #             number=question_number_entry.get())
    #     )
    #     question_number_button.place(x=260, y=230)

    #     return_home_button = Button(
    #         text='Return to home page',
    #         width=32,
    #         font=('Arial', 10),
    #         command=self.open_starting_window
    #     )
    #     return_home_button.place(x=260, y=270)

    # def initialize_test_window(self, number, weight=None):
    #     self.questions_obj = Questions(number, self.quiz_features.get_questions_available(), weight)
    #     if self.questions_obj:
    #         for widget in self.window.winfo_children():
    #             widget.destroy()
    #         self.fetch_next_question(weight)

    # def fetch_next_question(self, weight=None):
    #     if weight == 'Yes':
    #         self.current_question = self.questions_obj.next_question_practice()
    #     else:
    #         self.current_question = self.questions_obj.next_question_test()

    #     try:
    #         self.current_question.get('question index')
    #         self.update_test_window(weight)
    #     except AttributeError:
    #         right_answers = self.current_question[0]
    #         wrong_answers = self.current_question[1]
    #         self.open_score_window(right_answers, wrong_answers, weight)

    # def update_test_window(self, weight=None):

    #     canvas = Canvas(width=800, height=526)
    #     canvas_img = PhotoImage(file="images/card_front.png")
    #     canvas.create_image(400, 263, image=canvas_img)
    #     canvas.create_text(
    #         400, 163,
    #         text=self.current_question['question text'],
    #         font=("Arial", 20, "bold"),
    #         width=700
    #     )

    #     possible_answers = [str(self.current_question['correct answer']),
    #                         str(self.current_question['incorrect answer 1']),
    #                         str(self.current_question['incorrect answer 2']),
    #                         str(self.current_question['incorrect answer 3'])]
    #     random.shuffle(possible_answers)

    #     question_index = self.current_question['question index']
    #     correct_answer = str(self.current_question['correct answer'])

    #     answer_1_button = Button(
    #         text=possible_answers[0],
    #         width=40,
    #         font=('Arial', 10),
    #         command=lambda: self.send_answer(
    #             answer=possible_answers[0],
    #             correct_answer=correct_answer,
    #             index=question_index,
    #             weight=weight)
    #     )

    #     answer_2_button = Button(
    #         text=possible_answers[1],
    #         width=40,
    #         font=('Arial', 10),
    #         command=lambda: self.send_answer(
    #             answer=possible_answers[1],
    #             correct_answer=correct_answer,
    #             index=question_index,
    #             weight=weight)
    #     )

    #     answer_3_button = Button(
    #         text=possible_answers[2],
    #         width=40,
    #         font=('Arial', 10),
    #         command=lambda: self.send_answer(
    #             answer=possible_answers[2],
    #             correct_answer=correct_answer,
    #             index=question_index,
    #             weight=weight)
    #     )

    #     answer_4_button = Button(
    #         text=possible_answers[3],
    #         width=40,
    #         font=('Arial', 10),
    #         command=lambda: self.send_answer(
    #             answer=possible_answers[3],
    #             correct_answer=correct_answer,
    #             index=question_index,
    #             weight=weight)
    #     )

    #     if self.current_question['question type'] == 'multiple choice':
    #         answer_1_button.place(x=60, y=350)
    #         answer_2_button.place(x=415, y=350)
    #         answer_3_button.place(x=60, y=400)
    #         answer_4_button.place(x=415, y=400)
    #     else:
    #         freeform_entry = Entry(width=43, fg='black')
    #         freeform_entry.place(x=255, y=300)
    #         freeform_entry.focus()

    #         freeform_button = Button(
    #             text='Submit',
    #             width=15,
    #             font=('Arial', 10),
    #             command=lambda: self.send_answer(
    #                 answer=freeform_entry.get().lower().strip(),
    #                 correct_answer=correct_answer.lower(),
    #                 index=question_index,
    #                 weight=weight)
    #         )

    #         freeform_button.place(x=320, y=350)

    #     if weight:
    #         return_home_button = Button(
    #             text='Return to home page',
    #             width=32,
    #             font=('Arial', 10),
    #             command=self.open_starting_window
    #         )
    #         return_home_button.place(x=250, y=450)

    #     canvas.config(bg=COLOR_3, highlightthickness=0)
    #     canvas.grid(row=0, column=0, columnspan=2)

    # def open_score_window(self, right_answers, wrong_answers, weight):
    #     for widget in self.window.winfo_children():
    #         widget.destroy()

    #     score_label = Label(
    #         text=f"You got {right_answers} right out of {wrong_answers}!",
    #         fg=MAIN_COLOR,
    #         bg=COLOR_3,
    #         font=('Arial', 14, 'bold')
    #     )
    #     score_label.place(x=280, y=120)

    #     return_home_button = Button(
    #         text='Return to home page',
    #         width=32,
    #         font=('Arial', 10),
    #         command=self.open_starting_window
    #     )
    #     return_home_button.place(x=250, y=190)

    #     close_program_button = Button(
    #         text='Close program',
    #         width=32,
    #         font=('Arial', 10),
    #         command=self.close_program
    #     )
    #     close_program_button.place(x=250, y=240)

    #     if not weight:
    #         date = datetime.today().date()
    #         hour = datetime.today().hour
    #         minutes = datetime.today().minute
    #         with open('data/user_score.txt', 'a') as file:
    #             file.write(f'On {date} at {hour}:{minutes} you scored {right_answers} out of {wrong_answers}.\n')

    # def update_buttons(self, delete=None, add_questions_window=None):
    #     if delete:
    #         self.quiz_features.delete_database()
    #     if not add_questions_window:
    #         existing_file_buttons = [self.view_statistics_button, self.edit_button, self.delete_database_button]
    #     else:
    #         existing_file_buttons = []
    #     try:
    #         pandas.read_csv('data/user_database.csv')
    #         for button in existing_file_buttons:
    #             button.config(state='normal')
    #         if self.quiz_features.get_questions_available() >= 5:
    #             self.enter_practice_button.config(state='normal')
    #             self.enter_test_button.config(state='normal')
    #         else:
    #             self.enter_practice_button.config(state='disabled')
    #             self.enter_test_button.config(state='disabled')
    #     except FileNotFoundError:
    #         for button in existing_file_buttons:
    #             button.config(state='disabled')
    #         self.enter_practice_button.config(state='disabled')
    #         self.enter_test_button.config(state='disabled')

    # def send_answer(self, answer, correct_answer, index, weight=None):
    #     self.questions_obj.check_answer(answer, correct_answer, index, weight)
    #     self.fetch_next_question(weight)

    # def add_question(self, q_type, text, answer, incorrect_answer1=None,
    #                  incorrect_answer2=None, incorrect_answer3=None, test=None):
    #     if self.quiz_features.check_entry_data(q_type, text, answer, incorrect_answer1, incorrect_answer2,
    #                                            incorrect_answer3):
    #         table = {
    #             'Question': [str(text)],
    #             'Answer': [str(answer)],
    #             'Incorrect answer 1': [str(incorrect_answer1)],
    #             'Incorrect answer 2': [str(incorrect_answer2)],
    #             'Incorrect answer 3': [str(incorrect_answer3)],
    #             'Question type': [q_type],
    #         }
    #         print(tabulate(table, headers='keys', tablefmt='psql', showindex=False))

    #         confirmation = messagebox.askyesno(
    #             'Confirm question addition?',
    #             f'Do you really want to add to the database the\n question printed to the console?')
    #         if confirmation:
    #             question_to_add = {
    #                 'question': [str(text)],
    #                 'answer': [str(answer)],
    #                 'incorrect_answer1': [str(incorrect_answer1)],
    #                 'incorrect_answer2': [str(incorrect_answer2)],
    #                 'incorrect_answer3': [str(incorrect_answer3)],
    #                 'answered_right': [0],
    #                 'answered_wrong': [0],
    #                 'answered_right_percentage': ['N/A'],
    #                 'times_shown': [0],
    #                 'question_type': [q_type],
    #                 'is_active': ['Yes'],
    #                 'question_weight': [10],
    #             }
    #             question_to_add_df = pandas.DataFrame(question_to_add)
    #             try:
    #                 pandas.read_csv('data/user_database.csv')
    #                 question_to_add_df.to_csv('data/user_database.csv', mode='a', index=False, header=False, float_format='%.0f')
    #             except FileNotFoundError:
    #                 question_to_add_df.to_csv('data/user_database.csv', mode='a', index=False, float_format='%.0f')
    #             finally:
    #                 print('Question added successfully.\n')
    #         else:
    #             print('Operation canceled.')

    #         if not test:
    #             self.update_buttons(add_questions_window=True)

    # @staticmethod
    # def close_program():
    #     sys.exit('Program successfully closed.')

window = UserInterface()
window.open_starting_window()