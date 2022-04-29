import subprocess as sb
from asyncio.subprocess import PIPE
import time

class Interface():

    def __init__(self):

        self.monitor = ""
        self.max_retries = 5
        self.scan_time = 20

    def get_list_interfaces(self):
        list_ifs = sb.run([r"""ip -o link | grep ether | awk '{ print $2" : "$17 }'"""],
                        capture_output=True, text=True, shell=True)
        
        list_ifs = list_ifs.stdout
        list_ifs = list_ifs.split('\n') # Split interfaces
        
        return list_ifs[:-1]