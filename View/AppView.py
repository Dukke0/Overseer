from tkinter import Toplevel, ttk
import tkinter as tk
from tkinter.messagebox import showerror
from View.View import AbstractView

class AppView(AbstractView):

    def __init__(self, parent): 
        super().__init__(parent)
        
        self.label = ttk.Label(self, text='Welcome to Wifipy')
        self.label.grid(row=0, column=1)
        """
        self.combobox = ttk.Combobox(self)
        self.combobox.bind('<Button-1>', self.interface_changed)
        self.combobox.grid(row=1, column=0)

        self.startButton = ttk.Button(self, text="Continue")
        self.startButton.bind('<Button-1>', self.nextButton_clicked)
        self.startButton.grid(row=3, column=0)
        """
        self.startButton = ttk.Button(self, text="Start")
        self.startButton.bind('<Button-1>', self.interface_window)
        self.startButton.grid(row=0, column=0)

        reports_button = ttk.Button(self, text='Reports')
        reports_button.grid(row=1, column=0)
        
        quit_button = ttk.Button(self, text='Quit')
        quit_button.grid(row=2, column=0)

        self.controller = None

    def interface_window(self, event):
        popup = Toplevel()
        popup.geometry("300x400")
        popup.configure(bg='red')

        ttk.Label(popup, text='Select an interface to start').grid(row=0,column=0)
        self.combobox = ttk.Combobox(popup)
        self.combobox.bind('<Button-1>', self.interface_changed)
        self.combobox.grid(row=1, column=0)

        self.startButton = ttk.Button(popup, text="Continue")
        self.startButton.bind('<Button-1>', self.nextButton_clicked)
        self.startButton.grid(row=2, column=0)




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

    def show_error(self, ex):
        showerror(title='Error', message=str(ex))