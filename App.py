
import tkinter as tk
from Controller.appController import AppController
from Model.Database import Database
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

        AppController(self, AppView)
 


if __name__ == '__main__':

    t = Target(bssid = '00:00:00:00:00:00', essid = 'eduroam', protocol = 'WPA2', channel = 6)
    r = Report(t, database= Database("database.db"))
    """
    r.write_attack_result(DeauthAttack, True, 'A')
    r.write_attack_result(TestAttack, True, 'A')
    r.write_attack_result(DeauthAttack, False, 'A')
    r.save_report()
    """
    app = App()
    
    app.mainloop()
    """
    db = Database("database.db")
    with db.conn:
        report = ('Report 1', 'Hoy', 'some bssid', 'some essid', 'WPA2', 'channel')
        report_id = db.create_report(report)

        attack_1 = ('Attack 1', 'easy lol', 'High', report_id)
        attack_2 = ('Attack 2', 'SO HARD', 'None', report_id)

        db.create_attack(attack_1)
        db.create_attack(attack_2)

        cur = db.conn.cursor()
        cur.execute("SELECT * FROM Report")

        rows = cur.fetchall()

        for row in rows:
            print(row)

        cur = db.conn.cursor()
        cur.execute("SELECT * FROM Attack")

        rows = cur.fetchall()

        for row in rows:
            print(row)
    """

