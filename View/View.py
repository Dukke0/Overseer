from abc import ABC, abstractmethod
from tkinter import ttk

class View(ABC, ttk.Frame):

    @abstractmethod
    def show_error(self):
        #raise NotImplementedError
        pass