
from tkinter import Toplevel
from tkinter import ttk
from functools import partial

from Model.Attacks.AbstractAttack import AbstractAttack


class TestOptions(Toplevel):

    def __init__(self, parent):
        
        super().__init__(parent)

        self.label = ttk.Label(self, text='Available attacks').grid(row=0, column=0)
        self.options = list()
        print(parent)
    
    def change(self, n):
        btn, attack = self.options[n]
        print(parent)        

    def show_options(self, attack_list: tuple) -> None:
        self.options.clear()
        for idx, a in enumerate(attack_list):
            self.create_option(a, idx)

    def create_option(self, option: AbstractAttack, idx: int):
        cb = ttk.Checkbutton(self, text='Option ' + option.attack_name(), command=partial(self.change, idx))
        cb.grid(row=idx+1, column=0)
        self.options.append((cb, option))
        
        

        


