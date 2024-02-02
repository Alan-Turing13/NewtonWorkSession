from tkinter import *
import math
import simpleaudio as sa
from PIL import ImageTk, Image
import sys
import os
# ---------------------------- CONSTANTS ------------------------------- #
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the path to the resources is different
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

newton_jpeg_path = os.path.join(application_path, 'Newton.jpeg')
green_lion_png_path = os.path.join(application_path, 'green-lion-rosarium-philosophorum-hedesan-coloured.png')
end_wav_path = os.path.join(application_path, 'end.wav')

BLACK = "#2D2727"
GREY = "#413543"
PURPLE = "#8F43EE"
YELLOW = "#F0EB8D"
FONT_NAME = "Trebuchet"
WORK_MIN = 75
SHORT_BREAK_MIN = 11
LONG_BREAK_MIN = 22
timer = None
reps_done = 0
short_breaks_seq = [1, 3, 4, 6, 7, 9, 10, 12, 13, 15, 16, 18]
long_breaks_seq = [2, 5, 8, 11, 14, 17, 19]
breaks_taken = 0
breaktime = False
worktime = False

wave_obj2 = sa.WaveObject.from_wave_file(end_wav_path)

def bell_sound(end_wav_path):
    play_obj = wave_obj2.play()
# ---------------------------- TIMER RESET ------------------------------- #

def reset():

    global breaktime
    global worktime
    global reps_done
    global breaks_taken

    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="0:00:00")
    title.config(text="A Newton work session", fg=YELLOW, bg=GREY, font=(FONT_NAME, 22))
    title.place(x=111, y=-33)
    if breaktime:
        breaks_taken -= 1
    elif worktime:
        reps_done -= 1

    breaktime = False
    worktime = False
# ---------------------------- TIMER MECHANISM ------------------------------- #

def start_timer():

    global reps_done
    global breaks_taken
    global breaktime
    global worktime

    if breaktime or worktime:
        pass

    else:
        bell_sound(end_wav_path)

        if reps_done > breaks_taken and reps_done in short_breaks_seq:
            breaks_taken += 1
            breaktime = True
            countdown(SHORT_BREAK_MIN * 60)
            title.config(text="'Nature is pleased with simplicity. And nature is no dummy'",
                         fg=YELLOW, font=(FONT_NAME, 16))
            title.place(x=2, y=-27)

        elif reps_done > breaks_taken and reps_done in long_breaks_seq:
            breaks_taken += 1
            breaktime = True
            countdown(LONG_BREAK_MIN * 60)
            title.config(text="'To myself I am only a child playing on the beach, \nwhile "
            "vast oceans of truth lie undiscovered before me'", fg=YELLOW, font=(FONT_NAME, 13))
            title.place(x=60, y=-39)

        elif reps_done == breaks_taken:
            reps_done += 1
            worktime = True
            countdown(WORK_MIN * 60)
            title.config(text="'What we know is a drop, what we don't know is "
            "an ocean.'", fg=YELLOW, font=(FONT_NAME, 16))
            title.place(x=5, y=-27)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def countdown(count):

    global worktime
    global breaktime

    if count > 0:
        global timer
        timer = window.after(1000, countdown, count - 1)
    else:
        completed_sessions.config(text=f"Newton work sessions completed: {reps_done}")
        worktime = False
        breaktime = False
        start_timer()
        bell_sound('end.wav')

    hours_remaining = math.floor(count / 3600)
    mins_remaining = math.floor((count % 3600) / 60)
    secs_remaining = count % 60

    if mins_remaining == 0:
        mins_remaining = "00"
    elif mins_remaining < 10:
        mins_remaining = f"0{mins_remaining}"
    if secs_remaining == 0:
        secs_remaining = "00"
    elif secs_remaining < 10:
        secs_remaining = f"0{secs_remaining}"

    canvas.itemconfig(timer_text, text=f"{hours_remaining}:{mins_remaining}:{secs_remaining}")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("NWS")
window.config(padx=111, pady=55, bg=GREY)

canvas = Canvas(width=440, height=530, bg=BLACK, highlightthickness=0)
Newton_img = ImageTk.PhotoImage(Image.open(newton_jpeg_path))
canvas.create_image(220, 265, image=Newton_img)
timer_text = canvas.create_text(220, 303, text="0:00:00", fill=YELLOW, font=(FONT_NAME, 33))
canvas.grid(column=1, row=1)

lion_img = Image.open(green_lion_png_path)
resized_lion_img = lion_img.resize((88,88), Image.ANTIALIAS)
new_lion_img = ImageTk.PhotoImage(resized_lion_img)

sidelion_l = Label(highlightbackground=GREY, image=new_lion_img, bg=GREY)
sidelion_l.place(x=-100, y=200)

flipped_lion_img = resized_lion_img.transpose(Image.FLIP_LEFT_RIGHT)
new_flipped_lion_img = ImageTk.PhotoImage(flipped_lion_img)

sidelion_r = Label(highlightbackground=GREY, image=new_flipped_lion_img, bg=GREY)
sidelion_r.place(x=450, y=200)

title = Label(text="A Newton work session", fg=YELLOW, bg=GREY, font=(FONT_NAME, 22))
title.place(x=111, y=-33)

start_button = Button(text="Start", highlightbackground=GREY, command=start_timer)
start_button.place(x=10, y=530)

completed_sessions = Label(text=f"Newton work sessions completed: {reps_done}", fg=PURPLE, bg=GREY)
completed_sessions.place(x=111, y=535)

reset_button = Button(text="Reset", highlightbackground=GREY, command=reset)
reset_button.place(x=360, y=530)

window.mainloop()