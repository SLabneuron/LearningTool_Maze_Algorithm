# -*- coding: utf-8 -*-

"""
Created on: 2024-07-09

@author: shirafujilab

Content:

        Maze


"""

# import standard library
import tkinter as tk
from tkinter import ttk


def micro_mouse_debug_cont(master, frame):

    # left frame (controller)
    fr_l = ttk.Frame(frame, style="Intract.TFrame", height=100, width=480, padding="3 3 12 12")
    fr_l.grid(row=0, column=1,sticky="nsew")

    # blanks
    blank1 = ttk.Frame(fr_l, height=30, width=100)
    blank1.grid(row=0, column=0, sticky="nsew")

    blank2 = ttk.Frame(fr_l, height=30, width=100)
    blank2.grid(row=0, column=2, sticky="nsew")

    # click event
    def cursor_click(direction):

        master.entries["direction_btn"] = direction
        master.mouse.move_mouse(master.maze.maze, btn_dir=direction)

    # buttons
    button_up = tk.Button(fr_l, text="↑", command=lambda: cursor_click("up"))
    button_up.grid(row=0, column=1, sticky = "nsew")

    button_lf = tk.Button(fr_l, text="←", command=lambda: cursor_click("left"))
    button_lf.grid(row=1, column=0, sticky = "nsew")

    button_dw = tk.Button(fr_l, text="↓", command=lambda: cursor_click("down"))
    button_dw.grid(row=1, column=1, sticky = "nsew")

    button_rg = tk.Button(fr_l, text="→", command=lambda: cursor_click("right"))
    button_rg.grid(row=1, column=2, sticky = "nsew")


    

