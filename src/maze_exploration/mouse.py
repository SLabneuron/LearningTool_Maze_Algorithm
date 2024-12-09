# -*- coding: utf-8 -*-

"""

Created on: 2024-12-08


@author: shriafujilab

Purpose:

    Mouse Setting

"""

import os
import pygame


class MicroMouse:

    def __init__(self, master, params, entries, init_position, init_direction):

        # Global Settings
        self.master = master
        self.params = params
        self.entries = entries

        # Attributes
        self.position = init_position
        self.direction = init_direction

        self.images = self.load_image()


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
            images[key] = pygame.transform.scale(images[key], (self.master.maze.cell_size, self.master.maze.cell_size))

        return images