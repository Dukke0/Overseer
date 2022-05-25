
from enum import Enum
from Model.Attacks.AbstractAttack import AbstractAttack
from Model.Target import Target
import datetime

class Report():

    def __init__(self, target):
        self.title = "Report on " + target.essid
        self.failed_attacks = 0
        self.succesful_attacks = 0
        self.attacks_results = list()
        self.target = target
    
    def report_date(self) -> str:
        e = datetime.datetime.now()
        return e.strftime("%Y-%m-%d %H:%M:%S")
    
    def write_attack_result(self, attack: AbstractAttack, success: bool, messages="") -> None:
        if success: self.succesful_attacks +=1
        else: self.failed_attacks +=1
        self.attacks_results.append({'attack': attack.attack_name(), 'success': success, 'info': messages})

    def to_pdf(self):
        pass

    def to_json(self):
        pass

    def to_txt(self) -> None:
        with open("report.txt", "w") as f:
            f.write(self.title + "\n" + "Date: " + self.report_date() +"\n")
            
            f.write("\nAccess point properties: \n" )
            f.write("\nMAC address: " + self.target.bssid)
            f.write("\nEncryption protocol: " + self.target.protocol)
            f.write("\nChannel: " + str(self.target.channel) + "\n")

            f.write("\nTotal attacks performed on the target: ")
            f.write("\nSuccesful Attacks: " + str(self.succesful_attacks))
            f.write("\nFailed Attacks: " + str(self.failed_attacks))
            f.write("\nVulnerability Percentage: " 
                    + str(round(self.succesful_attacks / len(self.attacks_results), 2) * 100) + "%\n")


            for attack in self.attacks_results:
                f.write('\nAttack type: ' + attack['attack'])
                f.write('\nInformation: ' + attack['info'])
                f.write('\nRisk: ' + str(attack['success'])+"\n")
            