import subprocess as sb
from asyncio.subprocess import PIPE
import time
from Model.utils import wifi_file, parse_networks_file

class Interface():

    def __init__(self):
        self.max_retries = 5
        self.scan_time = 20
        self.intf = ""
        self.monitor = ""

    def scan_networks(self):
        '''
        Scans the signals around using Aircack tool.
        '''
        cmd = ['sudo',
            'airodump-ng', self.monitor,
            '--wps',
            '--write', wifi_file]
        
        process = sb.Popen(cmd, stdout=PIPE)
        time.sleep(self.scan_time)
        process.terminate()
     
    def get_networks(self):
        return parse_networks_file(wifi_file)

    def set_interface(self, name):
        self.intf = name
    
    def init_monitor(self):
        sb.run(["sudo airmon-ng start %s" % self.intf], capture_output=True, shell=True)
        monitor_name = sb.run(["iwconfig | grep mon"], capture_output=True, text=True, shell=True)
        self.monitor= monitor_name.stdout.split(" ")[0]
        if self.monitor == "":
            raise Exception("Could not enable monitor mode, use a card that allows monitor mode")

    def get_list_interfaces(self):
        list_ifs = sb.run([r"""ip -o link | grep ether | awk '{ print $2" : "$17 }'"""],
                        capture_output=True, text=True, shell=True)
        
        list_ifs = list_ifs.stdout
        list_ifs = list_ifs.split('\n') # Split interfaces
        
        return list_ifs[:-1]