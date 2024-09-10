# -*- coding: utf-8 -*-
"""
Created on Mon July 9, 2024

@author: shirafujilab
"""

import sys
import os
import tkinter as tk
import pygame
import threading

class Animation:
    def __init__(self, master, params, config, main_frame):
        """
        Initialize Graphics
        master: widget of Tkinter
        """

        # Get components
        self.master = master
        self.params = params
        self.config = config
        self.main_frame = main_frame
        self.load_image()
        self.running = True
        self.console_flag = True

        self.maze = [
            "1111111111111111",
            "1000000000000001",
            "1011111111111101",
            "1010000000000101",
            "1010111111111101",
            "1010100010000101",
            "1010101010100101",
            "1010101010100101",
            "1010101010100101",
            "1010101010100101",
            "1010101310100101",
            "1010101110100101",
            "1010100000100101",
            "1010111111100101",
            "1210000000000001",
            "1111111111111111"
        ]

        self.mouse_position = [1, 14]
        self.mouse_direction = "down"

        # Set Window Config
        self.set_frame_config()
        self.initialize_pygame()
        #self.initialize_figure()



    def set_frame_config(self):

        # Determine OS
        def set_sdl_driver():
            if sys.platform == "win32":
                os.environ['SDL_VIDEODRIVER'] = 'windib'
            elif sys.platform == "linux" or sys.platform == "linux2":
                os.environ['SDL_VIDEODRIVER'] = 'x11'
            elif sys.platform == "darwin":
                os.environ['SDL_VIDEODRIVER'] = 'cocoa'

        set_sdl_driver()
        os.environ["SDL_WINDOWID"] = str(self.main_frame.winfo_id())


    def initialize_pygame(self):

        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))
        threading.Thread(target=self.pygame_loop, daemon=True).start()


    def pygame_loop(self):
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill((240, 240, 240))

            # maze regeneration each frame
            self.draw_maze()

            # draw micro mouse
            current_image = self.images[self.mouse_direction]
            self.screen.blit(current_image, (self.mouse_position[0]*20, self.mouse_position[1]*20))
            pygame.display.update()
            
            if self.console_flag: self.master.output_console(self.maze[self.mouse_position[1]][self.mouse_position[0]])
            self.console_flag = False
            
            clock.tick(30)


    def draw_maze(self):

        # Create default maze pattern (10x5)

        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == '1':  # Wall
                    pygame.draw.rect(self.screen, (0, 0, 0), [x*20, y*20, 20, 20])
                elif cell == "2":# Start
                    pygame.draw.rect(self.screen, (0, 80, 0), [x*20, y*20, 20, 20])
                elif cell == "3":# End
                    pygame.draw.rect(self.screen, (120, 0, 0), [x*20, y*20, 20, 20])


    def move_mouse(self):

        direction = self.master.main_window.entries["direction_btn"]
        deltas = {'up': (0, -1), 'left': (-1, 0), 'down': (0, 1), 'right': (1, 0),}
        delta = deltas.get(direction, (0, 0))
        new_x = self.mouse_position[0] + delta[0]
        new_y = self.mouse_position[1] + delta[1]
        if new_x in range(0, len(self.maze[0])) and new_y in range(0, len(self.maze)):
            if self.maze[new_y][new_x] != "1":
                self.mouse_position = [new_x, new_y]
                self.mouse_direction = direction
        
        

        self.console_flag = True

    """
    def left_hand_method(self):

        directions = [(-1, 0), (0,-1), (1, 0), (0, 1)]          # up, left, down, right

        while self.maze[self.mouse_position[1]][self.mouse_position[0]] != "3":
            
            left_index = self.find_initial_direction()
            left_dx, left_dy = directions[left_index]
            leftx = self.mouse_position[0] + left_dx
            lefty = self.mouse_position[1] + left_dy
        
    """

    def load_image(self):

        image_path = os.path.join(self.params["root_dir"], "src","images")
        
        up_path = os.path.join(image_path, "down.png")
        back_path = os.path.join(image_path, "up.png")
        left_path = os.path.join(image_path, "left.png")
        right_path = os.path.join(image_path, "right.png")

        self.images = {
            "up": pygame.image.load(up_path),
            "down": pygame.image.load(back_path),
            "left": pygame.image.load(left_path),
            "right": pygame.image.load(right_path),
        }

        for key in self.images:
            self.images[key] = pygame.transform.scale(self.images[key], (20, 20))
