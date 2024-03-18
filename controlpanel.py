# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14, 2024

@author: shirafujilab

Purpose:
    ControlPanel: Handles the initialization and configuration of the main GUI window,
    integrates with the Graphics module for plotting, and sets up the initial parameters for the application.


"""

# Import necessary modules
import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


from graphics.graphics import Graphics  # Graphical plotting of characteristics
from GUI.main_window import MainWindow  # Main GUI window configuration
from sims.lpf import LPF
from sims.hpf import HPF
from sims.bpf import BPF


class ControlPanel:
    def __init__(self, init_params):
        """Initialize ControlPanel with given parameters and setup the GUI."""
        # graphic array
        self.freq = np.arange(0, 10000, 1)
        self.results_amp = np.full(10000, 0)
        self.results_freq = np.full(10000, 0)

        # init parameter
        self.params = init_params  # Store initial parameters for later use

        # config
        self.config = {
            "haxis" : "log",        # horizontal-axis
            "vaxis": "log",         # vertical-axis
            "xlim_left" : 0,        # left of xlim
            "xlim_right": 10000,    # right of xlim
            "ylim_left" : -20,      # left of ylim
            "ylim_right": 0,        # right of ylim
        }

        # init tkinter
        self.root = tk.Tk()

        # Set widgets
        self.set_widget()


    def run(self):
        """GUI Loop"""
        self.root.mainloop()


    def set_widget(self):
        # Initialize GUI
        self.root.title("Control Panel")    #Set a title for the window
        self.root.geometry("800x600")   # Initial size of the main window
        self.root.minsize(800,600)      # Minimum size of the main window

        # Set up MainWindow
        self.setupMainWindow()

        # Set up Figure canvas
        self.graphic_results = Graphics(self.root)

        self.create_output_console()

        self.create_plot_area()

        # Set up Buttons
        self.create_buttons()


    def setupMainWindow(self):
        """Set up MainWindow"""
        self.main_window = MainWindow(self.params, self.root)


    def create_output_console(self):
        """Set up Output Console"""
        self.output_console = tk.Text(self.root, height=2, state=tk.DISABLED)
        self.output_console.grid(row=2, column=0)


    def create_buttons(self):
        """Set Buttons"""
        calculate_button = ttk.Button(self.root, padding=10, text="Calc.", command=self.calculate_and_plot)
        calculate_button.grid(row=3, column=0)


    def create_plot_area(self):
        """Create and embed a figure in the Tkinter window for plotting."""

        # Examplt plot
        self.calculate_and_plot() # Plots test data


    def calculate_and_plot(self):

        # Get parameter and filter type from GUI
        params = self.main_window.get_parameter_values()
        filter_type = self.main_window.filter_type.get()

        # Calling adequately functions
        if filter_type == "LPF":
            self.results_amp, self.results_freq, cutoff_freq = LPF.calculate_response_lpf(params, self.freq)
        elif filter_type == "HPF":
            self.results_amp, self.results_freq, cutoff_freq = HPF.calculate_response_hpf(params, self.freq)
        elif filter_type == "BPF":
            self.results_amp, self.results_freq, lower_cutoff_freq, upper_cutoff_freq  = BPF.calculate_response_bpf(params, self.freq)

        self.graphic_results.initialize_figure()
        self.graphic_results.plot_results_amp(self.config, filter_type, self.freq, self.results_amp)
        self.graphic_results.plot_results_phase(self.config, filter_type, self.freq, self.results_freq)

        # Output logs every filter
        print(filter_type)
        if (filter_type == "LPF") or (filter_type == "HPF"):
            console_text1 = f"          Filter type : {filter_type}"
            console_text2 = f"-3dB cutoff frequency : {cutoff_freq}Hz "
        elif filter_type == "BPF":
            console_text1 = f"          Filter type : {filter_type}"
            console_text2 = f"    Bandwidth at -3dB : {lower_cutoff_freq}Hz ~ {upper_cutoff_freq}Hz"
        self.output_console.config(state=tk.NORMAL) # Enable to edit text widget
        self.output_console.delete("1.0", tk.END)
        self.output_console.insert(tk.END, console_text1 + "\n" + console_text2)
        self.output_console.config(state=tk.DISABLED) # Unable to edit text widget


if __name__ == "__main__":
    """Initial paramters for the application, used for setup or configuration"""
    init_params = {
        "R1": {"value": 10, "unit": "kohm"},
        "R2": {"value": 10, "unit": "kohm"},
        "C1": {"value": 0.1, "unit": "uF"},
        "C2": {"value": 0.01, "unit": "uF"},
    }

    # Create an instance of ControlPanel with initial parameters
    control_panel = ControlPanel(init_params)
    control_panel.run()