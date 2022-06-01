
from tkinter import NORMAL, DISABLED, Toplevel, ttk
import tkinter as tk
from tkinter.messagebox import showerror

from View.View import AbstractView
import View.AppView
import tkinter.font as tkFont
from View.View import AbstractView


class ReportListView(AbstractView):

    def __init__(self, parent, controller=None): 
        super().__init__(parent, controller)
        self.parent = parent
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.tv = None
        # NETWORK LIST WITH SCROLLBAR:
        self.tv = self.create_treeview(r=0,c=0)
        #self.tv.bind('<<TreeviewSelect>>', self.net_list_selected)
        
        self.back_btn = ttk.Button(self, text="Back")
        self.back_btn.bind('<Button-1>', self.go_back)
        self.back_btn.grid(row=2, column=0, sticky='w')   

        self.get_reports()     
    
    # -- WIDGET CREATION ---

    def create_treeview(self, c, r) -> ttk.Treeview:
        self.columns = ('Name', 'Date', 'Target')
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

    def get_reports(self) -> None:
        reports = self.controller.get_reports()
        print(reports)
        for n in reports:
            self.tv.insert('', tk.END, values=tuple(n))
            #for ix, val in enumerate(tuple(n)):
            #    col_w = tkFont.Font().measure(val)
            #    if self.tv.column(self.columns[ix],width=None)<col_w:
            #        self.tv.column(self.columns[ix], width=col_w)

    # -- FUNCTIONS ---
    def go_back(self, event):
        self.controller.change_view(View.AppView.AppView)

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
