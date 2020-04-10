# -*- coding: UTF-8 -*-

import tkinter as tk
import tkinter.messagebox
import onmyoji

window = tk.Tk()
window.title("阴阳师辅助")

def hello():
    onmyoji.base_process("baiguiyexing",1)
    # tk.messagebox.showinfo(title="Hello")

button_baiguiyexing = tk.Button(window,text="百鬼夜行",command=hello)
button_baiguiyexing.pack()

# 进入消息循环
window.mainloop()