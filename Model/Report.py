
from enum import Enum
from Model.Attacks.AbstractAttack import AbstractAttack, AttackResultInfo
from Model.Target import Target
#from fpdf import FPDF
import json
import datetime
import os.path

class Report():

    def __init__(self, target, filename="Report"):
        
        self.filename = filename
        self.failed_attacks = 0
        self.succesful_attacks = 0
        self.attacks_results = list()
        self.target = target
    
    def report_date(self) -> str:
        e = datetime.datetime.now()
        return e.strftime("%Y-%m-%d %H:%M:%S")
    
    def write_attack_result(self, attack: AbstractAttack, success: bool, messages="") -> None:
        if success: self.succesful_attacks += 1
        else: self.failed_attacks += 1
        self.attacks_results.append({'attack': attack.attack_name(), 'success': success, 'info': messages})

    def report_results_from(self, results: AttackResultInfo):
        print('hello there')
        success = False
        if results.risk != 'Not vulnerable':
            success = True
        self.write_attack_result(attack=results.attack, success=success, messages=results.desc)

    def report_info(self):
        dic = {
            'Title': "self.title",
            'Date': self.report_date(),
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
    
    def get_name_number(self, ext="txt") -> str:
        file_exists = os.path.exists(self.filename + "." + ext)
        new_name = self.filename + "." + ext
        i = 0
        while file_exists:
            i += 1
            new_name = self.filename + "-" + str(i) + "." + ext
            file_exists = os.path.exists(new_name + "." + ext)

        return new_name

    def to_json(self) -> None:
        with open(self.get_name_number("json"), 'w') as file:
            json.dump(self.report_info(), file, indent=4)

    def to_txt(self) -> None:
        with open(self.get_name_number("txt"), "w") as f:
            f.write("self.title" + "\n" + "Date: " + self.report_date() +"\n")
            
            f.write("\nAccess point properties: \n" )
            f.write("\nMAC address: " + self.target.bssid)
            f.write("\nEncryption protocol: " + str(self.target.protocol))
            f.write("\nChannel: " + str(self.target.channel) + "\n")

            f.write("\nTotal attacks performed on the target: " + str(len(self.attacks_results)))
            f.write("\nSuccesful Attacks: " + str(self.succesful_attacks))
            f.write("\nFailed Attacks: " + str(self.failed_attacks))
            f.write("\nVulnerability Percentage: " 
                    + str(round(self.succesful_attacks / len(self.attacks_results), 2) * 100) + "%\n")


            for attack in self.attacks_results:
                f.write('\nAttack type: ' + attack['attack'])
                f.write('\nInformation: ' + attack['info'])
                f.write('\nRisk: ' + str(attack['success'])+"\n")
            