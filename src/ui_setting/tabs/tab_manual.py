# -*- coding: utf-8 -*-

"""

Created on: 2024-12-05

@author:  shirafujilab

Contents:

    User Manual


"""

import tkinter
from tkinter import ttk
from tkinter import font



def set_manual_tab(tab):

        # Custom font
        custom_font = font.Font(family="明朝", size=12, weight="bold")

        title1 = ttk.Label(tab, text = "簡易マニュアル", font=custom_font)
        title1.grid(row=0, column=0)

        blank1 = ttk.Label(tab, text="")
        blank1.grid(row=1, column=0)

        """ msg_frame1 (row=2, 3): コードスニペットの仕様 """

        msg_frame1_title = ttk.Label(tab, text = "コードスニペットの仕様", font=custom_font)
        msg_frame1_title.grid(row=2, column=0)

        msg_frame1 =  ttk.Frame(tab)
        msg_frame1.grid(row=3, column=0)

        msg1_1 = ttk.Label(msg_frame1, text = "if 文の下の処理文の前にはインデントを付けよう．")
        msg1_1.grid(row=0, column=0)

        msg1_1 = ttk.Label(msg_frame1, text = " ")
        msg1_1.grid(row=1, column=0)

        msg1_3 = ttk.Label(msg_frame1, text = "ただしい例")
        msg1_3.grid(row=2, column=0)

        msg1_4 = ttk.Label(msg_frame1, text = "if 左に壁がある == False")
        msg1_4.grid(row=3, column=0)

        msg1_5 = ttk.Label(msg_frame1, text = "---- 左に進む           ")
        msg1_5.grid(row=4, column=0)

        msg1_6 = ttk.Label(msg_frame1, text = " ")
        msg1_6.grid(row=5, column=0)

        msg1_7 = ttk.Label(msg_frame1, text = "※ ---- はインデントというpython の必須概念です．")
        msg1_7.grid(row=6, column=0)

        msg1_8 = ttk.Label(msg_frame1, text = "　 Cでは関係ないと思う方も多いと思いますが，")
        msg1_8.grid(row=7, column=0)

        msg1_9 = ttk.Label(msg_frame1, text = "　 見やすいコードを書く上で大切な概念です．")
        msg1_9.grid(row=7, column=0)

        blank2 = ttk.Label(tab, text = "")
        blank2.grid(row=4, column= 0)

        """ msg_frame2 (row=5, 6): 迷路を右クリックすると """

        msg_frame2_title = ttk.Label(tab, text = "迷路を右クリックすると．．．", font=custom_font)
        msg_frame2_title.grid(row=5, column=0)

        msg_frame2 =  ttk.Frame(tab)
        msg_frame2.grid(row=6, column=0)

        msg2_1 = ttk.Label(msg_frame2, text = "道 -> 壁 -> Start -> Goal の順で変わるよ．")
        msg2_1.grid(row=0, column=0)