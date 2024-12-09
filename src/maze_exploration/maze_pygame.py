# -*- coding: utf-8 -*-
"""
Created on Mon July 9, 2024

@author: shirafujilab
"""

# import standard library
import sys
import os
import pygame
import threading

# import my library
from src.maze_exploration.maze import Maze
from src.maze_exploration.mouse import MicroMouse


class MazeRunning:

    def __init__(self, master, params, entries, frame):

        # Get components
        self.master = master
        self.params = params
        self.entries = entries
        self.frame = frame

        self.set_frame_config()

        self.initialize_pygame


    def initialize_pygame(self):

        self.running = False

        if hasattr(self, 'thread') and self.thread.is_alive():
            return

        # maze and mouse initialize
        self.master.maze = Maze(self.master, self.params, self.entries, self.master.maze.maze, self.master.maze.cell_size)
        self.master.mouse = MicroMouse(self.master, self.params, self.entries, self.master.maze.init_pos, "down")

        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))
        self.running = True

        self.thread = threading.Thread(target=self.pygame_loop, daemon=True)
        self.thread.start()


    def pygame_loop(self):

        clock = pygame.time.Clock()

        self.console = True

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

            if self.console: self.before_goal()

            self.screen.fill((240, 240, 240))

            # maze regeneration each frame
            self.draw_maze()

            # draw micro mouse
            self.screen.blit(self.master.mouse.images[self.master.mouse.direction], (self.master.mouse.position[0]*self.master.maze.cell_size, self.master.mouse.position[1]*self.master.maze.cell_size))

            # update
            pygame.display.update()
            clock.tick(20)


    def before_goal(self):

        # Check State
        current_state = self.master.maze.maze[self.master.mouse.position[1]][self.master.mouse.position[0]]

        if current_state == "2":
            print("*** Go for the goal!! ***")
        if current_state == "3":
            print("*** Congratulations!! ***")
            self.console = False

        # calc next mouse position
        if self.console: self.explore()


    def draw_maze(self):

        # Create default maze pattern (10x5)

        for y, row in enumerate(self.master.maze.maze):
            for x, cell in enumerate(row):

                if cell == '1':  # Wall
                    pygame.draw.rect(self.screen, (0, 0, 0), [x*self.master.maze.cell_size, y*self.master.maze.cell_size, self.master.maze.cell_size, self.master.maze.cell_size])
                elif cell == "2":# Start
                    pygame.draw.rect(self.screen, (0, 80, 0), [x*self.master.maze.cell_size, y*self.master.maze.cell_size, self.master.maze.cell_size, self.master.maze.cell_size])
                elif cell == "3":# End
                    pygame.draw.rect(self.screen, (120, 0, 0), [x*self.master.maze.cell_size, y*self.master.maze.cell_size, self.master.maze.cell_size, self.master.maze.cell_size])


    def explore(self):

        if self.master.method == "左手法":
            self.left_hand_method()
        elif self.master.method == "code_block":
            self.block_programming()

        self.master.mouse.mouse_eye()


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
        cell_x = x // self.master.maze.cell_size
        cell_y = y // self.master.maze.cell_size

        # rotate the state of the wall at the current position
        if self.master.maze.maze[cell_y][cell_x] == "0":
            # 0 (path) -> 1 (wall)
            self.master.maze.maze[cell_y] = self.master.maze.maze[cell_y][:cell_x] + "1" + self.master.maze.maze[cell_y][cell_x+1:]
        elif self.master.maze.maze[cell_y][cell_x] == "1":
            # 1 (wall) -> 2 (start)
            self.master.maze.maze[cell_y] = self.master.maze.maze[cell_y][:cell_x] + "2" + self.master.maze.maze[cell_y][cell_x+1:]
        elif self.master.maze.maze[cell_y][cell_x] == "2":
            # 2 (start)-> 3 (end)
            self.master.maze.maze[cell_y] = self.master.maze.maze[cell_y][:cell_x] + "3" + self.master.maze.maze[cell_y][cell_x+1:]
        elif self.master.maze.maze[cell_y][cell_x] == "3":
            # 3 (end)  -> 0 (path)
            self.master.maze.maze[cell_y] = self.master.maze.maze[cell_y][:cell_x] + "0" + self.master.maze.maze[cell_y][cell_x+1:]





    """ Algorithms """

    def left_hand_method(self):

        # Patterns
        directions = ["left", "up", "right", "down"]
        direction_vectors = {"left": (-1, 0), "up": (0, -1), "right":(1, 0), "down":(0, 1),}

        # Get current direction
        cur_dir = directions.index(self.master.mouse.direction)

        # left hand method
        for i in range(4):

            # left -> up -> right -> back
            dir_idx = (cur_dir + i + 3) % 4
            direction = directions[dir_idx]
            dx, dy = direction_vectors[direction]
            nx, ny = self.master.mouse.position[0] + dx, self.master.mouse.position[1] + dy

            # if not wall, go the direction
            if self.master.maze.maze[ny][nx] != "1":
                self.master.mouse.position = [nx, ny]
                self.master.mouse.direction = direction
                break


    def block_programming(self):

        """  """

        # Patterns
        directions = ["left", "up", "right", "down"]
        direction_vectors = {"left": (-1, 0), "up": (0, -1), "right":(1, 0), "down":(0, 1),}

        # Get current direction
        cur_dir = directions.index(self.master.mouse.direction)

        """ Prepare block programming """

        # left
        l_dir_idx = (cur_dir + 3) % 4
        l_direction = directions[l_dir_idx]
        ldx, ldy = direction_vectors[l_direction]
        lnx, lny = self.master.mouse.position[0] + ldx, self.master.mouse.position[1] + ldy

        # right
        r_dir_idx = (cur_dir + 1) % 4
        r_direction = directions[r_dir_idx]
        rdx, rdy = direction_vectors[r_direction]
        rnx, rny = self.master.mouse.position[0] + rdx, self.master.mouse.position[1] + rdy

        # front
        f_dir_idx = (cur_dir + 0) % 4
        f_direction = directions[f_dir_idx]
        fdx, fdy = direction_vectors[f_direction]
        fnx, fny = self.master.mouse.position[0] + fdx, self.master.mouse.position[1] + fdy

        # back
        b_dir_idx = (cur_dir + 2) % 4
        b_direction = directions[b_dir_idx]
        bdx, bdy = direction_vectors[b_direction]
        bnx, bny = self.master.mouse.position[0] + bdx, self.master.mouse.position[1] + bdy

        try:
            #print(self.master.code)
            exec(self.master.python_code)
        except Exception as e:
            print("error is: ", e)
            print(self.master.python_code)


    def set_frame_config(self):

        """

        Note!!: Not working in Mac Env.

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
        os.environ["SDL_WINDOWID"] = str(self.frame.winfo_id())