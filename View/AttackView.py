from View.View import AbstractView
from tkinter import ttk
import tkinter as tk
from tkinter import END

class AttackView(AbstractView):

    def __init__(self, parent):
        super().__init__(parent)
        
        self.label = ttk.Label(self, text="here comes the target info")
        self.label.grid(row=0, column=0, pady=(20, 0))

        box_r, box_c = 1, 0
        self.info_box = tk.Text(self, height=20, width=60)


        vsb = ttk.Scrollbar(orient="vertical", command=self.info_box.yview)
        
        self.info_box.configure(yscrollcommand=vsb.set)
    
        self.info_box.grid(column=box_c, row=box_r, sticky='nsew', in_=self)
        vsb.grid(column=box_c+1, row=box_r, sticky='ns', in_=self)

        self.stop_btn = ttk.Button(self, text="Stop")
        self.stop_btn.grid(row=box_r + 2, column=0, sticky='w')

    def show_error():
        pass