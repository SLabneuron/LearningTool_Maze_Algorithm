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
import random

class MazeExploration:

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

        self.running = True
        self.explore_flag = True
        
        self.max_width_pixel = self.config["maze_width_pixel"]
        self.max_height_pixel = self.config["maze_height_pixel"]
        self.cell_size = 20


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
        
        init_pos = self.find_start_position()

        self.mouse = MicroMouse(self.params, self.config, init_pos, "down")


        # Set Window Config
        self.set_frame_config()
        self.initialize_pygame()


    def pygame_loop(self):

        clock = pygame.time.Clock()

        self.output_console2 = True
        self.output_console3 = True
        
        # Maze is static, draw it once before the loop
        #self.draw_maze()

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # check state
            if self.maze[self.mouse.position[1]][self.mouse.position[0]] == "2" and self.output_console2:
                self.master.output_console(self.maze[self.mouse.position[1]][self.mouse.position[0]])
                self.output_console2 = False
            if self.maze[self.mouse.position[1]][self.mouse.position[0]] == "3" and self.output_console3:
                self.master.output_console(self.maze[self.mouse.position[1]][self.mouse.position[0]])
                self.output_console3 = False
                #self.running = False
                self.explore_flag = False

            self.screen.fill((240, 240, 240))

            # maze regeneration each frame
            self.draw_maze()

            # calc next mouse position
            if self.explore_flag:
                self.explore()

            # draw micro mouse
            self.screen.blit(self.mouse.images[self.mouse.direction], (self.mouse.position[0]*self.cell_size, self.mouse.position[1]*self.cell_size))

            # update
            pygame.display.update()

            self.mouse.console_flag = False

            clock.tick(20)


    def explore(self):

        if self.params["method"] == "左手法":
            self.left_hand_method()

        self.mouse.mouse_eye()


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

        self.running = False

        if hasattr(self, 'thread') and self.thread.is_alive():
            return

        pygame.init()
        self.adjust_cell_size()

        self.output_console2 = True
        self.output_console3 = True
        self.running = True
        self.explore_flag = True

        self.mouse.position = self.find_start_position()

        self.screen = pygame.display.set_mode((400, 400))
        self.thread = threading.Thread(target=self.pygame_loop, daemon=True)
        self.thread.start()


    def adjust_cell_size(self):
        maze_width = len(self.maze[0])
        maze_height = len(self.maze)
        self.cell_size = min(self.max_width_pixel // maze_width, self.max_height_pixel // maze_height)


    def find_start_position(self):
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == "2":
                    return [x, y]
        return None

    """ Maze """

    def maze_regeneration(self):

        w = int(self.master.main_window.entries["maze_width_config"].get())
        h = int(self.master.main_window.entries["maze_height_config"].get())

        print(w, h)

        w = (w // 2) * 2 + 1
        h = (h // 2) * 2 + 1

        self.maze = self.make_maze(w, h)

        self.adjust_cell_size()


    def draw_maze(self):

        # Create default maze pattern (10x5)

        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):

                if cell == '1':  # Wall
                    pygame.draw.rect(self.screen, (0, 0, 0), [x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size])
                elif cell == "2":# Start
                    pygame.draw.rect(self.screen, (0, 80, 0), [x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size])
                elif cell == "3":# End
                    pygame.draw.rect(self.screen, (120, 0, 0), [x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size])



    def make_maze(self, width, height):

        maze = [['1'] * width for _ in range(height)]

        def carve(x, y, paths):
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + 2 * dx, y + 2 * dy
                if 0 <= nx < width and 0 <= ny < height:
                    if maze[ny][nx] == '1':
                        maze[ny][nx] = '0'
                        maze[y + dy][x + dx] = '0'
                        paths.add((nx, ny))
                        carve(nx, ny, paths)

        # 初期位置を選び、掘り進める
        paths = set()
        start_x, start_y = 1, 1
        maze[start_y][start_x] = '0'
        paths.add((start_x, start_y))
        carve(start_x, start_y, paths)

        # スタートとゴールのランダムな設定
        def set_random_start_goal():
            paths_list = list(paths)
            start, goal = random.sample(paths_list, 2)
            maze[start[1]][start[0]] = '2'
            maze[goal[1]][goal[0]] = '3'

        set_random_start_goal()

        maze = [''.join(row) for row in maze]


        return maze


    """ Algorithms """

    def left_hand_method(self):

        # Patterns
        directions = ["left", "up", "right", "down"]
        direction_vectors = {"left": (-1, 0), "up": (0, -1), "right":(1, 0), "down":(0, 1),}

        # Get current direction
        cur_dir = directions.index(self.mouse.direction)

        # left hand method
        for i in range(4):

            # left -> up -> right -> back
            dir_idx = (cur_dir + i + 3) % 4
            direction = directions[dir_idx]
            dx, dy = direction_vectors[direction]
            nx, ny = self.mouse.position[0] + dx, self.mouse.position[1] + dy

            # if not wall, go the direction
            if self.maze[ny][nx] != "1":
                self.mouse.position = [nx, ny]
                self.mouse.direction = direction
                break


class MicroMouse:

    def __init__(self, params, config, init_position, init_direction):

        # Global Settings
        self.params = params
        self.config = config

        # Attributes
        self.position = init_position
        self.direction = init_direction
        self.images = self.load_image()

        # Judge Flags
        self.console_flag = True


    def move_mouse(self, maze, btn_dir=None, alg_dir=None):

        # If Click Button, determine move direction
        if btn_dir:
            self.direction = btn_dir
        elif alg_dir:
            self.direction = alg_dir

        deltas = {'left': (-1, 0), 'up': (0, -1), 'right': (1, 0), 'down': (0, 1), }
        delta = deltas.get(self.direction, (0, 0))
        new_x = self.position[0] + delta[0]
        new_y = self.position[1] + delta[1]

        # on Maze Judge
        if new_x in range(0, len(maze[0])) and new_y in range(0, len(maze)):

            # Wall Judge
            if maze[new_y][new_x] != "1":

                self.position = [new_x, new_y]
                self.direction = self.direction

        self.console_flag = True


    def mouse_eye(self):

        # Pattern and Relative direction index
        directions = ["left", "up", "right", "down"]
        cur_dir_idx = directions.index(self.direction)

        left_dir = (cur_dir_idx + 3) % 4
        left = directions[left_dir]

        up_dir = (cur_dir_idx) % 4
        up = directions[up_dir]

        right_dir = (cur_dir_idx + 1) % 4
        right = directions[right_dir]

        down_dir = (cur_dir_idx + 2) % 4
        down = directions[down_dir]

        print("cur_dir:", up, "left_dir: ", left)


    def load_image(self):

        image_path = os.path.join(self.params["root_dir"], "src","images")

        front_path = os.path.join(image_path, "front.png")
        back_path = os.path.join(image_path, "back.png")
        left_path = os.path.join(image_path, "left.png")
        right_path = os.path.join(image_path, "right.png")

        images = {
            "down": pygame.image.load(front_path),
            "up": pygame.image.load(back_path),
            "left": pygame.image.load(left_path),
            "right": pygame.image.load(right_path),
        }

        for key in images:
            images[key] = pygame.transform.scale(images[key], (20, 20))

        return images