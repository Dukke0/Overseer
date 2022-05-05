
from Model.AbstractAttack import AbstractAttack
from Model.utils import target_dump

class DeauthAttack(AbstractAttack):

    def __init__(self):
        super().__init__()

    def execute_attack():
        cmd = ['tshark',
            '-r', target_dump + '-01.cap',
            '-Y', 'wlan.rsn.capabilities',
            '-T', 'fields',
            '-e', 'wlan.rsn.capabilities.mfpr'] 

        result = run_command(cmd, shell=False)

        if result.stdout.find('1') == -1:
            return False
        else: 
            return True
