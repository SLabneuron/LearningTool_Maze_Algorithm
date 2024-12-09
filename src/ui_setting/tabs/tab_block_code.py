# -*- coding: utf-8 -*-

"""

Created on Thu Mar 14, 2024

@author: shriafujilab

Purpose:

    Block Code Editor

"""


# import standard library
import tkinter as tk
from tkinter import ttk

# import my library

from src.block_code.inst_block import CodeBlock
from src.block_code.compiler import compile_block_code


class TabBlockCode:

    def __init__(self, master, tab):

        self.master = master

        # Attributes
        self.blocks = []                # code blocks
        self.selected_block = None
        self.last_block = None

        self.set_frames(tab)


    def set_frames(self, tab):

        # title
        text = ttk.Label(tab, text = "選択画面（条件・処理）")
        text.grid(row=0, column=0, sticky=tk.W)
        
        # row
        row = ttk.Frame(tab, width=400)
        row.grid(row=1, column=0, sticky=tk.W)

        # Combobox (conditions or procedures)
        combo01 = ttk.Combobox(row, width=10)
        combo01["value"] = ("条件分岐", "条件式", "評価", "処理")
        combo01.current(0)       # Init
        combo01.grid(row=0, column=0, sticky = tk.W)

        # Combobox determine by above selects
        combo02 = ttk.Combobox(row, width=10)
        combo02.grid(row=0, column=1, sticky = tk.W)

        options = {
            "条件分岐"  :("if", "else if", "else"),
            "条件式"    :("左に壁がある", "右に壁がある", "前に壁がある", "後ろに壁がある"),
            "条件式"    :("左に壁がある", "右に壁がある", "前に壁がある", "後ろに壁がある",
                       "左に壁がない", "右に壁がない", "前に壁がない", "後ろに壁がない"),
            "評価"      :("== True", "== False"),
            "処理"      :("左に進む", "右に進む", "前に進む", "後ろに進む", "----"),
        }

        def update_combo02(event=None):
            chosen_option = combo01.get()
            combo02["value"] = options[chosen_option]
            combo02.current(0)

        combo01.bind("<<ComboboxSelected>>", update_combo02)
        update_combo02()        # Init

        # Add blocks
        def add_block():

            new_block = CodeBlock(canvas, combo02.get(), 10, 25)
            self.blocks.append(new_block)

        button1 = ttk.Button(row, text="ブロック追加", width=12, command=add_block)
        button1.grid(row=0, column=2, sticky = tk.W)

        # execute code
        def execute_code():

            self.master.python_code = compile_block_code(self.blocks, canvas)

            self.master.method = "code_block"

            # run block code
            self.master.run()

        button2 = ttk.Button(row, text="実行", width = 6,command=execute_code)
        button2.grid(row=0, column=3, sticky = tk.W)


        # Canvas: block code editor
        canvas = tk.Canvas(tab, width=400, height=300, bg="white")
        canvas.grid(row=2, column=0, sticky = "nsew")
        self.canvas_settings(canvas)

        # clear all
        button3 = ttk.Button(tab, text = "clear all", width=12, command = self.clear_all)
        button3.grid(row=3, column=0, sticky=tk.W)


    def clear_all(self):

        while self.blocks != []:

            for block in self.blocks:
                block.remove()
                self.blocks.remove(block)


    def canvas_settings(self, canvas):

        # Canvas Guidelines
        def canvas_draw_guidelines():

            # config height of row
            line_spacing = 25

            for i in range(10,  400, line_spacing):
                canvas.create_line(0, i, 300, i, fill="#a0a0a0", dash=(2, 5))

        canvas_draw_guidelines()

        # Event: click event
        def on_click(event):

            for block in self.blocks:
                coords = canvas.coords(block.id)

                if coords[0] <= event.x <= coords[2] and coords[1] <= event.y <= coords[3]:
                    # if click on box, do procedure
                    self.selected_block = block
                    self.last_block = block
                    self.selected_block.x, self.selected_block.y = event.x, event.y
                    return

        canvas.bind("<Button-1>", on_click)

        # Event: drag evemt
        def on_drag(event):

            def snap_to_row(mouse_y):

                row_height = 25

                nearest_row_y = round((mouse_y - 10)/row_height)*row_height + 10
                return max(nearest_row_y, 10)

            def snap_to_column(mouse_x):

                indent = 20

                nearest_row_x = round((mouse_x - 10)/indent) * indent + 10
                return max(nearest_row_x, 10)


            if self.selected_block:

                # Firstly set colummn
                dx, dy = event.x -self.selected_block.x, event.y - self.selected_block.y
                self.selected_block.move(dx, dy)
                self.selected_block.x = event.x
                self.selected_block.y = event.y

                # Next set row
                snapped_x = snap_to_column(event.x)
                snapped_y = snap_to_row(event.y)
                self.selected_block.move_to_x(snapped_x)
                self.selected_block.move_to_y(snapped_y)

        canvas.bind("<B1-Motion>", on_drag)   # drag

        # release event
        def on_release(event=None):
            if self.selected_block:
                self.selected_block = None

        canvas.bind("<ButtonRelease-1>", on_release)  # release

        # right double click event
        def on_right_double_click(event):

            for block in self.blocks:
                coords = canvas.coords(block.id)
                if coords[0] <= event.x <= coords[2] and coords[1] <= event.y <= coords[3]:
                    block.remove()
                    self.blocks.remove(block)
                    return

        canvas.bind("<Double-Button-3>", on_right_double_click)   # right double click
