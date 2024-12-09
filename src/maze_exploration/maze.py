# -*- coding: utf-8 -*-

"""
Created on: 2024-07-09

@author: shirafujilab

Content:

        Maze


Attribute

        self.maze
        self.init_pos
        self.cell_size

"""

# import my library
import random



class Maze:

    maze = [
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

    def __init__(self, master, params, entries, maze=None, size=None):

            # Get params
            self.master = master
            self.params = params
            self.entries = entries


            """ set maze """

            # get default
            self.maze = Maze.maze if maze == None else maze

            # find 'start' and 'goal'
            self.init_pos = self.find_start_position(self.maze)

            # adjust cell size
            self.cell_size = 20 if size == None else size


    def regenerate_maze(self):

        w = int(self.master.entries["maze_width_config"].get())
        h = int(self.master.entries["maze_height_config"].get())

        # resize for path (for avoiding even num)
        w = (w//2) * 2 + 1
        h = (h//2) * 2 + 1

        self.master.maze.maze = self.make_maze(w, h)

        # get initial position
        self.init_pos = self.find_start_position(self.master.maze.maze)

        self.adjust_cell_size()
        
        self.master.mouse.images = self.master.mouse.load_image()


    def find_start_position(self, maze):

        for y, row in enumerate(maze):
            for x, cell in enumerate(row):

                 if cell == "2": return [x, y]

        # Exception handling
        return None


    def adjust_cell_size(self):
        


        maze_width = len(self.master.maze.maze[0])
        maze_height = len(self.master.maze.maze)
        self.cell_size = min(int(self.params["maze_width_pixel"] / maze_width), int(self.params["maze_height_pixel"] /maze_height))
        
        print(maze_width, maze_height, self.cell_size)


    def make_maze(self, w, h):

        """ make maze array """

        # Fill in '1'
        maze = [['1'] * w for _ in range(h)]

        # set path '0'
        def carve(x, y, paths):
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + 2 * dx, y + 2 * dy
                if 0 <= nx < w and 0 <= ny < h:
                    if maze[ny][nx] == '1':
                        maze[ny][nx] = '0'
                        maze[y + dy][x + dx] = '0'
                        paths.add((nx, ny))
                        carve(nx, ny, paths)

        paths = set()
        start_x, start_y = 1, 1
        maze[start_y][start_x] = '0'
        paths.add((start_x, start_y))
        carve(start_x, start_y, paths)

        # set 'start' and 'goal'
        def set_random_start_goal():
            paths_list = list(paths)
            start, goal = random.sample(paths_list, 2)
            maze[start[1]][start[0]] = '2'
            maze[goal[1]][goal[0]] = '3'

        set_random_start_goal()

        maze = [''.join(row) for row in maze]

        return maze


    def default_maze(self):

        # default setting (for practice)
        self.master.maze.maze = Maze.maze

        # get initial position
        self.init_pos = self.find_start_position(self.master.maze.maze)

        self.cell_size = 20

        self.master.mouse.images = self.master.mouse.load_image()

