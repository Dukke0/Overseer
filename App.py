
import tkinter as tk
from Controller.appController import AppController
from View.AppView import AppView
from View.AttackView import AttackView
from View.ScanView import ScanView

class App(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title('Wifipy')
        self.geometry('800x600')
        self.eval('tk::PlaceWindow . center')

        AppController(self, AttackView)

if __name__ == '__main__':
    app = App()
    app.mainloop()
