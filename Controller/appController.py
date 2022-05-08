#from View.AppView import AppView
from Controller.appException import AppException
from Model.Protocols import WPA, AbstractProtocol
from Model.Target import Target
from Model.interface import Interface
from View.AppView import AppView
from View.ScanView import ScanView
import Model.utils as utl
import logging

class AppController:

    def __init__(self, app, firstView):
        self.app = app
        self.interface = Interface()
        self.target = Target()
        self.view = None
        self.change_view(firstView) # Only one view

        #utl.temp_folder() # Create temp folder


    def change_view(self, viewClass) -> None:
        '''
        Changes view and removes old's view
        :viewClass: View class to change to 
        :return: void
        '''
        if self.view != None:
            self.view.grid_forget()
            self.view.destroy()
        self.view = viewClass(self.app)
        self.view.grid(row=0, column=0, padx=10, pady=10)
        self.view.set_controller(self)

    def get_list_interfaces(self) -> list():
        '''
        :return: A list of detected interfaces
        '''
        return self.interface.get_list_interfaces()

    def get_networks(self) -> list:
        '''
        Scans and returns a list of networks
        :return: list of networks
        '''

        try:
            # self.interface.scan_networks()
            return self.interface.get_networks()
        except AppException as ex:
            self.view.show_error(ex)
        except Exception as e:
            print(e)
            self.clean_close
    
    def selected_interface(self, name: str) -> None:
        '''
        Initializes net card to monitor and changes to next view
        :return void
        '''
        try:
            self.interface.set_interface(name)
            self.interface.init_monitor()
            self.change_view(ScanView) #Change view to next page
        except AppException as ex:
            self.view.show_error(ex)
        except Exception as e:
            print(e)
            self.clean_close()
    
    def attack_target(self):
        # TODO
        raise NotImplementedError
            
        
    def get_scan_time(self):
        return self.interface.get_scan_time()

    def clean_close(self):
        try:
            self.interface.clean_exit()
            self.app.destroy()
        except Exception as e:
            print(e)
            self.app.destroy()

    def change_target(self, bssid: str, essid: str, protocol: str) -> None:
        self.target.bssid = bssid
        self.target.essid = essid
        protocol = protocol.strip()
        if protocol == 'WPA' or protocol == 'WPA2' or protocol == 'WPA/WPA2':
            self.target.protocol = WPA

    def protocol_attacks(self, protocol: AbstractProtocol) -> list():
        return protocol.attacks_list()

    def get_target_info(self):
        return vars(self.target)