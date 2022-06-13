import tkinter as tk
from Controller.appController import AppController
from View.AppView import AppView
import sv_ttk


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title('Wifipy')
        #self.geometry('800x600')
        self.eval('tk::PlaceWindow . center')

        sv_ttk.set_theme("light")
        sv_ttk.set_theme("dark")
        sv_ttk.use_light_theme()
        #sv_ttk.use_dark_theme()

        AppController(self, AppView)
 

if __name__ == '__main__':
    app = App()
    app.mainloop()
   