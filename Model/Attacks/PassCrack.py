
from Model.Attacks.AbstractAttack import AbstractAttack, AttackResultInfo
from Model.utils import target_dump
import subprocess as sb
import os.path

class BruteForceAttack(AbstractAttack):

    @classmethod
    def attack_name(cls) -> str:
        return 'Brute Force'

    @classmethod
    def execute_attack(cls):
        pass

class DictionaryAttack(AbstractAttack):
    __path_dict = 'Model/files/pass_dict' #TODO make default wordlist

    @classmethod
    def attack_name(cls) -> str:
        return 'Dictionary attack'
    
    @classmethod
    def execute_attack(cls, q, kwargs):
        '''
        Attempts to crack the captured hash containing the password with a dictionary attack using the Aircrack tool 
        '''
        wordlist = cls.__path_dict
        if os.path.exists('Model/files/wordlist.txt'):
            wordlist = 'Model/files/wordlist.txt'

        kwargs['target'].bssid = 'E8:DE:27:B0:14:C9' #TODO
        target_dump = 'Model/files/handshake' #TODO
        cmd = ['aircrack-ng',
            '-w', wordlist, #TODO create/upload dictionary file
            '-b', kwargs['target'].bssid,
            target_dump + "-01.cap"]

        result = AttackResultInfo()
        p = sb.Popen(["stdbuf","-i0","-o0","-e0"] + cmd, stdout=sb.PIPE, text=True)

        for line in p.stdout:
            perc = line.find('%')
            key_found = line.find('KEY FOUND')

            if perc != -1:
                q.put('Current total passwords tested: ' + line[perc-6: perc+1] + "\n")

            if key_found != -1:
                q.put(line[key_found:]) 
                result.risk = 'High'
                result.desc = 'It was easy LOL'
                result.attack = cls
                q.put(result)

            elif line.find('KEY NOT FOUND') != -1:
                q.put('KEY NOT FOUND')

        p.kill()