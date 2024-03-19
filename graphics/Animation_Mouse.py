# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19, 2024

@author: shirafujilab
"""

import tkinter as tk

class Animation:
    def __init__(self, master):
        """
        Initialize Graphics
        master: widget of Tkinter
        """

        # Parent class root
        self.master = master

        # Create default maze pattern (10x5)
        init_maze = [
            "1111111111",
            "1000100001",
            "1010101011",
            "1000000011",
            "1111111111"
        ]

        self.maze = [list(row) for row in init_maze] # Transger init_maze to 2d list
        self.initialize_figure()       # Graphic maze


    def initialize_figure(self):

        self.canvas = tk.Canvas(self.master, width = 600, height = 300)
        self.canvas.grid(row=0, column=1, pady=5, sticky="nsew")
        self.draw_maze()
        self.mouse = self.canvas.create_rectangle(0, 0, 20, 20, fill="blue")


    def draw_maze(self):
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == '1':  # Wall
                    self.canvas.create_rectangle(
                        x*20, y*20, (x+1)*20, (y+1)*20,
                        fill="black"
                    )


    def start_mouse_animation(self):
        # Animation of the Mouse
        path = [(0, 1), (0, 2), (1, 2), (2, 2)]
        self.animate_mouse(path)


    def animate_mouse(self, path):
        if path:
            next_x, next_y = path.pop(0)
            current_x1, current_y1, current_x2, current_y2 = self.canvas.coords(self.mouse)
            move_x, move_y = (next_x * 20 - current_x1), (next_y * 20 - current_y1)
            self.canvas.move(self.mouse, next_x, next_y)
            self.master.after(500, self.animate_mouse, path)


if __name__ == "__main__":
    root = tk.Tk()
    app = Animation(root)
    root.after(1000, app.start_mouse_animation)
    root.mainloop()