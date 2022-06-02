import time
from Model.Attacks.EvilTwin import EvilTwin
from View.AttackWindow import AttackWindow
import View.ScanView
from View.View import AbstractView
from Model.Attacks.DeauthAttack import DeauthAttack, TestAttack
from tkinter import ttk
import tkinter as tk
from tkinter import END

from View.VisualizeReportView import VisualizeReport

class AttackView(AbstractView):

    def __init__(self, parent, controller=None):
        super().__init__(parent)

        self.parent = parent
        
        self.label = ttk.Label(self, text="TARGET: ESSID: My personal net. MAC: f1:0b:01:00:ab:a0. CHANNEL: 6. PROTOCOL: WPA2")
        self.label.grid(row=0, column=0, pady=(20, 0))

        box_r, box_c = 1, 0
        self.info_box = tk.Text(self, height=20, width=100)

        vsb = ttk.Scrollbar(orient="vertical", command=self.info_box.yview)
        
        self.info_box.configure(yscrollcommand=vsb.set)
    
        self.info_box.grid(column=box_c, row=box_r, sticky='nsew', in_=self, pady=10)
        vsb.grid(column=box_c+1, row=box_r, sticky='ns', in_=self)

        self.back_btn = ttk.Button(self, text="Back")
        self.back_btn.bind('<Button-1>', self.go_back)
        self.back_btn.grid(row=0, column=0, sticky='w')

        self.stop_btn = ttk.Button(self, text="Stop", width=10, state="disabled")
        self.stop_btn.bind('<Button-1>', self.stop_attack)
        self.stop_btn.grid(row=box_r + 2, column=0, sticky='w')

        self.check_report_btn = ttk.Button(self, text='Check report')
        self.check_report_btn.bind('<Button-1>', self.open_report)
        self.check_report_btn.grid(row=box_r + 2, column=0, sticky='e', padx=(0,120))

        self.start_btn = ttk.Button(self, text='Start', style="Accent.TButton", width=10)
        self.start_btn.bind('<Button-1>', self.test_attack)
        self.start_btn.grid(row=box_r + 2, column=0, sticky='e')

        self.extra_windows = dict()

    def go_back(self, event):
        self.controller.change_view(View.ScanView.ScanView)
    
    def stop_attack(self, event):
        self.start_btn["state"] = "normal"
        self.check_report_btn["state"] = "normal"
        self.stop_btn["state"] = "disabled"


    def open_report(self, event):
        popup = VisualizeReport(self, self.controller.get_report_info(id=None))

    def test_attack(self, event):
        self.start_btn["state"] = "disabled"
        self.check_report_btn["state"] = "disabled"
        self.stop_btn["state"] = "normal"
        #for n in range(3):
        #    self.create_extra_window('window' + str(n))
        #t0 = time.time()
        """t1= time.time()
            while t1 - t0 < 1:
                t1 = time.time()
            t0 = time.time()"""
        #self.controller.attack_plan.attack_list = EvilTwin
        
        for path in self.controller.attack_target():
            if len(self.extra_windows) != 0:
                print(path[0], path[1])
                if path[0] in self.extra_windows:
                    self.extra_windows[path[0]].put_data(path[1])
                    self.parent.update()
                else:
                    self.info_box.insert('end', path + "\n")
                    self.info_box.see('end')
                    self.parent.update()
            else:
                self.info_box.insert('end', path + "\n")
                self.info_box.see('end')
                self.parent.update()
        

    def create_extra_window(self, name):
        windows = len(self.extra_windows)
        if windows < 1: mod = 2
        else: mod = -2
        x = self.winfo_x() + 200*(windows % mod)
        y = self.winfo_y() + 200*(windows+1%mod)
        self.extra_windows[name] = AttackWindow(self, name, pos=(x,y))

    def show_error():
        pass