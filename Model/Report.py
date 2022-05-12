
from enum import Enum
from Model.Attacks.AbstractAttack import AbstractAttack
from Model.Target import Target
import datetime

class Report():

    def __init__(self):
        self.title = "Report on 'wifi target name'"
        self.n_attacks = 10
        self.attacks_results = list()
        #self.target = target
    
    def report_date(self) -> str:
        e = datetime.datetime.now()
        return e.strftime("%Y-%m-%d %H:%M:%S")
    
    def write_attack_result(self, attack: AbstractAttack, success: bool, messages="") -> None:
        self.attack_result.append({'attack': attack.attack_name(), 'success': success, 'info': messages})

    def to_pdf(self):
        pass

    def to_json(self):
        pass

    def to_txt(self) -> None:
        f = open("report.txt", "a") #returns error if file exists, TODO unhandled error
        f.write(self.title + "\n" + "Date: " + self.report_date() +"\n")
        for attack in self.attacks_results:
            f.write('Attack type: ', attack['attack'], ' Information: ', attack['info'], ' Risk: ', attack['success'])
        f.close()
        