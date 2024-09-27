#  -*- coding: utf-8 -*-
"""
Created on Tue Sep 17, 2024

@author: shirafujilab

Puropose:

    CodeSnippet for block programming

"""


import tkinter as tk



class BlockSnippet:

    def __init__(self, canvas, text, x, y):

        # get canvas and text
        self.canvas = canvas
        self.text = text
        
        text_width = {

            "if"           : 40,
            "else if"      : 40,
            "else"         : 40,
            "左に壁がある"  : 80,
            "右に壁がある"  : 80,
            "前に壁がある"  : 80,
            "後ろに壁がある": 80,
            "== True"       : 60,
            "== False"      : 60,
            "左に進む"      : 60,
            "右に進む"      : 60,
            "前に進む"      : 60,
            "後ろに進む"    : 60,
            "----"          : 40,
        }
        
        self.id = canvas.create_rectangle(x, y, x + text_width[text], y + 25, fill="white", outline="black")
        self.text_id = canvas.create_text(x + text_width[text]/2, y + 12.5, text=text)
        self.x, self.y = x, y

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


class BlockCompiler:

    def __init__(self):

        self.lut = {

            "if"            : "if ",
            "else if"       : "elif ",
            "else"          : "else:",
            "左に壁がある": "(self.maze[lny][lnx] == '1')",
            "右に壁がある": "(self.maze[rny][rnx] == '1')",
            "前に壁がある": "(self.maze[fny][fnx] == '1')",
            "後ろに壁がある": "(self.maze[bny][bnx] == '1')",
            "== True": "== True:",
            "== False": "== False:",
            "左に進む": "self.mouse.move(self.maze, lnx, lny, l_direction)",
            "右に進む": "self.mouse.move(self.maze, rnx, rny, r_direction)",
            "前に進む": "self.mouse.move(self.maze, fnx, fny, f_direction)",
            "後ろに進む": "self.mouse.move(self.maze, bnx, bny, b_direction)",
            "----": "    ",

        }




    def generate_python_code(self, blocks, canvas):
        

        python_code = ""
        indent_spaces = "    "  # 4つのスペースでインデント
        block_groups = {}

        # ブロックを行（y座標）ごとにまとめる
        for block in blocks:
            block_y_coord = canvas.coords(block.id)[1]
            if block_y_coord not in block_groups:
                block_groups[block_y_coord] = []
            block_groups[block_y_coord].append(block)

        # 行ごとにソートし、x座標でインデントレベルを計算
        sorted_rows = sorted(block_groups.items())

        for row_y, blocks_in_row in sorted_rows:
            blocks_in_row = sorted(blocks_in_row, key=lambda b: canvas.coords(b.id)[0])

            # 各行の最初のブロックをインデント付きで出力
            for idx, block in enumerate(blocks_in_row):
                block_text = block.text
                if block_text in self.lut:
                    code_line = self.lut[block_text]

                    # if文やelif文など条件文の場合は改行して書く
                    if code_line.strip().endswith(":"):
                        python_code += f"{code_line}"  # それ以外はインデントせず
                    else:
                        python_code += f"{code_line} "  # 条件や処理のパーツを空白でつなげる

            # 行が終わったら改行を追加
            python_code += "\n"

        return python_code




