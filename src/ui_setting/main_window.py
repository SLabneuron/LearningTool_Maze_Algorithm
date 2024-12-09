# -*- coding: utf-8 -*-

"""

Created on Thu Mar 14, 2024

@author: shriafujilab

Purpose:
    The code privide GUI config

"""

# import standard library
import tkinter as tk
from tkinter import ttk
import sys


# import my library

# maze algorithms
from src.maze_exploration.maze import Maze
from src.maze_exploration.mouse import MicroMouse
from src.maze_exploration.maze_pygame import MazeRunning

# frames
from src.ui_setting.control_and_console import micro_mouse_debug_cont


# tabs
from src.ui_setting.tabs.tab_initial import TabInit
from src.ui_setting.tabs.tab_block_code import TabBlockCode
from src.ui_setting.tabs.tab_practice import set_practice_tab
from src.ui_setting.tabs.tab_manual import set_manual_tab



class MainWindow:

    def __init__(self, root, params):

        """ Initialize """

        # get initial params
        self.root = root
        self.params = params

        # for storing attribute of tkinter objects

        self.entries ={}
        self.combos = {}
        self.method = "左手法"

        """ maze and mouse """
        self.maze = Maze(self, self.params, self.entries)
        self.mouse = MicroMouse(self, self.params, self.entries, self.maze.init_pos, "down")

        self.create_widgets()


    def create_widgets(self):


        # Create control frame
        frame1 = ttk.Frame(self.root, style="Co.TFrame", height=400, width=320, padding = "3 3 12 12")
        frame1.grid(row=0, column=0, sticky="nsew")
        self.create_control_frame(frame1)

        # Create aimation frame (frame only here)
        frame2 = ttk.Frame(self.root, style="An.TFrame", height=400, width = 480, padding="3 3 12 12")
        frame2.grid(row=0, column=1, sticky="nsew")
        self.main_code = MazeRunning(self, self.params, self.entries, frame2)

        # Create Interactive Frame()
        frame3 = ttk.Frame(self.root, style="Intract.TFrame", height=100, width=800, padding="3 3 12 12")
        frame3.grid(row=1, column=0, columnspan =2, sticky="nsew")
        micro_mouse_debug_cont(self, frame3)
        
        self.console =tk.Text(self.root, width=120, height=2)
        self.console.grid(row=1, column=1, sticky="nsw")
        sys.stdout = self


    def write(self, msg):

        self.console.insert(tk.END, msg)
        self.console.see(tk.END)           # Scroll to the end

    def flush(self):

        pass

    def create_control_frame(self, frame):

        notebook = ttk.Notebook(frame, height=380, width=300, padding="3 3 3 3")
        notebook.grid(row=0, column=0, padx=10, pady=10)

        """ Set Tabs """

        # Tab1: Introduction
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Introduction")
        TabInit(self, tab1)

        # Tab2: editor
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Basic")
        self.block_pg_editor = TabBlockCode(self, tab2)

        # Tab3: practice
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="Practice")
        set_practice_tab(tab3)

        # Tab4: 
        tab4 = ttk.Frame(notebook)
        notebook.add(tab4, text="Manual")
        set_manual_tab(tab4)



    def run(self):

        self.main_code.initialize_pygame()
