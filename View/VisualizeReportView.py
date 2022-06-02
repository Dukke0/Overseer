from tkinter import Toplevel, filedialog
from tkinter import ttk
import tkinter as tk

from sqlalchemy import column

class VisualizeReport(tk.Toplevel):

    def __init__(self, parent, report_info):
        super().__init__(parent)
        self.parent = parent

        box_c, box_r = 0, 0
        self.info_box = tk.Text(self)
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.info_box.yview)

        self.info_box.configure(yscrollcommand=vsb.set)
    
        self.info_box.grid(column=box_c, row=box_r, sticky='nsew', in_=self, pady=(20,10), padx=(20,0))
        vsb.grid(column=box_c+1, row=box_r, sticky='ns', pady=(20,10), padx=(0,20))

        self.export_btn = ttk.Button(self, text='Export', style="Accent.TButton", command=self.export)
        self.export_btn.grid(row=box_r+1, column=box_c, sticky='e', pady=(0,10))

        self.info_box.insert(tk.END, report_info)
    
    def export(self):
        files = [('JSON file', '*.json')]
        file_path = filedialog.asksaveasfilename(filetypes = files)
        self.parent.controller.export_report(id=None, file_path=file_path, type='json')
        self.destroy()

