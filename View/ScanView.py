from tkinter import NORMAL, DISABLED, StringVar, Toplevel, ttk
import tkinter as tk
from tkinter.messagebox import showerror
from View.View import AbstractView
from View.TestOptions import TestOptions
import time

class ScanView(AbstractView):

    def __init__(self, parent): 
        super().__init__(parent)

        #SIDE BUTTONS
        self.start_test_btn = ttk.Button(self, text="Start Testing", state=DISABLED)
        self.start_test_btn.grid(row=2, column=0)

        self.config_test_btn = ttk.Button(self, text="Test Options", state=DISABLED)
        self.config_test_btn.grid(row=3, column=0)

        #SCAN BUTTON
        self.scan_btn = ttk.Button(self, text="Scan networks")
        self.scan_btn.bind('<Button-1>', self.scan_btn_clicked)
        self.scan_btn.grid(row=2, column=1)
        
        # NETORK LIST WITH SCROLLBAR:
        self.list_networks = StringVar()
        self.networks_listbox = tk.Listbox(self, listvariable=self.list_networks,
                                            height=10, width=50, selectmode='browse')
        self.networks_listbox.bind('<<ListboxSelect>>', self.net_list_selected)
        self.networks_listbox.grid(row=4, column=1)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        scrollbar.config(command=self.networks_listbox.yview)
        scrollbar.grid(row=4, column=2, sticky="NS")

        self.networks_listbox.config(yscrollcommand=scrollbar.set)

        #PROGRESS BAR
        self.scan_progress = ttk.Progressbar(self, orient=tk.HORIZONTAL,
                                            length=200, mode='indeterminate')

        self.controller = None


    # -- EVENTS ---

    def net_list_selected(self, event):
        self.start_test_btn["state"] = NORMAL
        self.start_test_btn.bind('<Button-1>', self.start_testing_clicked)

        self.config_test_btn["state"] = NORMAL
        self.config_test_btn.bind('<Button-1>', self.config_testing_clicked)


    
    def start_testing_clicked(self, event):
        pass

    def config_testing_clicked(self, event):
        popup = TestOptions(self)

    def scan_btn_clicked(self, event):

        #self.scan_progress.grid(row=4,column=1)
        #self.scan_progress.start(7)

        networks = self.controller.get_networks()
        self.list_networks.set(networks)

        #self.after(self.controller.get_scan_time()*1000, lambda: self.hide_stop_progress())
    
    # -- FUNCTIONS ---

    def hide_stop_progress(self):
        self.scan_progress.stop()
        self.scan_progress.grid_forget()

    def show_error(self, ex):
        showerror(title='Error', message=str(ex))