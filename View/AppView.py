from tkinter import ttk
import tkinter as tk

class AppView(ttk.Frame):

    def __init__(self, parent): 
        super().__init__(parent)

        self.label = ttk.Label(self, text='Welcome to Wifipy')
        self.label.grid(row=1, column=0)


        self.controller = None

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller

    def show_list_interfaces(self):
        self.controller.get_list_interfaces
        