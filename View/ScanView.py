from tkinter import NORMAL, DISABLED, Toplevel, ttk
import tkinter as tk
from tkinter.messagebox import showerror
from turtle import width

from View.View import AbstractView
from View.AttackOptions import TestOptions
from View.AttackView import AttackView
import View.AppView
import time
import tkinter.font as tkFont

# https://stackoverflow.com/questions/5286093/display-listbox-with-columns-using-tkinter

class ScanView(AbstractView):

    def __init__(self, parent, controller=None): 
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        parent.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.tv = None
        # SIDE BUTTONS
        self.start_test_btn = ttk.Button(self, text="Start Testing", state=DISABLED, style="Accent.TButton")
        self.start_test_btn.grid(row=0, column=0, sticky='NWE', padx=10)

        self.config_test_btn = ttk.Button(self, text="Test Options", state=DISABLED, style="Accent.TButton")
        self.config_test_btn.grid(row=0, column=0, sticky='NWE', pady='40', padx=10)

        self.tools_btn = ttk.Button(self, text="Other tools", style="Accent.TButton")
        self.tools_btn.bind('<Button-1>', self.open_tools)
        self.tools_btn.grid(row=0, column=0, sticky='NWE', pady='80', padx=10)

        # SCAN BUTTON
        self.scan_btn = ttk.Button(self, text="Scan networks", style="Accent.TButton")
        self.scan_btn.bind('<Button-1>', self.scan_btn_clicked)
        self.scan_btn.grid(row=2, column=1, sticky='E')

        self.scan_btn = ttk.Button(self, text="Back")
        self.scan_btn.bind('<Button-1>', self.go_back)
        self.scan_btn.grid(row=2, column=0, sticky='S')
        
        # NETWORK LIST WITH SCROLLBAR:
        self.tv = self.create_treeview(r=0,c=1)
        self.tv.bind('<<TreeviewSelect>>', self.net_list_selected)

        # PROGRESS BAR
        self.scan_progress = ttk.Progressbar(self, orient=tk.HORIZONTAL,
                                            length=200, mode='indeterminate')

        self.process_networks(scan=False)
        self.options_popup = None
        self.tools_popup = None
        self.target_properties = None
        self.controller = None

    
    # -- WIDGET CREATION ---

    def create_treeview(self, c, r) -> ttk.Treeview:
        self.columns = (' ESSID', 'BSSID',' channel', ' Privacy', ' Cipher', ' Authentication')
        tv = ttk.Treeview(self, columns=self.columns, 
                            show='headings', height=10, selectmode='browse')

        vsb = ttk.Scrollbar(orient="vertical", command=tv.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=tv.xview)

        tv.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tv.grid(column=c, row=r, sticky='nsew', in_=self)
        vsb.grid(column=c+1, row=r, sticky='ns', in_=self)
        hsb.grid(column=c, row=r+1, sticky='ew', in_=self)

        for i, col in enumerate(self.columns):
            tv.column(column=i, width=100)
            tv.heading(col, text=str(col),
                command=lambda c=col: self.sortby(c, 0))
        
        return tv

    # -- EVENTS ---


    def open_tools(self, event) -> None:
        self.tools_popup = Toplevel()
        
        # WORDLIST
        self.wordlist_btn = ttk.Button(self.tools_popup, text='Create Wordlist', style="Accent.TButton",  width=15)
        self.wordlist_btn.grid(row=1,column=0, pady=10, padx=10,)
        self.wordlist_btn.bind('<Button-1>', self.create_dict)

        self.word_info =ttk.Label(self.tools_popup, text='Enter key words, separated by coma.')
        self.word_info.grid(row=0, column=0, columnspan=2, pady=10)

        self.entry_words = ttk.Entry(self.tools_popup)  
        self.entry_words.grid(row=1, column=1, padx=10)

        # MAC CHANGE:
        
        self.generate_mac_btn = ttk.Button(self.tools_popup, text='Generate MAC', style="Accent.TButton", width=15)
        self.generate_mac_btn.grid(row=3, column=0, pady=10, padx=10, sticky='W')
        self.generate_mac_btn.bind('<Button-1>', self.change_mac)
        
        self.mac_info = ttk.Label(self.tools_popup, text='Generate a new MAC or type your own')
        self.mac_info.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        
        self.mac_entry = ttk.Entry(self.tools_popup)
        self.mac_entry.grid(row=3, column=1, padx=10)

    def change_mac(self, event):
        self.controller.change_mac(mac=self.mac_entry.get())

    def create_dict(self, event) -> None:
        self.controller.create_wordlist(self.entry_words.get())
                

    def net_list_selected(self, event) -> None:
        currItem = self.tv.focus()
        self.target_properties = self.tv.item(currItem)['values']
        #FIXME self.target_properties a dict
        self.controller.change_target(bssid=self.target_properties[1],
                                      essid=self.target_properties[0],
                                      protocol=self.target_properties[3],
                                      channel=self.target_properties[2])

        self.start_test_btn["state"] = NORMAL
        self.start_test_btn.bind('<Button-1>', self.start_testing_clicked)

        self.config_test_btn["state"] = NORMAL
        self.config_test_btn.bind('<Button-1>', self.config_testing_clicked)

    def start_testing_clicked(self, event) -> None:
        '''
        Creates a popup that shows a summary of the test plan
        '''
        if self.options_popup:
            self.options_popup.destroy()
        self.controller.change_view(AttackView)
    

    def config_testing_clicked(self, event) -> None:
        '''
        A popup is created showing the protocol's possible attack options
        '''
        if self.options_popup:
            self.options_popup.destroy()

        self.options_popup = TestOptions(self)
        target_info = self.controller.get_target_info()
        attack_list = self.controller.protocol_attacks(target_info['protocol'])
        self.options_popup.show_options(attack_list=attack_list)

    def process_networks(self, scan):
        networks = self.controller.get_networks(scan=scan)

        if not networks:
             return

        for n in networks:
            parsed_net = ['-' if not i.strip() else i for i in n]
            self.tv.insert('', tk.END, values=tuple(parsed_net))

            for ix, val in enumerate(tuple(parsed_net)):
                col_w = tkFont.Font().measure(val)
                if self.tv.column(self.columns[ix],width=None)<col_w:
                    self.tv.column(self.columns[ix], width=col_w)

    def scan_btn_clicked(self, event) -> None:
        self.tv.delete(*self.tv.get_children())
        self.process_networks(scan=True)

    def go_back(self, event):
        self.controller.change_view(View.AppView.AppView)
            
    # -- FUNCTIONS ---

    def hide_stop_progress(self) -> None:
        self.scan_progress.stop()
        self.scan_progress.grid_forget()

    def show_error(self, ex):
        showerror(title='Error', message=str(ex))

    def sortby(self,col, descending) -> None:
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
