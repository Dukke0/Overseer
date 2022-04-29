from tkinter import StringVar, ttk
import tkinter as tk
from tkinter.messagebox import showinfo
from View.View import AbstractView

class ScanView(AbstractView):

    def __init__(self, parent): 
        super().__init__(parent)
        
        self.label = ttk.Label(self, text='Second page')
        self.label.grid(row=1, column=0)

        self.scan_button = ttk.Button(self, text="Scan networks")
        self.scan_button.bind('<Button-1>', self.scan_button_clicked)
        self.scan_button.grid(row=2, column=0)

        self.list_networks = StringVar()
        self.networks_listbox = tk.Listbox(self, listvariable=self.list_networks,
                                            height=10, width=50, selectmode='browse')

        self.networks_listbox.grid(row=3, column=0)

        self.controller = None

    # -- EVENTS ---
    def scan_button_clicked(self, event):
        networks = self.controller.get_networks()
        self.list_networks.set(networks)

    def show_error(self, ex):
        showinfo(title='Error', message=str(ex))