
from tkinter import Toplevel
from tkinter import ttk

from Model.Attacks.AbstractAttack import AbstractAttack


class TestOptions(Toplevel):

    def __init__(self, parent):
        
        super().__init__(parent)

        self.label = ttk.Label(self, text='Available attacks').grid(row=0, column=0)
    

    def show_options(self, attack_list: tuple) -> None:
        for idx, a in enumerate(attack_list):
            self.create_option(a, idx)

    def create_option(self, option: AbstractAttack, idx: int):
        print(repr(option))
        ttk.Checkbutton(self, text='Option ' + option.attack_name()).grid(row=idx+1, column=0)
        

        

