
# monthly expense and budget estimator.

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3


def firstwin():
    global font1, font2, uname
    win1 = Tk()
    win1.title("Log in")
    win1.geometry('1000x600')
    win1.maxsize(1000, 600)
    win1.minsize(1000, 600)

    font1 = ("Harlow Solid Italic", 25, )
    font2 = ("Roboto Mono", 18)

    f1 = Frame(win1, height=600, width=1000, bg="#8ecae6")
    f1.propagate(0)
    f1.place(x=0, y=0)

    uname = StringVar()
    password = StringVar()