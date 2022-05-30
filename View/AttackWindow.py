
from tkinter import Toplevel, ttk
import tkinter as tk


class AttackWindow(Toplevel):

    def __init__(self, parent, name, pos=(0,0)):
        
        super().__init__(parent)
        self.parent = parent
        self.name = name
        self.title(self.name)
        self.geometry("+%d+%d" %(pos[0], pos[1]))

        self.text_box = tk.Text(self, height=20, width=80)
        self.text_box.grid(row=0, column=0)

    def put_data(self, data: str):
        self.text_box.insert('end', data)
        self.text_box.see('end')
    

    