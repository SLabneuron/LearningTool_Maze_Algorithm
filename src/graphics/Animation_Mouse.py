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
        Maze and Algorithm


        """

        # Get components
        self.master = master
        self.params = params
        self.config = config
        self.main_frame = main_frame

        self.running = True
        self.explore_flag = True

        # Config of Graphic Spaace
        self.max_width_pixel = self.config["maze_width_pixel"]
        self.max_height_pixel = self.config["maze_height_pixel"]
        self.cell_size = 20

        # init maze
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


    def initialize_pygame(self):

        # finish thread
        self.running = False

        if hasattr(self, 'thread') and self.thread.is_alive():
            return

        pygame.init()
        self.adjust_cell_size()

        # Flag activate
        self.output_console2 = True
        self.output_console3 = True
        self.running = True             # restart thread
        self.explore_flag = True

        # Get a current position
        self.mouse.position = self.find_start_position()

        self.screen = pygame.display.set_mode((400, 400))
        self.thread = threading.Thread(target=self.pygame_loop, daemon=True)
        self.thread.start()


    def find_start_position(self):
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == "2":
                    return [x, y]
        return None


    """ Main Loop """

    def pygame_loop(self):

        clock = pygame.time.Clock()

        self.output_console2 = True
        self.output_console3 = True

        # Main Loop
        while self.running:

            # Event Handller
            for event in pygame.event.get():

                # Finish pygame (no binding a specific key)
                if event.type == pygame.QUIT:
                    self.running = False

                # Remove walls (right click)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    mouse_x, mouse_y = event.pos
                    self.rotate_state_of_wall(mouse_x,  mouse_y)

            # Check State
            current_state = self.maze[self.mouse.position[1]][self.mouse.position[0]]
            
            if current_state == "2" and self.output_console2:
                self.master.output_console(self.maze[self.mouse.position[1]][self.mouse.position[0]])
                self.output_console2 = False
            if self.maze[self.mouse.position[1]][self.mouse.position[0]] == "3" and self.output_console3:
                self.master.output_console(self.maze[self.mouse.position[1]][self.mouse.position[0]])
                self.output_console3 = False
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
        elif self.params["method"] == "code_block":
            self.block_programming()

        self.mouse.mouse_eye()


    """ Event Handlers """

    def rotate_state_of_wall(self, x, y):
        """
        Description:
            Event handler that changes the state of a wall in the maze.
            The state changes in the following order:

                Before  | After

                0 (path)  -> 1 (wall)
                1 (wall)  -> 2 (start)
                2 (start) -> 3 (end)
                3 (end)   -> 4 (start)

        Appendix:

            1. Integer Division (//):
                This operator performs intefer (floor) division.

                Example)
                     3.5    ->  3
                    -2.5    -> -3.0

            2. Why update the entire row?
                In Python, strings are immutablem which means their contents cant't be changed directly.
                To update a single character, the entire string (in this case, a row) needs to be modified.

        """

        # get the current position in the maze
        cell_x = x // self.cell_size
        cell_y = y // self.cell_size

        # rotate the state of the wall at the current position
        if self.maze[cell_y][cell_x] == "0":
            # 0 (path) -> 1 (wall)
            self.maze[cell_y] = self.maze[cell_y][:cell_x] + "1" + self.maze[cell_y][cell_x+1:]
        elif self.maze[cell_y][cell_x] == "1":
            # 1 (wall) -> 2 (start)
            self.maze[cell_y] = self.maze[cell_y][:cell_x] + "2" + self.maze[cell_y][cell_x+1:]
        elif self.maze[cell_y][cell_x] == "2":
            # 2 (start)-> 3 (end)
            self.maze[cell_y] = self.maze[cell_y][:cell_x] + "3" + self.maze[cell_y][cell_x+1:]
        elif self.maze[cell_y][cell_x] == "3":
            # 3 (end)  -> 0 (path)
            self.maze[cell_y] = self.maze[cell_y][:cell_x] + "0" + self.maze[cell_y][cell_x+1:]


    

    """ Maze """

    def maze_regeneration(self):

        w = int(self.master.main_window.entries["maze_width_config"].get())
        h = int(self.master.main_window.entries["maze_height_config"].get())

        print(w, h)

        w = (w // 2) * 2 + 1
        h = (h // 2) * 2 + 1

        self.maze = self.make_maze(w, h)

        self.adjust_cell_size()


    def adjust_cell_size(self):
        maze_width = len(self.maze[0])
        maze_height = len(self.maze)
        self.cell_size = min(self.max_width_pixel // maze_width, self.max_height_pixel // maze_height)


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


    def block_programming(self):
        
        """  """
        
        # Patterns
        directions = ["left", "up", "right", "down"]
        direction_vectors = {"left": (-1, 0), "up": (0, -1), "right":(1, 0), "down":(0, 1),}

        # Get current direction
        cur_dir = directions.index(self.mouse.direction)

        """ Prepare block programming """

        # left
        l_dir_idx = (cur_dir + 3) % 4
        l_direction = directions[l_dir_idx]
        ldx, ldy = direction_vectors[l_direction]
        lnx, lny = self.mouse.position[0] + ldx, self.mouse.position[1] + ldy

        # right
        r_dir_idx = (cur_dir + 1) % 4
        r_direction = directions[r_dir_idx]
        rdx, rdy = direction_vectors[r_direction]
        rnx, rny = self.mouse.position[0] + rdx, self.mouse.position[1] + rdy

        # front
        f_dir_idx = (cur_dir + 0) % 4
        f_direction = directions[f_dir_idx]
        fdx, fdy = direction_vectors[f_direction]
        fnx, fny = self.mouse.position[0] + fdx, self.mouse.position[1] + fdy

        # back
        b_dir_idx = (cur_dir + 2) % 4
        b_direction = directions[b_dir_idx]
        bdx, bdy = direction_vectors[b_direction]
        bnx, bny = self.mouse.position[0] + bdx, self.mouse.position[1] + bdy

        try:
            #print(self.master.code)
            exec(self.master.code)
        except Exception as e:
            print("error is: ", e)
            print(self.master.code)

    # Utils
    def set_frame_config(self):
        """
        Description:
            Set up SDL environmental variables to ensure that pygame renders inside a tkinter frame.
            This involves determining the OS-specific SDL video and setting the window ID to the tkinter frame.

        Appendix:
            Pygame is usually reffers to the environmental variable "SDL_VIDEODRIVER"
            to determine how to handle window rendering. In this case, by passing the tkinter frame's
            window ID to "SDL_WINDOWID", pygame is embedded directly within the tkinter frame.

        """

        # Determine OS and set appropriate SDL video driver
        if sys.platform == "win32":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        elif sys.platform == "linux" or sys.platform == "linux2":
            os.environ['SDL_VIDEODRIVER'] = 'x11'
        elif sys.platform == "darwin":
            os.environ['SDL_VIDEODRIVER'] = 'cocoa'

        # Pass the tkinter frame's window ID to SDL
        os.environ["SDL_WINDOWID"] = str(self.main_frame.winfo_id())



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

        # move
        self.move(maze, new_x, new_y, self.direction)

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


    # Operation

    def move(self, maze, nx, ny, direction):
        """
        Description:
            move mouse by next position (nx, ny) if not next position is wall
            update position

        Attribute:
            maze: maze
            nx: coordinate x of next position
            ny: coordinate y of next position
            direction: next direction
        """

        # if not next position is wall, position and direction are updated
        if nx in range(0, len(maze[0])) and ny in range(0, len(maze)) and maze[ny][nx] != '1':
            self.position = [nx, ny]
            self.direction = direction


    # Utils

    def load_image(self):
        """
        Description: get figures from "src.images"
        Use: Init
        """

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