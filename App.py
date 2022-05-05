
import tkinter as tk
from Controller.appController import AppController

class App(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title('Wifipy')
        self.geometry('800x600')

        AppController(self)

if __name__ == '__main__':
    app = App()
    app.mainloop()
