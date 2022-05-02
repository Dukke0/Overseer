
import tkinter as tk
from View.MultiColumn import MultiColumnListbox
from Controller.appController import AppController

class App(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title('Wifipy')
        self.geometry('600x400')

        AppController(self)

if __name__ == '__main__':
    app = App()
    app.mainloop()
