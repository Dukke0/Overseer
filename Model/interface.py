import subprocess as sb
from asyncio.subprocess import PIPE
import time 

class Interface():

    def __init__(self):

        self.monitor = ""
        self.max_retries = 5
        self.scan_time = 20

    def get_list_interfaces():
        list_ifs = sb.run([r"""ip -o link | grep ether | awk '{ print $2" : "$17 }'"""],
                        capture_output=True, text=True, shell=True)
        return list_ifs