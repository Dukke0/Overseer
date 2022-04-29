from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo

class AppView(ttk.Frame):

    def __init__(self, parent): 
        super().__init__(parent)

        self.label = ttk.Label(self, text='Welcome to Wifipy')
        self.label.grid(row=1, column=0)

        self.combobox = ttk.Combobox(self)
        self.combobox.bind('<Button-1>', self.interface_changed)
        self.combobox.grid(row=2, column=0)

        self.startButton = ttk.Button(self, text="Continue")
        self.startButton.bind('<Button-1>', self.nextButton_clicked)
        self.startButton.grid(row=3, column=0)


        self.controller = None

    def set_controller(self, controller):
        self.controller = controller
            
    #-----EVENTS-------:
    def interface_changed(self, event):
        self.combobox['values'] = self.controller.get_list_interfaces()

    def nextButton_clicked(self, event):
        if self.combobox.get() == "":
            showinfo(title='Error', message='Please select an interface')
        else:
            print(self.combobox.get())
