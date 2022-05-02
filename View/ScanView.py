from tkinter import NORMAL, DISABLED, StringVar, Toplevel, ttk
import tkinter as tk
from tkinter.messagebox import showerror
from View.View import AbstractView
from View.TestOptions import TestOptions
import time

class ScanView(AbstractView):

    def __init__(self, parent): 
        super().__init__(parent)
        self.tv = None
        # SIDE BUTTONS
        self.start_test_btn = ttk.Button(self, text="Start Testing", state=DISABLED)
        self.start_test_btn.grid(row=2, column=0)

        self.config_test_btn = ttk.Button(self, text="Test Options", state=DISABLED)
        self.config_test_btn.grid(row=3, column=0)

        # SCAN BUTTON
        self.scan_btn = ttk.Button(self, text="Scan networks")
        self.scan_btn.bind('<Button-1>', self.scan_btn_clicked)
        self.scan_btn.grid(row=2, column=2)
        
        # NETWORK LIST WITH SCROLLBAR:
        self.tv = self.create_treeview(0,0)
        self.tv.bind('<<TreeviewSelect>>', self.net_list_selected)

        # PROGRESS BAR
        self.scan_progress = ttk.Progressbar(self, orient=tk.HORIZONTAL,
                                            length=200, mode='indeterminate')


        
        self.controller = None

    
    # -- WIDGET CREATION ---

    def create_treeview(self, c, r):
        columns = (' ESSID', 'BSSID',' channel', ' Privacy', ' Cipher', ' Authentication')
        tv = ttk.Treeview(self, columns=columns, 
                            show='headings', height=5, selectmode='browse')
        tv.grid(row=0, column=0)

        vsb = ttk.Scrollbar(orient="vertical", command=tv.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=tv.xview)

        tv.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tv.grid(column=c, row=r, sticky='nsew', in_=self)
        vsb.grid(column=c+1, row=0, sticky='ns', in_=self)
        hsb.grid(column=0, row=r+1, sticky='ew', in_=self)

        for i, col in enumerate(columns):
            tv.column(column=i, width=100)
            tv.heading(col, text=str(col),
                command=lambda c=col: self.sortby(c, 0))
        
        return tv

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
        print(networks)
        self.list_networks.set(networks)

        #self.after(self.controller.get_scan_time()*1000, lambda: self.hide_stop_progress())
    
    # -- FUNCTIONS ---

    def hide_stop_progress(self):
        self.scan_progress.stop()
        self.scan_progress.grid_forget()

    def show_error(self, ex):
        showerror(title='Error', message=str(ex))

    def sortby(self,col, descending):
        """sort tree contents when a column header is clicked on"""
        # grab values to sort
        data = [(self.tv.set(child, col), child) \
            for child in self.tv.get_children('')]
        
        # if the data to be sorted is numeric change to float
        #data =  change_numeric(data)
        # now sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            self.tv.move(item[1], '', ix)
        # switch the heading so it will sort in the opposite direction
        self.tv.heading(col, command=lambda col=col: self.sortby(col, \
            int(not descending)))