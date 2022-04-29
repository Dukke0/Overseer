
import tkinter as tk
from View.AppView import AppView
from Model.interface import Interface
from Controller.appController import AppController

class App(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title('Wifipy')
        self.geometry('600x400+50+50')

        model = Interface()

        view = AppView(self)
        view.grid(row=0, column=0, padx=100, pady=100)

        controller = AppController(model, view)

        view.set_controller(controller)



if __name__ == '__main__':
    app = App()
    app.mainloop()
