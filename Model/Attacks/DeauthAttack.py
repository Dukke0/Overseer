
from Model.Attacks.AbstractAttack import AbstractAttack
from Model.utils import target_dump
import subprocess as sb

class DeauthAttack(AbstractAttack):

    @classmethod
    def attack_name(cls) -> str:
        return 'Deauthentication'

    @classmethod
    def execute_attack(cls) -> bool:
        cmd = ['tshark',
            '-r', target_dump + '-01.cap',
            '-Y', 'wlan.rsn.capabilities',
            '-T', 'fields',
            '-e', 'wlan.rsn.capabilities.mfpr'] 

        result = sb.run(cmd, capture_output=True, text=True, shell=False)

        if result.stdout.find('1') == -1:
            return False
        else: 
            return True
