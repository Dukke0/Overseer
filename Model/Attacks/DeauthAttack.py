
from Model.Attacks.AbstractAttack import AbstractAttack
from Model.utils import target_dump
import subprocess as sb

class DeauthAttack(AbstractAttack):

    @classmethod
    def attack_name(cls) -> str:
        return 'Deauthentication'

    @classmethod
    def execute_attack(cls, target=None) -> bool:
        cmd = ['tshark',
            '-r', target_dump + '-01.cap',
            '-Y', 'wlan.rsn.capabilities',
            '-T', 'fields',
            '-e', 'wlan.rsn.capabilities.mfpr'] 

        result = sb.Popen(cmd, stdout=sb.PIPE, universal_newlines=True)

        for stdout_line in iter(result.stdout.readline, ""):
            yield stdout_line 

        result.stdout.close()
        return_code = result.wait()

        if return_code:
            raise sb.CalledProcessError(return_code, cmd)

        """if result.stdout.find('1') == -1:
            return False
        else: 
            return True"""


class TestAttack(AbstractAttack):

    @classmethod
    def attack_name(cls) -> str:
        return 'test'

    @classmethod
    def execute_attack(cls, target=None) -> bool:
        cmd = ["locate", "a"]
        popen = sb.Popen(cmd, stdout=sb.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            raise StopIteration(True)
            yield stdout_line 
        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            raise sb.CalledProcessError(return_code, cmd)
