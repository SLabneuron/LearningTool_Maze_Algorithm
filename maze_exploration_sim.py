# -*- coding: utf-8 -*-
"""
Created on: 2024-03-14
Updated on: 2024-12-05

@author: shirafujilab

Contents:

        1. Learning Tool for Maze Exploration Algorithm
        2. Blockprogramming for beginer of programming
        3. Preparing ...


"""


# Import necessary modules
import os
import tkinter as tk
from tkinter import ttk


# import my libraries
from src.ui_setting.main_window import MainWindow  # Main GUI window configuration


class ControlPanel:

    def __init__(self):

        """ Initialize root and params, and Config """

        # Definition root window
        self.root = tk.Tk()
        self.root_config()

        # Definition Params
        self.params = {

            "root_dir" : os.getcwd(),
            "maze_width_pixel": 480,
            "maze_height_pixel": 400,

            "method" : "左手法",

        }

        # Set widgets
        self.main_window = MainWindow(self.root, self.params)


    def run(self):

        self.root.mainloop()


    def root_config(self):

        """ Size of Simulator """

        self.root.title("Micro Mouse Simulator")    # Title
        self.root.geometry("800x600")               # Initial size of the root window
        self.root.minsize(800,600)                  # Minimum size of the root window

        self.other_settings()


    def other_settings(self):

        # Config Style of Main Frame
        style = ttk.Style()

        # controller background
        style.configure("Co.TFrame", background="gray")

        # animation background
        style.configure("An.TFrame", background="cyan")

        # interactive mode background
        style.configure("Intract.TFrame", background="lightgray")


if __name__ == "__main__":

    # Create an instance of ControlPanel with initial parameters
    control_panel = ControlPanel()
    control_panel.run()