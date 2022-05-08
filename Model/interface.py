import subprocess as sb
from asyncio.subprocess import PIPE
import time
from Controller.appException import AppException

import Model.utils as utl

class Interface():

    def __init__(self):
        self.max_retries = 5
        self.__scan_time = 20
        self.intf = ""
        self.monitor = ""
    
    def get_scan_time(self) -> int:
        return self.__scan_time

    def scan_networks(self):
        '''
        Scans the signals around using Aircack tool.
        '''
        utl.temp_folder()

        cmd = ['sudo',
            'airodump-ng', self.monitor,
            '--wps',
            '--write', utl.wifi_file]
        
        process = sb.Popen(cmd, stdout=PIPE)
        time.sleep(self.__scan_time)
        process.terminate()
     
    def get_networks(self):
        return utl.parse_networks_file(utl.wifi_file + '-01.csv')

    def set_interface(self, name: str) -> None:
        self.intf = name

    def clean_exit(self) -> None:
        # utl.delete_temp()
        sb.run(["sudo airmon-ng stop %s" % self.monitor], shell=True)

    def init_monitor(self) -> None:
        sb.run(["sudo airmon-ng start %s" % self.intf], capture_output=True, shell=True)
        monitor_name = sb.run(["iwconfig | grep mon"], capture_output=True, text=True, shell=True)
        self.monitor= monitor_name.stdout.split(" ")[0]
        if self.monitor == "":
            raise AppException("Could not enable monitor mode, use a card that allows it")

    def get_list_interfaces(self) -> list():
        list_ifs = sb.run([r"""ip -o link | grep ether | awk '{ print $2" : "$17 }'"""],
                        capture_output=True, text=True, shell=True)
        
        list_ifs = list_ifs.stdout
        list_ifs = list_ifs.split('\n') # Split interfaces
        
        return list_ifs[:-1]