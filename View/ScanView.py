from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo
from View import View

class ScanView(ttk.Frame):

    def __init__(self, parent): 
        super().__init__(parent)
        
        self.label = ttk.Label(self, text='Second page')
        self.label.grid(row=1, column=0)

        self.scan_button = ttk.Button(self, text="Scan networks")
        self.scan_button.bind('<<ListboxSelect>>', self.scan_button_clicked)
        self.scan_button.grid(row=2, column=0)

        self.networks_listbox = tk.Listbox(self, height=5, selectmode='browse')
        self.networks_listbox.grid(row=3, column=0)

        self.controller = None
    
    def set_controller(self, controller):
        self.controller = controller

    # -- EVENTS ---
    def scan_button_clicked(self, event):
        print('Im clicked')