BACKGROUND_COLOR = "#B1DDC6"
FONT_FOR_LANGUAGE = ("Ariel", 40, "italic")
FONT_FOR_WORD = ("Ariel", 60, "bold")

import pandas
from tkinter import *
import random

word_now = []
word_old = []
french_to_learn = []
english_to_learn = []
len_word_to_learn = 0
count_check = 0 #check have or dont have word to learn file
'''
try:
    data2 = pandas.read_csv("words_to_learn.csv")
    len_word_to_learn = len(data2)
    count_check = 1
except FileNotFoundError:
    len_word_to_learn = 0
    count_check = 0
'''

def make_word():
    global word_now

    data = pandas.read_csv("./data/french_words.csv")
    #else:
       # data = data2

    ran_pos = random.randint(0, len(data))
    french_word = data["French"][ran_pos]
    english_word = data["English"][ran_pos]
    if len(word_now) == 0:
        word_now.append(french_word)
        word_now.append(english_word)
    else:
        word_now[0] = french_word
        word_now[1] = english_word


def change_word():
    global word_now, flip_timer, word_old
    if len(word_old) == 0:
        word_old.append(word_now[0])
        word_old.append(word_now[1])
    else:
        word_old[0] = word_now[0]
        word_old[1] = word_now[1]
    make_word()
    window.after_cancel(flip_timer)
    canvas.itemconfig(card_background, image=front_img)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=word_now[0], fill="black")
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_background, image=back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=word_now[1], fill="white")


def save_word_to_learn():
    global french_to_learn, english_to_learn
    if word_old[0] not in french_to_learn:
        french_to_learn.append(word_old[0])
        english_to_learn.append(word_old[1])
        new_word_dict = {
            "French": french_to_learn,
            "English": english_to_learn
        }
        new_word = pandas.DataFrame(new_word_dict)
        new_word.to_csv("words_to_learn.csv", index=False)


def remove_to_learn():
    global french_to_learn, english_to_learn, len_word_to_learn, count_check
    try:
        for i in range(0, len_word_to_learn):
            if french_to_learn[i].lower() == word_old[0].lower():
                french_to_learn.pop(i)
                english_to_learn.pop(i)
                break
        new_word_dict = {
            "French": french_to_learn,
            "English": english_to_learn
        }
        new_word = pandas.DataFrame(new_word_dict)
        new_word.to_csv("words_to_learn.csv", index=False)

    except IndexError:
        return


window = Tk()
window.title("Flash card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

make_word()
canvas = Canvas(width=800, height=526)
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=front_img)
card_title = canvas.create_text(400, 150, font=FONT_FOR_LANGUAGE, fill="black", text="French")
card_word = canvas.create_text(400, 263, font=FONT_FOR_WORD, fill="black", text=word_now[0])
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

'''
canvas_front = Canvas(width=800, height=526)
back_img = PhotoImage(file="./images/card_back.png")
canvas_front.create_image(526, 800, image=back_img)
canvas_front.create_text(400, 150, font=FONT_FOR_LANGUAGE, fill="black", text="English")
canvas_front.create_text(400, 263, font=FONT_FOR_WORD, fill="black", text=make_word()[1])
canvas_front.config(highlightthickness=0, bg=BACKGROUND_COLOR)
canvas_front.grid(row=0, column=0, columnspan=2)
'''

right_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=lambda: [change_word(), remove_to_learn()])
right_button.grid(row=1, column=1)

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=lambda: [change_word(), save_word_to_learn()])
wrong_button.grid(row=1, column=0)

window.mainloop()
