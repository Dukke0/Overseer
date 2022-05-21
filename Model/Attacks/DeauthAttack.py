
from Model.Attacks.AbstractAttack import AbstractAttack
from Model.utils import target_dump
import subprocess as sb

class DeauthAttack(AbstractAttack):

    @classmethod
    def attack_name(cls) -> str:
        return 'Deauthentication'

    @classmethod
    def execute_attack(cls, target=None) -> bool:
        cmd = ['sudo',
            'tshark',
            '-r', target_dump + '-01.cap',
            '-Y', 'wlan.rsn.capabilities',
            '-T', 'fields',
            '-e', 'wlan.rsn.capabilities.mfpr'] 

        result = sb.Popen(cmd, stdout=sb.PIPE, universal_newlines=True)
        if result.stdout.read().find('1') == -1:
            yield 'Vulnerability found: Network is vulnerable to deauthentication attacks.'
        else:
            yield 'Network is not vulnerable to deauthentication attacks.'

        result.stdout.close()
        return_code = result.wait()

        if return_code:
            raise sb.CalledProcessError(return_code, cmd)

class TestAttack(AbstractAttack):

    @classmethod
    def attack_name(cls) -> str:
        return 'test'

    @classmethod
    def execute_attack(cls, target=None) -> bool:

        '''
        Attempts to crack the captured hash containing the password with a dictionary attack using the Aircrack tool 
        '''
        target_dump = 'Model/files/handshake'
        cmd = ['sudo',
            'aircrack-ng',
            '-w', "Model/files/pass_dict",
            '-b', 'E8:DE:27:B0:14:C9',
            target_dump + "-01.cap"]
        
        result = sb.Popen(cmd, stdout=sb.PIPE, universal_newlines=True)
        #for l in iter(result.stdout.readline, ""):
            #yield l
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