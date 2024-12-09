# -*- coding: utf-8 -*-

"""

Created on: 2024-12-05

@author:  shirafujilab

Contents:

    Practice


"""

import tkinter as tk
from tkinter import ttk

def set_practice_tab(tab):

    msg1 = ttk.Label(tab, text = "準備中")
    msg1.grid(row=0, column=0)

    msg2 = ttk.Label(tab, text= "実験６でやったような，センサ・モータの制御も")
    msg2.grid(row=1, column=0, sticky = tk.W)

    msg3 = ttk.Label(tab, text= "必要な物を作成予定です．")
    msg3.grid(row=2, column=0, sticky=tk.W)