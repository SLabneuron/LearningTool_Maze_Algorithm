# -*- coding: utf-8 -*-

"""

Created on Thu Mar 14, 2024

@author: shriafujilab

Purpose:

    Block Code Compiler

"""


def compile_block_code(blocks, canvas):

    # set
    lut = set_lut()

    python_code = ""        # python code after compiled
    indent_spaces = "    "  # indent
    block_groups = {}

    # summarize blocks line by line
    for block in blocks:
        block_y_coord = canvas.coords(block.id)[1]
        if block_y_coord not in block_groups:
            block_groups[block_y_coord] = []
        block_groups[block_y_coord].append(block)

    # 行ごとにソートし、x座標でインデントレベルを計算 sort block_groups
    sorted_rows = sorted(block_groups.items())

    for row_y, blocks_in_row in sorted_rows:

        blocks_in_row = sorted(blocks_in_row, key=lambda b: canvas.coords(b.id)[0])

        # 各行の最初のブロックをインデント付きで出力
        for idx, block in enumerate(blocks_in_row):
            block_text = block.text
            if block_text in lut:
                code_line = lut[block_text]

                # add indent "if" and "else"
                if code_line.strip().endswith(":"):
                    python_code += f"{code_line}"  # それ以外はインデントせず
                else:
                    python_code += f"{code_line} "  # 条件や処理のパーツを空白でつなげる

        # new line
        python_code += "\n"

    return python_code


def set_lut():

    lut = {

        "if"            : "if ",
        "else if"       : "elif ",
        "else"          : "else:",
        "左に壁がある": "(self.master.maze.maze[lny][lnx] == '1')",
        "右に壁がある": "(self.master.maze.maze[rny][rnx] == '1')",
        "前に壁がある": "(self.master.maze.maze[fny][fnx] == '1')",
        "後ろに壁がある": "(self.master.maze.maze[bny][bnx] == '1')",
        "左に壁がない": "(self.master.maze.maze[lny][lnx] != '1')",
        "右に壁がない": "(self.master.maze.maze[rny][rnx] != '1')",
        "前に壁がない": "(self.master.maze.maze[fny][fnx] != '1')",
        "後ろに壁がない": "(self.master.maze.maze[bny][bnx] != '1')",
        "== True": "== True:",
        "== False": "== False:",
        "左に進む": "self.master.mouse.move(self.master.maze.maze, lnx, lny, l_direction)",
        "右に進む": "self.master.mouse.move(self.master.maze.maze, rnx, rny, r_direction)",
        "前に進む": "self.master.mouse.move(self.master.maze.maze, fnx, fny, f_direction)",
        "後ろに進む": "self.master.mouse.move(self.master.maze.maze, bnx, bny, b_direction)",
        "----": "    ",

    }

    return lut
