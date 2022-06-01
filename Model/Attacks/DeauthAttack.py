
from Model.Attacks.AbstractAttack import AbstractAttack, AttackResultInfo
from Model.utils import target_dump
import subprocess as sb

class DeauthAttack(AbstractAttack):

    @classmethod
    def attack_name(cls) -> str:
        return 'Deauthentication'

    @classmethod
    def description(cls, result: bool) -> str:
        desc = ""
        if result:
            desc += "Vulnerability found: Network is vulnerable to deauthentication attacks.\n"
            + "Even thought the network is vulnerable, deauthentication attacks are not a threat on their own.\n"
            + "However, they can enable other type of attacks like Evil twin or stealing your networks password hash.\n"
        else:
            desc += "Network is not vulnerable to deauthentication attacks."
        return desc

    @classmethod
    def execute_attack(cls, q, kwargs) -> bool:
        cmd = ['tshark',
            '-r', target_dump + '-01.cap',
            '-Y', 'wlan.rsn.capabilities',
            '-T', 'fields',
            '-e', 'wlan.rsn.capabilities.mfpr'] 

        result = AttackResultInfo()
        result.attack = cls.attack_name

        process = sb.Popen(cmd, stdout=sb.PIPE, universal_newlines=True)
        if process.stdout.read().find('1') == -1:
            result.risk = 'Low'
            result.desc = cls.description(True)
        else:
            result.risk = 'None'
            result.desc = cls.description(False)

        q.put(result)


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
        