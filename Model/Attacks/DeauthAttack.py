
from Model.Attacks.AbstractAttack import AbstractAttack
from Model.utils import target_dump
import subprocess as sb

class DeauthAttack(AbstractAttack):

    @classmethod
    def attack_name(cls) -> str:
        return 'Deauthentication'

    @classmethod
    def execute_attack(cls, q, kwargs) -> bool:
        cmd = ['tshark',
            '-r', target_dump + '-01.cap',
            '-Y', 'wlan.rsn.capabilities',
            '-T', 'fields',
            '-e', 'wlan.rsn.capabilities.mfpr'] 

        result = sb.Popen(cmd, stdout=sb.PIPE, universal_newlines=True)
        if result.stdout.read().find('1') == -1:
            yield 'Vulnerability found: Network is vulnerable to deauthentication attacks.'
        else:
            yield 'Network is not vulnerable to deauthentication attacks.'

class TestAttack(AbstractAttack):

    @classmethod
    def attack_name(cls) -> str:
        return 'test'

    @classmethod
    def execute_attack(cls, q, kwargs) -> bool:
        cmd = ['airodump-ng', 'wlan0mon']
        p = sb.Popen(["stdbuf","-i0","-o0","-e0"]  + cmd, stdout=sb.PIPE, text = True)
        for line in p.stdout:
            q.put(line)
        p.kill()
        