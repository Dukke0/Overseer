from abc import ABC, abstractmethod
from tkinter import ttk

class AbstractView(ABC, ttk.Frame):

    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

    @abstractmethod
    def show_error(self, ex):
        pass
    
    def on_closing(self) -> None:
        self.controller.clean_close()

    def set_controller(self, controller) -> None:
        self.controller = controller
