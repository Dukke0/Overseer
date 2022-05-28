
import tkinter as tk
from Controller.appController import AppController
from Model.Target import Target
from View.AppView import AppView
from View.AttackView import AttackView
from View.ScanView import ScanView
from Model.Report import Report
import sv_ttk
from Model.Attacks.DeauthAttack import DeauthAttack, TestAttack
from threading import Thread

class App(tk.Tk):

    def __init__(self):
        "sudo -E "
        super().__init__()

        self.title('Wifipy')
        #self.geometry('800x600')
        self.eval('tk::PlaceWindow . center')

        sv_ttk.set_theme("light")
        sv_ttk.set_theme("dark")
        sv_ttk.use_light_theme()
        #sv_ttk.use_dark_theme()

        AppController(self, ScanView)

        

if __name__ == '__main__':
    """
    t = Target(bssid = '00:00:00:00:00:00', essid = 'eduroam', protocol = 'WPA2', channel = 6)
    r = Report(t)
    r.write_attack_result(DeauthAttack, True, 'A')
    r.write_attack_result(TestAttack, True, 'A')
    r.write_attack_result(DeauthAttack, False, 'A')

    r.to_txt()
    r.to_json()
    """
    app = App()
    app.mainloop()
