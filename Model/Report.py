
from enum import Enum
import threading
from typing import Union

from pyrsistent import b
from Model.Attacks.AbstractAttack import AbstractAttack, AttackResultInfo
from Model.Target import Target
#from fpdf import FPDF
import json
import datetime
import os.path
from Model.Database import Database
import datetime

class Report():

    def __init__(self, target, database: Database, filename="Report"):
        
        self.filename = filename
        self.failed_attacks = 0
        self.succesful_attacks = 0
        self.attacks_results = list()
        self.target = target
        self.db = database

    def save_report(self):
        with self.db.conn:
            report = ('Report', datetime.datetime.now().strftime("%x"), self.target.bssid, self.target.essid,
            str(self.target.protocol), self.target.channel)
            report_id = self.db.create_report(report)
            
            for r in self.attacks_results:
                attack = (r['attack'], r['info'], 'High', report_id)
                self.db.create_attack(attack)

    def reset_data(self):
        '''
        Function that resets the report's data.
        '''
        self.succesful_attacks = 0
        self.failed_attacks = 0
        self.attacks_results = list()

    def export_report(self, id, file_path=None, type='json'):
        if id != None:
            with self.db.conn:
                self.reset_data()
                c = self.db.conn.cursor()

                c.execute("SELECT * FROM REPORT WHERE id=="+str(id))
                report = c.fetchall()[0]
                date, bssid, essid, protocol, channel = report[2], report[3], report[4], report[5], report[6]
                t = Target(bssid=bssid, essid=essid, protocol=protocol, channel=channel)
                self.target = t
                c.execute("SELECT * FROM Attack WHERE report_id=="+str(id))
                for at in c: 
                    #TODO SUCCESS
                    self.write_attack_result(attack=at[1], messages=at[2], success=True)

        if type == 'json':
            self.to_json(file_path)
        elif type == 'txt':
            self.to_txt(file_path)
    
    def report_date(self) -> str:
        e = datetime.datetime.now()
        return e.strftime("%Y-%m-%d %H:%M:%S")
    
    def write_attack_result(self, attack: Union[AbstractAttack, str], success: bool, messages="") -> None:
        if success: self.succesful_attacks += 1
        else: self.failed_attacks += 1

        if type(attack) == str:
                self.attacks_results.append({'attack': attack, 'success': success, 'info': messages})
        else:
            self.attacks_results.append({'attack': attack.attack_name(), 'success': success, 'info': messages})

    def report_results_from(self, results: AttackResultInfo):
        success = False
        if results.risk != 'None': #TODO fix sucess to risk
            success = True
        self.write_attack_result(attack=results.attack, success=success, messages=results.desc)

    def get_name_number(self, ext="txt") -> str:
        file_exists = os.path.exists(self.filename + "." + ext)
        new_name = self.filename + "." + ext
        i = 0
        while file_exists:
            i += 1
            new_name = self.filename + "-" + str(i) + "." + ext
            file_exists = os.path.exists(new_name + "." + ext)

        return new_name

    def to_json(self, path=None) -> None:
        if not path:
            path = self.get_name_number("json")

        with open(path, 'w') as file:
            json.dump(self.report_info(), file, indent=4)
        
    def to_txt(self, path=None) -> None:
        if not path:
            path = self.get_name_number("txt")

        with open(path, "w") as f:
            f.write(self.report_info(format='txt'))

    def report_info(self, format='json'):
        if format == 'json':
            return self.__info_as_dict()
        else:
            return self.__info_as_txt()

    def __info_as_txt(self):
        print(self.attacks_results)
        s = "self.title" + "\n" + "Date: " + self.report_date() +"\n" \
        + "\nAccess point properties: \n" \
        + "\nMAC address: " + self.target.bssid \
        + "\nEncryption protocol: " + str(self.target.protocol) \
        + "\nChannel: " + str(self.target.channel) + "\n" \
        + "\nTotal attacks performed on the target: " + str(len(self.attacks_results)) \
        + "\nSuccesful Attacks: " + str(self.succesful_attacks) \
        + "\nFailed Attacks: " + str(self.failed_attacks) \
        + "\nVulnerability Percentage: " + str(round(self.succesful_attacks / len(self.attacks_results), 2) * 100) + "%\n" 

        for attack in self.attacks_results:
            s +='\nAttack type: ' + attack['attack'] \
            + '\nInformation: ' + attack['info'] \
            + '\nRisk: ' + str(attack['success'])+"\n"

        return s

    def __info_as_dict(self):
        print(self.attacks_results)
        dic = {
            'Title': "self.title", # TODO fix 
            'Date': self.report_date(), #TODO fix report date not taking from db,
            'Target': 
                {
                'ESSID': self.target.essid,
                'MAC': self.target.bssid, 
                'Protocol': str(self.target.protocol),
                'Channel': self.target.channel
                },
            'Results':
                {
                    'Attacks': len(self.attacks_results),
                    'Succesful': self.succesful_attacks,
                    'Failed': self.failed_attacks,
                    'Percentage': round(self.succesful_attacks / len(self.attacks_results), 2)
                },
            'Attacks': {}
        }

        for atk in self.attacks_results:
            dic['Attacks'][atk['attack']] = {'Information': atk['info'],
                                            'Risk': atk['success']}
        return dic
