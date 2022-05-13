from tkinter import NORMAL, DISABLED, Toplevel, ttk
import tkinter as tk
from tkinter.messagebox import showerror
from View.View import AbstractView
from View.AttackOptions import TestOptions
from View.AttackView import AttackView
import time
import tkinter.font as tkFont

# https://stackoverflow.com/questions/5286093/display-listbox-with-columns-using-tkinter

class ScanView(AbstractView):

    def __init__(self, parent): 
        super().__init__(parent)
        self.parent = parent
        parent.protocol("WM_DELETE_WINDOW", self.on_closing)

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

        self.options_popup = None
        self.target_properties = None
        self.controller = None

    
    # -- WIDGET CREATION ---

    def create_treeview(self, c, r) -> ttk.Treeview:
        self.columns = (' ESSID', 'BSSID',' channel', ' Privacy', ' Cipher', ' Authentication')
        tv = ttk.Treeview(self, columns=self.columns, 
                            show='headings', height=10, selectmode='browse')
        tv.grid(row=0, column=0)

        vsb = ttk.Scrollbar(orient="vertical", command=tv.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=tv.xview)

        tv.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tv.grid(column=c, row=r, sticky='nsew', in_=self)
        vsb.grid(column=c+1, row=0, sticky='ns', in_=self)
        hsb.grid(column=0, row=r+1, sticky='ew', in_=self)

        for i, col in enumerate(self.columns):
            tv.column(column=i, width=100)
            tv.heading(col, text=str(col),
                command=lambda c=col: self.sortby(c, 0))
        
        return tv

    # -- EVENTS ---

    def net_list_selected(self, event) -> None:
        currItem = self.tv.focus()
        self.target_properties = self.tv.item(currItem)['values']
        #TODO self.target_properties a dict
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
        #TODO to class
        self.summary_popup = Toplevel()
        self.summary_popup.geometry("300x400")
        
        ttk.Label(self.summary_popup, text='Summary').grid(row=0, column=0)
        
        for idx, attack in enumerate(self.controller.get_plan()):
            ttk.Label(self.summary_popup, text=attack.attack_name()).grid(row=idx+1, column=0)

        attack_button = ttk.Button(self.summary_popup, text='Continue')
        attack_button.bind('<Button-1>', self.summary_continue_btn)
        attack_button.grid(row=len(self.controller.get_plan())+2, column=0)

    
    def summary_continue_btn(self, event) -> None:
        '''
        Event fired when the continue button from summary popup is clicked.
        '''
        self.summary_popup.destroy()
        if self.options_popup:
            self.options_popup.destroy()
        self.controller.change_view(AttackView)
        #self.controller.attack_target()

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


    def scan_btn_clicked(self, event) -> None:
        networks = self.controller.get_networks()

        for n in networks:
            parsed_net = ['-' if not i.strip() else i for i in n]
            self.tv.insert('', tk.END, values=tuple(parsed_net))

            for ix, val in enumerate(tuple(parsed_net)):
                col_w = tkFont.Font().measure(val)
                if self.tv.column(self.columns[ix],width=None)<col_w:
                    self.tv.column(self.columns[ix], width=col_w)
            
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