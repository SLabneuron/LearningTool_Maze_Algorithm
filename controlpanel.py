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



from src.graphics.Animation_Mouse import Animation  # Graphical plotting of characteristics
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
            
            
        }

        # Definition Configs
        self.config = {
            "haxis" : "log",        # horizontal-axis
            "vaxis": "log",         # vertical-axis
            "xlim_left" : 0,        # left of xlim
            "xlim_right": 10000,    # right of xlim
            "ylim_left" : -20,      # left of ylim
            "ylim_right": 0,        # right of ylim
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

        # Set up Figure canvas
        self.animation = Animation(self, self.params, self.config, self.main_window.animation_frame)



    def cursor_click(self, direction):
        
        self.main_window.entries["direction_btn"] = direction
        self.animation.move_mouse()
    
    def output_console(self, state):
        
        if state == "2":
            print("*** Go for the goal!! ***")
        if state == "3":
            print("*** Congratulations!! ***")





if __name__ == "__main__":

    # Create an instance of ControlPanel with initial parameters
    control_panel = ControlPanel()
    control_panel.run()