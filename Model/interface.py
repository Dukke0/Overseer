import subprocess as sb
from asyncio.subprocess import PIPE
import time
from Controller.appException import AppException
from Model.Target import Target
from Model.utils import target_dump
import Model.utils as utl

class Interface():

    def __init__(self):
        self.max_retries = 5
        self.__scan_time = 20
        self.intf = ""
        self.monitor = ""
    
    def get_scan_time(self) -> int:
        return self.__scan_time

    def scan_networks(self) -> None:
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
        process.kill()
     
    def get_networks(self) -> list():
        return utl.parse_networks_file(utl.wifi_file + '-01.csv')

    def set_interface(self, name: str) -> None:
        self.intf = name

    def clean_exit(self) -> None:
        utl.delete_temp()
        #sb.run(["sudo airmon-ng stop %s" % self.monitor], shell=True)

    def init_monitor(self) -> None:
        self.monitor = 'wlan0mon'
        """
        sb.run(["sudo airmon-ng start %s" % self.intf], capture_output=True, shell=True)
        monitor_name = sb.run(["iwconfig | grep mon"], capture_output=True, text=True, shell=True)
        self.monitor= monitor_name.stdout.split(" ")[0]
        if self.monitor == "":
            raise AppException("Could not enable monitor mode, use a card that allows it")
        """

    def get_list_interfaces(self) -> list():
        list_ifs = sb.run([r"""ip -o link | grep ether | awk '{ print $2" : "$17 }'"""],
                        capture_output=True, text=True, shell=True)
        
        list_ifs = list_ifs.stdout
        list_ifs = list_ifs.split('\n') # Split interfaces
        
        return list_ifs[:-1]
    
    def sniff_target(self, target_wifi):
        '''
        Sniff packets related to our target network
        '''
        
        cmd = ['sudo',
            'airodump-ng',
            '-c', str(target_wifi.channel),
            '--bssid', target_wifi.bssid,
            '--write', target_dump,
            '--wps',
            self.monitor]

        process = sb.Popen(cmd, stdout=PIPE)
        time.sleep(self.__scan_time)
        process.terminate()
        
        #out, err = process.communicate()
        #target_wifi.wps = self.get_wps(out, target_wifi)
    
        
    def get_wps(self, data, target):
        data = data.decode("utf-8")
        start_idx = data.find(target.bssid)
        if start_idx == -1:
            return -1
        end_idx = data.find("\n", start_idx)
        line = data[start_idx:end_idx]
        wps = " ".join(line.split()).split()[11] # 11 is where wps value is placed inside the lane
        #TODO null at 11
        print('WPS value: ' + wps)
        """
        if wps == "1.0" or wps == "2.0":
            return WPS_STATE.UNLOCKED
        else:
            return WPS_STATE.LOCKED
        """
