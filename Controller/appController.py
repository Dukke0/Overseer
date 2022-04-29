#from View.AppView import AppView
from Model.interface import Interface
from View.ScanView import ScanView

class AppController:

    def __init__(self, app):
        self.app = app
        self.interface = Interface()
        self.view = None
        self.change_view(ScanView) # Welcome page

    def change_view(self, viewClass):
        if self.view != None:
            self.view.grid_forget()
            self.view.destroy()
        self.view = viewClass(self.app)
        self.view.grid(row=0, column=0, padx=10, pady=10)
        self.view.set_controller(self)

    def get_list_interfaces(self):
        return self.interface.get_list_interfaces()

    def selected_interface(self, name):
        self.interface.init_monitor()
        self.change_view(ScanView) #Change view to next page
        
