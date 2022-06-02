
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
    def description(cls, result: bool) -> str:
        desc = ""
        if result:
            desc += "The password has been cracked easily, it is usually a bad indication that this application" \
            + "can get your network password. Change your password as it is very weak. Tips: Use password longer than" \
            + " 8 characters, use uncommon words, don't put keywords that can be easily deduced (Your company name," \
            + "your name, your age, etc...)\n"
        else:
            desc += "The application could not recover your password."
        return desc

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
        result.attack = cls.attack_name()

        p = sb.Popen(["stdbuf","-i0","-o0","-e0"] + cmd, stdout=sb.PIPE, text=True)

        for line in p.stdout:
            perc = line.find('%')
            key_found = line.find('KEY FOUND')

            if perc != -1:
                q.put('Current total passwords tested: ' + line[perc-6: perc+1] + "\n")

            if key_found != -1:
                q.put(line[key_found:]) 
                result.risk = 'High'
                result.desc = cls.description(True)
                q.put(result)

            elif line.find('KEY NOT FOUND') != -1:
                q.put('KEY NOT FOUND')
                result.risk = 'None'
                result.desc = cls.description(True)
                q.put(result)

        p.kill()