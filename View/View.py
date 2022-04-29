from abc import ABC, abstractmethod
from tkinter import ttk

class AbstractView(ABC, ttk.Frame):

    @abstractmethod
    def show_error(self, ex):
        pass

    def set_controller(self, controller):
        self.controller = controller