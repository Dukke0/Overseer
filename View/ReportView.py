
from tkinter import NORMAL, DISABLED, Toplevel, ttk
import tkinter as tk
from tkinter.messagebox import WARNING, askokcancel, showerror, showinfo, showwarning
from tkinter import filedialog

from View.View import AbstractView
import View.AppView
import tkinter.font as tkFont
from View.View import AbstractView
from View.VisualizeReportView import VisualizeReport


class ReportListView(AbstractView):

    def __init__(self, parent, controller=None): 
        super().__init__(parent, controller)
        self.parent = parent
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        title = ttk.Label(self, text="Reports", font=(tk.font.BOLD, 15))
        title.grid(row=0, column=0, sticky='W', padx=20, pady=20)

        self.tv = None
        # NETWORK LIST WITH SCROLLBAR:

        self.tv = self.create_treeview(r=1,c=0)
        #self.tv.bind('<<TreeviewSelect>>', self.net_list_selected)

        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label='View', command=self.view_report)
        self.popup_menu.add_command(label='Export to json', command=self.export_json)
        self.popup_menu.add_command(label='Export to txt', command=self.export_txt)
        self.popup_menu.add_command(label='Delete', command=self.delete)

        self.tv.bind('<Button-3>', self.popup)
        self.back_btn = ttk.Button(self, text="Back")
        self.back_btn.bind('<Button-1>', self.go_back)
        self.back_btn.grid(row=3, column=0, sticky='w', padx=(20,0))   

        self.get_reports()     
    
    def view_report(self):
        if self.iid:
            currItem = self.tv.focus()
            val = self.tv.item(currItem)['values']
            self.controller.get_report_info(id=val[0])
            self.report_popup = VisualizeReport(self, report_info=self.controller.get_report_info(id=val[0]))

    def delete(self):
        if self.iid:
            if askokcancel(title='Confirmation', message='Deleting will delete all the data.', icon=WARNING):
                currItem = self.tv.focus()
                val = self.tv.item(currItem)['values']
                deleted_id = self.controller.delete_report(id=val[0])
                if deleted_id != None:
                    selected_item = self.tv.selection()[0]
                    self.tv.delete(selected_item)
                    showinfo(title='Deletion Status', message='The report has been deleted successfully')

    def popup(self, event):
        self.iid = self.tv.identify_row(event.y)
        if self.iid:
            # mouse pointer over item
            self.tv.focus(self.iid)
            self.tv.selection_set(self.iid)
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        else:
            # mouse pointer not over item
            # occurs when items do not fill frame
            # no action required
            pass

    def export_json(self):
        if self.iid:
            currItem = self.tv.focus()
            val = self.tv.item(currItem)['values']
            files = [('JSON file', '*.json')]
            file_path = filedialog.asksaveasfilename(filetypes = files)
            self.controller.export_report(id=val[0], file_path=file_path, type='json')
        else:
            pass
    
    def export_txt(self):
        if self.iid:
            currItem = self.tv.focus()
            val = self.tv.item(currItem)['values']
            files = [('Text Document', '*.txt')]
            file_path = filedialog.asksaveasfilename(filetypes = files)
            self.controller.export_report(id=val[0], file_path=file_path, type='txt')
        else:
            pass


    # -- WIDGET CREATION ---

    def create_treeview(self, c, r) -> ttk.Treeview:
        self.columns = ('ID', 'Name', 'Date', 'BSSID','ESSID','Protcol','Channel')
        tv = ttk.Treeview(self, columns=self.columns, 
                            show='headings', height=10, selectmode='browse')

        vsb = ttk.Scrollbar(orient="vertical", command=tv.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=tv.xview)

        tv.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tv.grid(column=c, row=r, sticky='nsew', in_=self, padx=(20,0))
        vsb.grid(column=c+1, row=r, sticky='ns', in_=self, padx=(0, 20))
        hsb.grid(column=c, row=r+1, sticky='ew', in_=self, padx=(20,0), pady=(0,20))

        for i, col in enumerate(self.columns):
            tv.column(column=i, width=100)
            tv.heading(col, text=str(col),
                command=lambda c=col: self.sortby(c, 0))
        
        return tv

    def get_reports(self) -> None:
        reports = self.controller.get_reports()
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
