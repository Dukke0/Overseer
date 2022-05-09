
from Model.Attacks.AbstractAttack import AbstractAttack
from Model.utils import target_dump
import subprocess as sb

class BruteForceAttack(AbstractAttack):

    @classmethod
    def attack_name(cls) -> str:
        return 'Brute Force'

    @classmethod
    def execute_attack(cls):
        pass

class DictionaryAttack(AbstractAttack):
    __word_list = list()

    @classmethod
    def attack_name(cls) -> str:
        return 'Dictionary attack'
    
    @classmethod
    def execute_attack(cls, target=None):
        
        '''
        Attempts to crack the captured hash containing the password with a dictionary attack using the Aircrack tool 
        '''
        cmd = ['aircrack-ng',
            '-w', cls.word_list, #TODO create/upload dictionary file
            '-b', target.bssid,
            target_dump + "-01.cap"]
        
        output = sb.run(cmd, capture_output=True, text=True, shell=True)

        if output.stdout.find('No valid WPA handshakes found'):
            return False 

        if output.stdout.find('KEY FOUND'):
            return True

        return False
