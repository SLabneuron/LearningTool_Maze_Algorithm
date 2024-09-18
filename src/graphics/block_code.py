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

        # make canvas
        self.canvas = canvas
        self.text = text
        self.id = canvas.create_rectangle(x, y, x + 120, y + 25, fill="white", outline="black")
        self.text_id = canvas.create_text(x + 60, y + 12.5, text=text)
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




class Application(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.blocks = []
        
    
    def create_widgets(self):
        self.canvas = tk.Canvas(self, width = 400, height = 300)
        canvas.pack(side="top", fill="both", expand= True)
        self.add_button = tk.Button(self, text="add a block", command=self.add_block)



def add_block():
    new_block = BlockSnippet(canvas, "条件: 左に壁がない", 10, 10 + len(blocks) * 40)
    blocks.append(new_block)



def on_click(event):
    global selected_block, last_block, selected_arrow
    for block in blocks:
        coords = canvas.coords(block.id)
        if coords[0] <= event.x <= coords[2] and coords[1] <= event.y <= coords[3]:

            selected_block = block
            last_block = block  # 現在のブロックをlast_blockとして設定
            selected_block.start_x, selected_block.start_y = event.x, event.y
            return


def on_drag(event):
    if selected_block:
        dx, dy = event.x - selected_block.start_x, event.y - selected_block.start_y
        selected_block.move(dx, dy)
        selected_block.start_x, selected_block.start_y = event.x, event.y


def on_release(event):
    global selected_block, selected_arrow
    if selected_block:
        selected_block = None
    if selected_arrow:
        selected_arrow = None


def delete_selected_arrow():
    global selected_arrow
    if selected_arrow:
        canvas.delete(selected_arrow.arrow_id)
        arrows.remove(selected_arrow)
        selected_arrow = None


if __name__ == "__main__":
    root = tk.Tk()
    root.title("ブロックベースのプログラミングデモ")

    canvas = tk.Canvas(root, width=400, height=300)
    canvas.pack()

    blocks = []  # 追加されたブロックを追跡
    arrows = []
    selected_block = None  # 現在選択されているブロック
    last_block = None
    selected_arrow = None

    add_button = tk.Button(root, text="ブロック追加", command=add_block)
    add_button.pack()
    
    delete_button = tk.Button(root, text="矢印削除", command=delete_selected_arrow)
    delete_button.pack()

    canvas.bind("<Button-1>", on_click)  # クリックイベントのバインド
    canvas.bind("<B1-Motion>", on_drag)  # ドラッグイベントのバインド
    canvas.bind("<ButtonRelease-1>", on_release)  # リリースイベントのバインド

    root.mainloop()