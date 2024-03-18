# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18, 2024

@author: shirafujilab
"""

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.gridspec as gridspec


class Graphics:
    def __init__(self, master):
        """
        Initialize Graphics
        master: widget of Tkinter
        """

        self.master = master
        self.initialize_figure()


    def initialize_figure(self):
        self.fig = Figure(figsize=(8, 3), dpi = 100)
        self.gs = gridspec.GridSpec(2, 3, height_ratios= [5,1], width_ratios= [6,1,6], figure = self.fig)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().grid(row=1, column=0, pady=5, sticky="nsew")
        self.ax1 = self.fig.add_subplot(self.gs[0, 0])
        self.ax2 = self.fig.add_subplot(self.gs[0, 2])
        self.canvas.draw()


    def plot_results_amp(self, config, filter_type, freq, amp_response):

        """
        Graphic amplotude characteristics
        config = {
            "haxis": "linear" or "log",
            "vaxis": "linear" or "log",
            "amp_mode": "normal" or "dB",
            "xlim_left" : num,        # left of xlim
            "xlim_right": num,    # right of xlim
            "ylim_left" : num,      # left of ylim
            "ylim_right": num,        # right of ylim
        }
        freq: numpy array
        amp_resoponse: numpy array
        """

        # clear plot
        self.ax1.clear()

        # plot
        self.ax1.plot(freq, amp_response)

        # Set horizontal axis
        if config["haxis"] == "log":
            self.ax1.set_xscale("log")
            self.ax1.set_xlabel("Frequency [Hz]")
            self.ax1.set_xlim(config["xlim_left"], config["xlim_right"])
        else:
            self.ax1.set_xscale("linear")
            self.ax1.set_xlabel("Frequency [Hz]")
            self.ax1.set_xlim(config["xlim_left"], config["xlim_right"])

        # Set vertical axis
        if config["vaxis"] == "log":
            self.ax1.set_yscale("log")
            self.ax1.set_ylabel("Gain [dB]")
            self.ax1.set_ylim(config["ylim_left"], config["ylim_right"])
        else:
            self.ax1.set_yscale("linear")
            self.ax1.set_ylabel("|Vout/Vin|")
            self.ax1.set_ylim(config["ylim_left"], config["ylim_right"])

        self.ax1.set_title("Amplitude Response")
        self.ax1.grid(color="black", linewidth = 0.2, which="minor", axis="both")
        self.ax1.grid(color="black", linewidth = 0.8, which="major", axis="both")
        self.canvas.draw()


    def plot_results_phase(self, config, filter_type, freq, ph_response):

        """
        Graphic amplotude characteristics
        config: same as results_amp
        freq: numpy array
        amp_resoponse: numpy array
        """

        # clear plot
        self.ax2.clear()

        # plot
        self.ax2.plot(freq, ph_response, ".", markersize=1.2)

        # Set horizontal axis
        if config["haxis"] == "log":
            self.ax2.set_xscale("log")
            self.ax2.set_xlabel("Frequency [Hz]")
            self.ax2.set_xlim(config["xlim_left"], config["xlim_right"])
        else:
            self.ax2.set_xscale("linear")
            self.ax2.set_xlabel("Frequency [Hz]")
            self.ax2.set_xlim(config["xlim_left"], config["xlim_right"])

        self.ax2.set_yscale("linear")
        self.ax2.set_ylabel("Phase [degrees]")
        
        if filter_type == "LPF": self.ax2.set_ylim(90, 200)
        elif filter_type == "HPF": self.ax2.set_ylim(-200, -90)
        else: self.ax2.set_ylim(-200,  200)

        self.ax2.set_title("Phase Response")
        self.ax2.grid(color="black", linewidth = 0.2, which="minor", axis="both")
        self.ax2.grid(color="black", linewidth = 0.8, which="major", axis="both")
        self.canvas.draw()