"""

Created on Thu Mar 14, 2024

@author: shriafujilab

Purpose:
    The code privide GUI config

"""

# import standard library
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import sys
import os

# import my library
from src.graphics.block_code import BlockSnippet
from src.graphics.block_code import BlockCompiler




class MainWindow:
    def __init__(self, master, params, config):

        """Initialize the main window"""
        self.master = master
        self.params = params
        self.config = config

        self.entries ={}
        
        """ Parameters """
        
        self.pos_x = 10 # "if" = 10, "elif", and "else" = 40
        self.pos_y = 25
        
        # blocks
        self.blocks = []
        self.selected_block = None
        self.last_block = None

        self.create_widgets()



    def create_widgets(self):

        # Create control frame
        self.create_control_frame()

        # Create aimation frame
        self.create_animation_frame()

        # Create Interactive Frame()
        self.create_interactive_frame()

        # Figure configure
        #self.root.rowconfigure(0, weight=2)
        #self.root.rowconfigure(1, weight=3)
        #self.root.rowconfigure(2, weight=1)
        #self.root.rowconfigure(3, weight=1)


    def create_control_frame(self):

        # Config Style of Main Frame
        style = ttk.Style()
        style.configure("Co.TFrame", background="gray")

        # Create Main Frame (control)
        main_frame = ttk.Frame(self.master.root, style="Co.TFrame", height=400, width=320, padding = "3 3 12 12")
        main_frame.grid(row=0, column=0, sticky="nsew")

        notebook = ttk.Notebook(main_frame, height=380, width=300, padding="3 3 3 3")
        notebook.grid(row=0, column=0, padx=10, pady=10)

        # Tab1: Introduction
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Introduction")
        self.setting_tab1(tab1)

        # Tab2: Introduction
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Basic")
        self.setting_tab2(tab2)

        # Tab3: Introduction
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="Practice")
        self.setting_tab3(tab3)


    def setting_tab1(self, tab):

        """ row = 0: detemine maze """
        
        row_frame1 = ttk.Frame(tab)
        row_frame1.grid(row=0, column=0, columnspan=2)
        
        label1 = ttk.Label(row_frame1, text="width")
        label1.grid(row=0, column=0)
        
        entry1 = ttk.Entry(row_frame1, width=5)
        entry1.grid(row=0, column = 1)
        entry1.insert(0, str(self.config["maze_width"]))
        self.entries["maze_width_config"] = entry1
        
        label2 = ttk.Label(row_frame1, text="height")
        label2.grid(row=0, column=2)
        
        entry2 = ttk.Entry(row_frame1, width=5)
        entry2.grid(row=0, column = 3)
        entry2.insert(0, str(self.config["maze_height"]))
        self.entries["maze_height_config"] = entry2
        
        button1 = ttk.Button(row_frame1, text="迷路再生成", command=self.master.regeneration)
        button1.grid(row=0, column=4)

        """ row = 1: determine explorer method """

        # method select

        def on_combobox_select(event):
            self.params["method"] = combo.get()
            print(self.params["method"])

        combo = ttk.Combobox(tab)

        combo["values"] = ("左手法", "トレモー法")
        combo.current(0)
        combo.bind("<<ComboboxSelected>>", on_combobox_select)
        combo.grid(row=1, column = 0)

        # execute the method

        button2 = ttk.Button(tab, text="実行", command=self.master.exploration)
        button2.grid(row=1, column=1)




    def create_animation_frame(self):

        # Config Style of Main Frame
        style = ttk.Style()
        style.configure("An.TFrame", background="cyan")

        # Create Main Frame (animation)
        self.animation_frame = ttk.Frame(self.master.root, style="An.TFrame", height=self.config["maze_height_pixel"], width = self.config["maze_width_pixel"], padding="3 3 12 12")
        self.animation_frame.grid(row=0, column=1, sticky="nsew")


    def create_interactive_frame(self):

        # Config Style of Main Frame
        style = ttk.Style()
        style.configure("Intract.TFrame", background="lightgray")

        # Config Interactive Frame
        main_frame = ttk.Frame(self.master.root, style="Intract.TFrame", height=100, width=800, padding="3 3 12 12")
        main_frame.grid(row=1, column=0, columnspan =2, sticky="nsew")

        self.micro_mouse_debug_controller(main_frame)


    def micro_mouse_debug_controller(self, main_frame):

        # left frame (blank)
        frame01 = ttk.Frame(main_frame, style="Intract.TFrame", height=100, width=320, padding="3 3 12 12")
        frame01.grid(row=0, column=0,sticky="nsew")

        # right frame (controller)
        frame02 = ttk.Frame(main_frame, style="Intract.TFrame", height=100, width=480, padding="3 3 12 12")
        frame02.grid(row=0, column=1,sticky="nsew")

        # blanks
        blank1 = ttk.Frame(frame02, height=30, width=100)
        blank1.grid(row=0, column=0, sticky="nsew")

        blank2 = ttk.Frame(frame02, height=30, width=100)
        blank2.grid(row=0, column=2, sticky="nsew")

        """ buttons click """

        # buttons
        button_up = tk.Button(frame02, text="↑", command=lambda: self.master.cursor_click("up"))
        button_up.grid(row=0, column=1, sticky = "nsew")
        button_up.bind()

        button_lf = tk.Button(frame02, text="←", command=lambda: self.master.cursor_click("left"))
        button_lf.grid(row=1, column=0, sticky = "nsew")

        button_dw = tk.Button(frame02, text="↓", command=lambda: self.master.cursor_click("down"))
        button_dw.grid(row=1, column=1, sticky = "nsew")

        button_rg = tk.Button(frame02, text="→", command=lambda: self.master.cursor_click("right"))
        button_rg.grid(row=1, column=2, sticky = "nsew")
        
        self.text = tk.Text(frame02, width=40, height=2)
        self.text.grid(row=0, column=3, rowspan=2, sticky="nsw")
        
        sys.stdout = self

    def write(self, msg):

        self.text.insert(tk.END, msg)
        self.text.see(tk.END)  # Scroll to the end
    
    def flush(self):
        
        pass


    def setting_tab2(self, tab):

        """ upper frame (control panel) """
        control_frame = tk.Frame(tab, height=100, width=320)
        control_frame.grid(row=0, column=0, sticky="nsew")
        
        control_text = ttk.Label(control_frame, text = "選択画面（条件・処理）")
        control_text.grid(row=0, column=0, columnspan=3, sticky="nsew")
        
        
        
        """ lower frame (code snippet) """
        code_snippet = tk.Frame(tab, height= 400, width = 320)
        code_snippet.grid(row=1, column=0, sticky="nsew")
        
        # Canvas (later divided)
        self.canvas = tk.Canvas(code_snippet, width=400, height=300, bg="white")
        self.canvas.grid(row=0, column=0, sticky = "nsew")
        self.canvas_draw_guidelines()
        
        
        """ Set Functions """
        # Combobox (conditions or procedures)
        cf_combo01 = ttk.Combobox(control_frame, width=10)
        cf_combo01["value"] = ("条件分岐", "条件式", "評価", "処理")
        cf_combo01.current(0)       # Init
        cf_combo01.grid(row=1, column=0)

        # Combobox determine by above selects
        self.cf_combo02 = ttk.Combobox(control_frame, width=10)
        self.cf_combo02.grid(row=1, column=1)

        options = {
            "条件分岐"  :("if", "else if", "else"),
            "条件式"    :("左に壁がある", "右に壁がある", "前に壁がある", "後ろに壁がある"),
            "評価"      :("== True", "== False"),
            "処理"      :("左に進む", "右に進む", "前に進む", "後ろに進む", "----"),
        }

        def update_cf_combo02(event):
            chosen_option = cf_combo01.get()
            self.cf_combo02["value"] = options[chosen_option]
            self.cf_combo02.current(0)

        update_cf_combo02(event=None)   # Init
        cf_combo01.bind("<<ComboboxSelected>>", update_cf_combo02)

        cf_button1 = ttk.Button(control_frame, text="ブロック追加", width=12, command=self.add_block)
        cf_button1.grid(row=1, column=2)

        cf_button2 = ttk.Button(control_frame, text="実行", width = 6,command=self.execute_code)
        cf_button2.grid(row=1, column=3)

        """ Canvas Event Binding """
        self.canvas.bind("<Button-1>", self.on_click)   # click
        self.canvas.bind("<B1-Motion>", self.on_drag)   # drag
        self.canvas.bind("<ButtonRelease-1>", self.on_release)  # release
        self.canvas.bind("<Double-Button-3>", self.on_right_double_click)   # right double click


    def add_block(self):
        new_block = BlockSnippet(self.canvas, self.cf_combo02.get(), self.pos_x, self.pos_y)
        self.blocks.append(new_block)


    def execute_code(self):
        print("start")
        # Judge executin order

        inst = BlockCompiler()
        python_code = inst.generate_python_code(self.blocks, self.canvas)
        
        self.master.block_programming(python_code)
        


    """ Canvas Config """
    def canvas_draw_guidelines(self):
        
        # config height of row
        line_spacing = 25
        
        for i in range(10,  400, line_spacing):
            self.canvas.create_line(0, i, 300, i, fill="#a0a0a0", dash=(2, 5))


    """ Canvas Event """

    def on_click(self, event):

        for block in self.blocks:
            coords = self.canvas.coords(block.id)

            if coords[0] <= event.x <= coords[2] and coords[1] <= event.y <= coords[3]:
                # if click on box, do procedure
                self.selected_block = block
                self.last_block = block
                self.selected_block.x, self.selected_block.y = event.x, event.y
                return

    def on_drag(self, event):
        
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


    def on_right_double_click(self, event):
        
        for block in self.blocks:
            coords = self.canvas.coords(block.id)
            if coords[0] <= event.x <= coords[2] and coords[1] <= event.y <= coords[3]:
                block.remove()
                self.blocks.remove(block)
                return
        


    def on_release(self, event):
        if self.selected_block:
            self.selected_block = None



    def setting_tab3(self, tab):

        pass






