from tkinter import *
from tkinter import messagebox
import math
import simpleaudio as sa
from PIL import ImageTk, Image
import sys
import os
# ---------------------------- CONSTANTS ------------------------------- #
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

newton_jpeg_path = os.path.join(application_path, 'Newton.jpeg')
green_lion_png_path = os.path.join(application_path, 'green-lion-rosarium-philosophorum-hedesan-coloured.png')
sfx_1_path = os.path.join(application_path, 'bell.wav')
sfx_2_path = os.path.join(application_path, 'bell-2.wav')

GREY = "#413543"
YELLOW = "#F0EB8D"
FONT_NAME = "Georgia"
WORK_MIN = 0 
SHORT_BREAK_MIN = 0
LONG_BREAK_MIN = 0
timer = None
timer_text = ""
reps_done = 0
short_breaks_seq = [1, 3, 4, 6, 7, 9, 10, 12, 13, 15, 16, 18]
long_breaks_seq = [2, 5, 8, 11, 14, 17, 19]
breaks_taken = 0
breaktime = False
worktime = False

# -- initialise sound files
bell_sound_1 = sa.WaveObject.from_wave_file(sfx_1_path)

bell_sound_2 = sa.WaveObject.from_wave_file(sfx_2_path)

# ---------------------------- TIMER RESET ------------------------------- #
def reset():

    global reps_done, breaks_taken, breaktime, worktime

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

    global reps_done, breaks_taken, breaktime, worktime

    if breaktime or worktime:
        pass

    else:

        # start short break
        if reps_done > breaks_taken and reps_done in short_breaks_seq:
            bell_sound_2.play()
            breaks_taken += 1
            breaktime = True
            countdown(SHORT_BREAK_MIN * 60)
            title.config(text="'Nature is pleased with simplicity. And nature is no dummy'",
                         fg=YELLOW, font=(FONT_NAME, 16))
            title.place(x=2, y=-27)

        # start long break
        elif reps_done > breaks_taken and reps_done in long_breaks_seq:
            bell_sound_2.play()
            breaks_taken += 1
            breaktime = True
            countdown(LONG_BREAK_MIN * 60)
            title.config(text="'To myself I am only a child playing on the beach, \nwhile "
            "vast oceans of truth lie undiscovered before me'", fg=YELLOW, font=(FONT_NAME, 13))
            title.place(x=60, y=-39)

        # start work session
        elif reps_done == breaks_taken:
            bell_sound_1.play()
            reps_done += 1
            worktime = True
            countdown(WORK_MIN * 60)
            title.config(text="'What we know is a drop, what we don't know is "
            "an ocean.'", fg=YELLOW, font=(FONT_NAME, 16))
            title.place(x=5, y=-27)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def countdown(count):

    global worktime, breaktime

    if count > 0:
        global timer
        timer = window.after(1000, countdown, count - 1)
    else:
        completed_sessions.config(text=f"Newton work sessions completed: {reps_done}")
        worktime = False
        breaktime = False
        start_timer()

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
def tab(event):
    event.widget.tk_focusNext().focus()        
    return "break"

window = Tk()
window.title("NWS")
window.config(padx=111, pady=55, bg=GREY)

# -- initialise main screen
def main_screen(event, work, short_break, long_break):
    global WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN, timer_text

    try:
        WORK_MIN = int(work.get(1.0, "end-1c"))
        SHORT_BREAK_MIN = int(short_break.get(1.0, "end-1c"))
        LONG_BREAK_MIN = int(long_break.get(1.0, "end-1c"))

        if SHORT_BREAK_MIN > WORK_MIN:  
            messagebox.showerror("Invalid input", "Work time must be greater than break time.")
            short_break_input.focus()
            return
        elif LONG_BREAK_MIN > WORK_MIN:
            messagebox.showerror("Invalid input", "Work time must be greater than break time.")
            long_break_input.focus()
            return
        elif WORK_MIN > 90:
            messagebox.showerror("Invalid input", "Please enter a time of between 1-90 minutes.")
            work_min_input.focus()
            return

        work_min_input.destroy()
        work_min_input_lbl.destroy()
        short_break_input.destroy()
        short_break_input_lbl.destroy()
        long_break_input.destroy()
        long_break_input_lbl.destroy()

        canvas.create_image(220, 265, image=Newton_img)
        timer_text = canvas.create_text(220, 290, text="0:00:00", fill=YELLOW, font=(FONT_NAME, 33))
        start_button.place(x=10, y=540)
        completed_sessions.place(x=90, y=545)
        reset_button.place(x=360, y=540)
        title.place(x=111, y=-33)
    
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter an amount of minutes for each field.")
    

# -- start screen
canvas = Canvas(width=440, height=530, highlightthickness=0)

work_min_input = Text(canvas, height = 1, width = 3, background="#FFD700", foreground="#022C43", font=(FONT_NAME, 22))
work_min_input.bind("<Tab>", tab)
work_min_input.place(x=50, y=225)
work_min_input_lbl = Label(text="Work session\nminutes:", fg=YELLOW, font=(FONT_NAME, 16))
work_min_input_lbl.place(x=25, y=180)

short_break_input = Text(canvas, height = 1, width = 3, background="#FFD700", foreground="#022C43", font=(FONT_NAME, 22))
short_break_input.bind("<Tab>", tab)
short_break_input.place(x=185, y=225)
short_break_input_lbl = Label(text="Short break\nminutes:", fg=YELLOW, font=(FONT_NAME, 16))
short_break_input_lbl.place(x=175, y=180)

long_break_input = Text(canvas, height = 1, width = 3, background="#FFD700", foreground="#022C43", font=(FONT_NAME, 22))
long_break_input.bind("<Tab>", tab)
long_break_input.place(x=320, y=225)
long_break_input_lbl = Label(text="Long break\nminutes:", fg=YELLOW, font=(FONT_NAME, 16))
long_break_input_lbl.place(x=310, y=180)

work_min_input.bind("<Return>", lambda event, w=work_min_input, sb=short_break_input, lb=long_break_input: 
                    main_screen(event, w, sb, lb))
short_break_input.bind("<Return>", lambda event, w=work_min_input, sb=short_break_input, lb=long_break_input: 
                    main_screen(event, w, sb, lb))
long_break_input.bind("<Return>", lambda event, w=work_min_input, sb=short_break_input, lb=long_break_input: 
                    main_screen(event, w, sb, lb))

canvas.grid(column=1, row=1)

# -- static files
Newton_img = ImageTk.PhotoImage(Image.open(newton_jpeg_path))

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
start_button = Button(text="Start", highlightbackground=GREY, font=(FONT_NAME, 16), command=start_timer)
completed_sessions = Label(text=f"Newton work sessions completed: {reps_done}", fg=YELLOW, bg=GREY, font=(FONT_NAME, 16))
reset_button = Button(text="Reset", highlightbackground=GREY, font=(FONT_NAME, 16), command=reset)

work_min_input.focus()

window.mainloop()