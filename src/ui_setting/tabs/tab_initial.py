# -*- coding: utf-8 -*-

"""

Created on: 2024-12-05

@author:  shirafujilab

Contents:

    Initial Screen




"""

# import standard library

import tkinter as tk
from tkinter import ttk
from tkinter import font

import webbrowser



class TabInit:

    def __init__(self, master, tab):

        # get parent instance
        self.master = master

        # attributes

        self.master.combos["method"] = None
        self.master.entries["maze_width_config"] = None
        self.master.entries["maze_height_config"] = None

        # Setup
        self.setup_frames(tab)


    def setup_frames(self, tab):

        """ frames """

        # set 1
        frame1 = ttk.Frame(tab)
        frame1.grid(row=0, column=0, sticky=tk.W)
        self.set_run_simulation(frame1)

        blank1 = ttk.Label(tab, text = " ")
        blank1.grid(row=1, column=0, sticky=tk.W)

        # set 2
        frame2 = ttk.Frame(tab)
        frame2.grid(row=2, column=0, sticky=tk.W)
        self.set_regenerating_maze(frame2)

        blank2 = ttk.Label(tab, text=" ")
        blank2.grid(row=3, column=0, sticky=tk.W)

        # set 3
        frame3 = ttk.Frame(tab)
        frame3.grid(row=4, column=0, sticky=tk.W)
        self.set_more_information(frame3)


    def set_run_simulation(self, frame):

        """ run simulation """

        # title
        text = ttk.Label(frame, text="迷路探索")
        text.grid(row=0, column=0, columnspan=2, sticky=tk.W)

        # combobox
        combo = ttk.Combobox(frame)
        combo["values"] = ("左手法", "None")
        combo.current(0)
        combo.grid(row=1, column = 0)
        self.master.combos["method"] = combo

        # execute the method
        def running():
            self.master.method = self.master.combos["method"].get()
            self.master.run()

        button2 = ttk.Button(frame, text="実行", command=running)
        button2.grid(row=1, column=1)


    def set_regenerating_maze(self, frame):

        """ Regenarate and default setting """

        # set title (迷路生成)
        text1 = ttk.Label(frame, text="迷路作成")
        text1.grid(row=0, column=0, columnspan=5, sticky=tk.W)

        """ Template regeneration """
        label1 = ttk.Label(frame, text='課題 1用迷路 再生成 ')
        label1.grid(row=1, column=0, columnspan=4, sticky=tk.W)

        def default_maze():

            # default
            self.master.maze.default_maze()
            
            # reset position
            self.master.mouse.position = self.master.maze.init_pos

        button1 = ttk.Button(frame, text="課題用再生成", command=default_maze)
        button1.grid(row=1, column=4, sticky=tk.W)

        """ regeneration """

        # setting width of maze
        label2 = ttk.Label(frame, text="width")
        label2.grid(row=2, column=0)

        entry1 = ttk.Entry(frame, width=5)
        entry1.grid(row=2, column = 1)
        entry1.insert(0, 16)
        self.master.entries["maze_width_config"] = entry1

        # setting height of maze
        label3 = ttk.Label(frame, text="height")
        label3.grid(row=2, column=2)

        entry2 = ttk.Entry(frame, width=5)
        entry2.grid(row=2, column = 3)
        entry2.insert(0, 16)
        self.master.entries["maze_height_config"] = entry2

        def regenerate_maze1():

            # default
            self.master.maze.regenerate_maze()

            # reset position
            self.master.mouse.position = self.master.maze.init_pos

        button2 = ttk.Button(frame, text="新規生成", command=regenerate_maze1)
        button2.grid(row=2, column=4)


    def set_more_information(self, frame):

        """ Information (Github link) """

        def open_url(event):
            webbrowser.open_new("https://github.com/SLabneuron/LearningTool_Maze_Algorithm")

        text = ttk.Label(frame, text="今後の更新が知りたい方はこちら")
        text.grid(row=0, column=0, columnspan=2, sticky=tk.W)

        custom_font = font.Font(family="Helvetica", size=8)
        url = tk.Label(frame, text="https://github.com/SLabneuron/LearningTool_Maze_Algorithm", fg="blue", cursor="hand2", font=custom_font)
        url.grid(row=1, column=0, columnspan=2, sticky=tk.W)
        url.bind("<Button-1>", open_url)


