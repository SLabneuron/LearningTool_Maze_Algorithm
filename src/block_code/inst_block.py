#  -*- coding: utf-8 -*-
"""
Created on Tue Sep 17, 2024

@author: shirafujilab

Puropose:

    Instance code block

"""


class CodeBlock:

    # control class variables
    instances = []

    def __init__(self, canvas, text, x, y):

        # get canvas and text
        self.canvas = canvas
        self.text = text

        # config
        text_width = self.text_config()

        # attributes
        self.id = canvas.create_rectangle(x, y, x + text_width[text], y + 25, fill="white", outline="black")
        self.text_id = canvas.create_text(x + text_width[text]/2, y + 12.5, text=text)
        self.x, self.y = x, y

        CodeBlock.instances.append(self)


    def move(self, dx, dy):
        self.canvas.move(self.id, dx, dy)
        self.canvas.move(self.text_id, dx, dy)


    def move_to_y(self, new_y):

        current_coords = self.canvas.coords(self.id)
        dy = new_y - current_coords[1]
        self.canvas.move(self.id, 0, dy)
        self.canvas.move(self.text_id, 0, dy)
        self.y = new_y


    def move_to_x(self, new_x):

        current_coords = self.canvas.coords(self.id)
        dx = new_x - current_coords[0]
        self.canvas.move(self.id, dx, 0)
        self.canvas.move(self.text_id, dx, 0)
        self.x = new_x


    def remove(self):

        self.canvas.delete(self.id)
        self.canvas.delete(self.text_id)


    @classmethod
    def delete_all(cls):

        for instance in  cls.instances[:]:
            instance.remove()


    def text_config(self):

        # config
        text_width = {

            "if"           : 40,
            "else if"      : 40,
            "else"         : 40,
            "左に壁がある"  : 80,
            "右に壁がある"  : 80,
            "前に壁がある"  : 80,
            "後ろに壁がある": 80,
            "左に壁がない"  : 80,
            "右に壁がない"  : 80,
            "前に壁がない"  : 80,
            "後ろに壁がない": 80,
            "== True"       : 60,
            "== False"      : 60,
            "左に進む"      : 60,
            "右に進む"      : 60,
            "前に進む"      : 60,
            "後ろに進む"    : 60,
            "----"          : 40,
        }

        return text_width

