"""

Created on Thu Mar 14, 2024

@author: shriafujilab

Purpose:
    The code privide GUI config

"""

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import sys
import os



class MainWindow:
    def __init__(self, master, params, config):
        """Initialize the main window"""
        self.master = master
        self.params = params
        self.config = config

        self.entries ={}

        self.create_widgets()



    def create_widgets(self):

        # Create control frame
        self.create_control_frame()

        # Create aimation frame
        self.create_animation_frame()
        
        # Create Interactive Frame()
        self.create_interactive_frame()

        # Figure configure
        #self.root.rowconfigure(0, weight=2)
        #self.root.rowconfigure(1, weight=3)
        #self.root.rowconfigure(2, weight=1)
        #self.root.rowconfigure(3, weight=1)


    def create_control_frame(self):

        # Config Style of Main Frame
        style = ttk.Style()
        style.configure("Co.TFrame", background="gray")

        # Create Main Frame (control)
        main_frame = ttk.Frame(self.master.root, style="Co.TFrame", height=400, width=320, padding = "3 3 12 12")
        main_frame.grid(row=0, column=0, sticky="nsew")

        notebook = ttk.Notebook(main_frame, height=380, width=300, padding="3 3 3 3")
        notebook.grid(row=0, column=0, padx=10, pady=10)

        # Tab1: Introduction
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Introduction")
        self.setting_tab1(tab1)

        # Tab2: Introduction
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Basic")
        self.setting_tab2(tab2)

        # Tab3: Introduction
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="Practice")
        self.setting_tab3(tab3)


    def setting_tab1(self, tab):

        pass


    def setting_tab2(self, tab):

        pass


    def setting_tab3(self, tab):

        pass


    def create_animation_frame(self):

        # Config Style of Main Frame
        style = ttk.Style()
        style.configure("An.TFrame", background="cyan")

        # Create Main Frame (animation)
        self.animation_frame = ttk.Frame(self.master.root, style="An.TFrame", height=400, width = 480, padding="3 3 12 12")
        self.animation_frame.grid(row=0, column=1, sticky="nsew")


    def create_interactive_frame(self):

        # Config Style of Main Frame
        style = ttk.Style()
        style.configure("Intract.TFrame", background="lightgray")

        # Config Interactive Frame
        main_frame = ttk.Frame(self.master.root, style="Intract.TFrame", height=100, width=800, padding="3 3 12 12")
        main_frame.grid(row=1, column=0, columnspan =2, sticky="nsew")

        self.micro_mouse_debug_controller(main_frame)


    def micro_mouse_debug_controller(self, main_frame):

        # left frame (blank)
        frame01 = ttk.Frame(main_frame, style="Intract.TFrame", height=100, width=320, padding="3 3 12 12")
        frame01.grid(row=0, column=0,sticky="nsew")

        # right frame (controller)
        frame02 = ttk.Frame(main_frame, style="Intract.TFrame", height=100, width=480, padding="3 3 12 12")
        frame02.grid(row=0, column=1,sticky="nsew")

        # blanks
        blank1 = ttk.Frame(frame02, height=30, width=100)
        blank1.grid(row=0, column=0, sticky="nsew")

        blank2 = ttk.Frame(frame02, height=30, width=100)
        blank2.grid(row=0, column=2, sticky="nsew")

        """ buttons click """

        # buttons
        button_up = tk.Button(frame02, text="up", command=lambda: self.master.cursor_click("up"))
        button_up.grid(row=0, column=1, sticky = "nsew")
        button_up.bind()

        button_lf = tk.Button(frame02, text="left", command=lambda: self.master.cursor_click("left"))
        button_lf.grid(row=1, column=0, sticky = "nsew")

        button_dw = tk.Button(frame02, text="down", command=lambda: self.master.cursor_click("down"))
        button_dw.grid(row=1, column=1, sticky = "nsew")

        button_rg = tk.Button(frame02, text="right", command=lambda: self.master.cursor_click("right"))
        button_rg.grid(row=1, column=2, sticky = "nsew")
        
        self.text = tk.Text(frame02, width=30, height=2)
        self.text.grid(row=0, column=3, rowspan=2, sticky="nsw")
        
        sys.stdout = self

    def write(self, msg):

        self.text.insert(tk.END, msg)
        #self.text.see(tk.END)  # Scroll to the end
    
    def flush(self):
        
        pass






