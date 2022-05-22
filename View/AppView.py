from tkinter import Toplevel, ttk
import tkinter as tk
from tkinter.messagebox import showerror
from View.View import AbstractView

class AppView(AbstractView):

    def __init__(self, parent): 
        super().__init__(parent)

        self.label = ttk.Label(self, text='Welcome to Wifipy', font=(25))
        self.label.grid(row=0, column=0, pady=20)
        """
        self.combobox = ttk.Combobox(self)
        self.combobox.bind('<Button-1>', self.interface_changed)
        self.combobox.grid(row=1, column=0)

        self.startButton = ttk.Button(self, text="Continue")
        self.startButton.bind('<Button-1>', self.nextButton_clicked)
        self.startButton.grid(row=3, column=0)
        """
        self.startButton = ttk.Button(self, text="Start", style="Accent.TButton", width=50)
        self.startButton.bind('<Button-1>', self.interface_window)
        self.startButton.grid(row=1, column=0, pady=5)


        reports_button = ttk.Button(self, text='Reports', width=50)
        reports_button.grid(row=2, column=0, pady=5)
        
        quit_button = ttk.Button(self, text='Quit', width=50)
        quit_button.grid(row=3, column=0, pady=5)

        self.popup = None
        self.controller = None

    def interface_window(self, event):
        if self.popup:
            self.popup.destroy
        self.popup = Toplevel()

        ttk.Label(self.popup, text='Select an interface to start', font=(25)).grid(row=0,column=0, pady=20, padx=20)
        
        self.combobox = ttk.Combobox(self.popup, width=25)
        self.combobox.bind('<Button-1>', self.interface_changed)
        self.combobox.grid(row=1, column=0, padx=10)

        self.startButton = ttk.Button(self.popup, text="Continue", style="Accent.TButton")
        self.startButton.bind('<Button-1>', self.nextButton_clicked)
        self.startButton.grid(row=2, column=0, pady=10, padx=10, sticky='EW')

    #-----EVENTS-------:
    def interface_changed(self, event):
        self.combobox['values'] = self.controller.get_list_interfaces()

    def nextButton_clicked(self, event):
        if self.combobox.get() == "":
            showerror(title='Error', message='Please select an interface')
        else:
            info = self.combobox.get()
            if info:
                ifs_name = info[:info.find(':')]
                self.controller.selected_interface(ifs_name)
                self.popup.destroy()
    

    def show_error(self, ex):
        showerror(title='Error', message=str(ex))