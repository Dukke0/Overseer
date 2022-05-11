
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
        
        result = sb.Popen(cmd, stdout=sb.PIPE, universal_newlines=True)
        
        for stdout_line in iter(result.stdout.readline, ""):
            """
            if stdout_line.find('No valid WPA handshake found'):
                raise StopIteration(True)
            elif stdout_line.find('KEY FOUND'):
                raise StopIteration(True)
            """
            raise StopIteration(True)
            yield stdout_line 

        result.stdout.close()
        return_code = result.wait()

        if return_code:
            raise sb.CalledProcessError(return_code, cmd)

        """"
        if return_code:
            raise sb.CalledProcessError(return_code, cmd)

        if output.stdout.find('No valid WPA handshakes found'):
            return False 

        if output.stdout.find('KEY FOUND'):
            return True

        return False
"""