
from tkinter import Toplevel
from tkinter import ttk
from functools import partial

from Model.Attacks.AbstractAttack import AbstractAttack


class TestOptions(Toplevel):

    def __init__(self, parent):
        
        super().__init__(parent)

        self.parent = parent
        self.label = ttk.Label(self, text='Available attacks',  font=(25)).grid(row=0, column=0, pady=10)
        self.options = list()
    
    def change(self, n):
        btn, attack = self.options[n]
        if 'selected' in btn.state():
            self.parent.controller.add_attack_to_plan(attack)
        else:
            self.parent.controller.remove_attack_from_plan(attack)
        
    def show_options(self, attack_list: tuple) -> None:
        self.options.clear()
        for idx, a in enumerate(attack_list):
            self.create_option(a, idx)
        self.accept_btn = ttk.Button(self, text='Accept', style="Accent.TButton", width=10, command=self.accept)
        self.accept_btn.grid(row=len(attack_list) + 2, column=0, pady=10)

    def accept(self) -> None:
        self.destroy()

    def create_option(self, option: AbstractAttack, idx: int):
        cb = ttk.Checkbutton(self, text='Option ' + option.attack_name(), command=partial(self.change, idx))
        cb.state(['!alternate'])
        cb.grid(row=idx+1, column=0, sticky='W', pady=5, padx=10)
        self.options.append((cb, option))

