# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14, 2024

@author: shirafujilab

Purpose:
    ControlPanel: Handles the initialization and configuration of the main GUI window,
    integrates with the Graphics module for plotting, and sets up the initial parameters for the application.


"""

# Import necessary modules
import os
import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure



from src.graphics.Animation_Mouse import MazeExploration  # Graphical plotting of characteristics
from src.GUI.main_window import MainWindow  # Main GUI window configuration


class ControlPanel:

    def __init__(self):

        """Initialize root and params, and Config """

        # Definition root window
        self.root = tk.Tk()
        self.root_config()

        cwd = os.getcwd()

        # Definition Params
        self.params = {

            "root_dir" : cwd,

            "method" : "左手法",

        }

        # Definition Configs
        self.config = {
            "maze_width": 16,
            "maze_height": 16,

            "maze_width_pixel": 480,
            "maze_height_pixel": 400,

        }


        # Set widgets
        self.set_widget()


    def run(self):

        """GUI Loop"""

        self.root.mainloop()


    def root_config(self):
        self.root.title("Micro Mouse Simulator")    # Title
        self.root.geometry("800x600")               # Initial size of the root window
        self.root.minsize(800,600)                  # Minimum size of the root window


    def set_widget(self):

        # Set up MainWindow
        self.main_window = MainWindow(self, self.params, self.config)

        # Set up Maze and Mouse
        self.maze = MazeExploration(self, self.params, self.config, self.main_window.animation_frame)


    def cursor_click(self, direction):

        self.main_window.entries["direction_btn"] = direction
        self.maze.mouse.move_mouse(self.maze.maze, btn_dir=direction)


    def regeneration(self):

        # Maze regeneration
        self.maze.maze_regeneration()

        # Start main program
        self.maze.initialize_pygame()


    def exploration(self):

        # Start main program
        self.maze.initialize_pygame()


    def output_console(self, state):

        if state == "2":
            print("*** Go for the goal!! ***")

        if state == "3":
            print("*** Congratulations!! ***")





if __name__ == "__main__":

    # Create an instance of ControlPanel with initial parameters
    control_panel = ControlPanel()
    control_panel.run()