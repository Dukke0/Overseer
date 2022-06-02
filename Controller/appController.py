#from View.AppView import AppView
import queue
from Controller.appException import AppException
from Model.AttackPlan import AttackPlan
from Model.Attacks.AbstractAttack import AbstractAttack, AttackResultInfo
from Model.Attacks.EvilTwin import EvilTwin
from Model.Protocols import OPEN, WEP, WPA, AbstractProtocol
from Model.Target import Target
from Model.interface import Interface
from View.AppView import AppView
from View.ScanView import ScanView
from Model.Report import Report
from View.View import AbstractView
import Model.utils as utl
import traceback
from Model.Database import Database

class AppController:

    def __init__(self, app, firstView : AbstractView):
        self.app = app
        self.interface = Interface()
        self.target = Target()
        self.attack_plan = AttackPlan(target=self.target, controller=self)
        self.db = Database('database.db')
        self.report = Report(self.target, database=self.db)
        self.view = None
        self.change_view(firstView) # Only one view

        utl.temp_folder() # Create temp folder


    def change_view(self, viewClass) -> None:
        '''
        Changes view and removes old's view
        :viewClass: View class to change to 
        :return: void
        '''
        if self.view != None:
            self.view.grid_forget()
            self.view.destroy()
        self.view = viewClass(self.app, controller=self)
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
            self.interface.scan_networks()
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
    
    def attack_target(self) -> str:
        try:
            #self.interface.sniff_target(self.target)
            if EvilTwin in self.get_plan():
                for n in EvilTwin.PROCESS_NAMES:
                    self.view.create_extra_window(name=n)

            for path in self.attack_plan.execute_plan(target=self.target, interface=self.interface):
                if type(path) == AttackResultInfo:
                    self.report.report_results_from(path)
                else:
                    yield path

            self.report.save_report()

        except StopIteration as si:
            #self.report.communicate_result(path)
            pass
        except Exception as e:
            print(e)
            yield 'error'
            #self.clean_close()
            traceback.print_exc()

    def get_scan_time(self) -> int:
        return self.interface.get_scan_time()

    def clean_close(self) -> None:
        try:
            self.interface.clean_exit()
            self.app.destroy()
        except Exception as e:
            print(e)
            self.app.destroy()

    def change_target(self, bssid: str, essid: str, protocol: str, channel:  str) -> None:

        self.target.bssid = bssid.strip()
        self.target.essid = essid.strip()
        self.target.channel = channel
        protocol = protocol.strip()

        if protocol == 'WPA' or protocol == 'WPA2' or protocol == 'WPA/WPA2' or protocol =='WPA2 WPA':
            self.target.protocol = WPA
        elif protocol == 'WEP':
            self.target.protocol = WEP
        elif protocol == 'OPN':
            self.target.protocol = OPEN

    def protocol_attacks(self, protocol: AbstractProtocol) -> list():
        if protocol != None:
            return protocol.attacks_list() # TODO manage none

    def get_plan(self):
        return self.attack_plan.attack_list

    def add_attack_to_plan(self, attack: AbstractAttack) -> None:
        self.attack_plan.add_attack(attack)
    
    def remove_attack_from_plan(self, attack: AbstractAttack) -> None:
        self.attack_plan.remove_attack(attack)

    def get_target_info(self) -> dict:
        '''
        Function that returns target's info in a dictionary form
        '''
        return vars(self.target)

    def get_target_info_as_string(self) -> str:
        try:
            dic_info = self.get_target_info()
            string_info = ""
            for key, val in enumerate(dic_info):
                string_info += str(key) + " " + str(val) + " "
            return string_info
        except:
            return 'Uknown'
    
    def create_wordlist(self, keywords):
        try:
            utl.WordListCreator.create_combinations(keywords=keywords)
        except AppException as ex:
            self.view.show_error(ex)
    
    def change_mac(self, mac=None):
        try:

            mac = mac.replace("-", ":")
            if not utl.MACChanger.validate_mac(mac):
                self.view.show_error(ex)
                return 
            #TODO return new mac address
            utl.MACChanger.change_mac(mac=mac)
                    
        except AppException as ex:
            self.view.show_error(ex)
        except Exception as ex:
            self.app.destroy()
    
    def check_report(self):
        try:
            self.report.to_txt()
            self.report.to_json()
        except AppException as ex:
            self.view.show_error(ex)
        except Exception as ex:
            self.app.destroy()
            traceback.print_exc()
    
    def get_reports(self, filter=None):
        return self.db.filter_reports(filter)

    def export_report(self, id, file_path=None, type='json'):
        try:
            self.report.export_report(id=id, file_path=file_path, type=type)
        except AppException as ex:
            self.view.show_error(ex)
        except Exception as ex:
            self.app.destroy()
            traceback.print_exc()            

