import time
import View.ScanView
from View.View import AbstractView
from Model.Attacks.DeauthAttack import DeauthAttack, TestAttack
from tkinter import ttk
import tkinter as tk
from tkinter import END

class AttackView(AbstractView):

    def __init__(self, parent):
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

        self.stop_btn = ttk.Button(self, text="Back")
        self.stop_btn.bind('<Button-1>', self.go_back)
        self.stop_btn.grid(row=0, column=0, sticky='w')


        self.stop_btn = ttk.Button(self, text="Stop", width=10)
        self.stop_btn.bind('<Button-1>', self.test_attack)
        self.stop_btn.grid(row=box_r + 2, column=0, sticky='w')

        self.check_report_btn = ttk.Button(self, text='Check report')
        self.check_report_btn.bind('<Button-1>', self.open_report)
        self.check_report_btn.grid(row=box_r + 2, column=0, sticky='e', padx=(0,120))

        self.check_report_btn = ttk.Button(self, text='Start', style="Accent.TButton", width=10)
        self.check_report_btn.bind('<Button-1>', self.test_attack)
        self.check_report_btn.grid(row=box_r + 2, column=0, sticky='e')

    def go_back(self, event):
        self.controller.change_view(View.ScanView.ScanView)
    
    def open_report(self, event):
        pass

    def test_attack(self, event):
        #t0 = time.time()
        """t1= time.time()
            while t1 - t0 < 1:
                t1 = time.time()
            t0 = time.time()"""
        #self.controller.attack_plan.attack_list = TestAttack
        for path in self.controller.attack_target():

            self.parent.update()
            self.info_box.insert('end', path)
            

    def show_error():
        pass