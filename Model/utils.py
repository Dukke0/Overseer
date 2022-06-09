
import pandas as pd
import os, glob
import time
from typing import Union
import itertools
import subprocess as sb

from Controller.appException import AppException

#Folder and files
folder_name = "temp"
wifi_file = folder_name + "/scan"
target_dump = folder_name + "/target_dump" 
pids_file = folder_name + "/pids"


def parse_networks_file(filename: str) -> list():
    '''
    Returns a list of networks, parsed with pandas. 
    TODO parse it without pandas
    '''
    df = pd.read_csv(filename)
    df.dropna(subset=[' ID-length'],inplace=True)
    fields = [' ESSID', 'BSSID',' channel', ' Privacy', ' Cipher', ' Authentication']
    df = df[fields].copy()
    dic = df.to_dict()

    #TODO is not efficient
    detected_networks = list()
    for i in range(len(df)):
        network = list()
        for f in fields:
            network.append(dic[f][i])
        detected_networks.append(network)
        
    return detected_networks

def set_temp(name: str) -> None:
    global folder_name
    folder_name = name

def temp_folder() -> int:
    current_path = os.getcwd()
    try:
        os.mkdir(current_path + '/temp')
        return 0
    except FileExistsError as e:
        return 1

def delete_file(file) -> None:
   for f in glob.glob(file + "*"):
      os.remove(f)

def delete_temp() -> Union[int, None]:
    current_path = os.getcwd()
    for root, dirs, files in os.walk(current_path + '/temp', topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    try:
        os.rmdir(current_path + '/temp')
    except:
        return 1

class MACChanger():

    @classmethod
    def change_mac(cls, ifce_name, ifce_monitor, mac=None):
        cmd = ['airmon-ng', 'stop', ifce_monitor]
        sb.run(cmd, sb.PIPE)

        cmd = ['ifconfig', ifce_name, 'down']
        sb.run(cmd, sb.PIPE)

        cmd = ['macchanger', ifce_name]

        if not mac: cmd.append('--random')
        else: cmd.append('--mac=' + mac)

        sb.run(cmd, sb.PIPE)

        cmd = ['ifconfig', ifce_name, 'up']
        sb.run(cmd, sb.PIPE)

        cmd = ['airmon-ng', 'start', ifce_name]
        sb.run(cmd, sb.PIPE)

    @classmethod
    def validate_mac(cls, mac, separator=":"):

        if len(mac) != (12 + 5):
            return False

        for i in range(5):
            if mac[i+2] != separator:
                return False

        return True
                    
        

class WordListCreator():
    __comb_path = "Model/files/comb_path.txt"
    __wordlist_path = "Model/files/wordlist.txt"

    @classmethod
    def parse_data(cls, keywords):
        title = keywords.title()
        nospaces = title.replace(" ", "")
        keywords_list = nospaces.split(",")
        return keywords_list

    @classmethod
    def create_combinations(cls, keywords: str):
        open(cls.__comb_path, 'w').close()
        parsed_keys = cls.parse_data(keywords=keywords)

        if len(parsed_keys) > 5:
            raise AppException('The number of words to create a wordlist has exceeded its maximum (max 5)')
        elif parsed_keys == ['']:
            raise AppException('Please enter a word between 1 and 5 words')
        print(parsed_keys, len(parsed_keys))

        for i in range(1, len(parsed_keys)+1):
            l = list(itertools.permutations(parsed_keys, i))
            together = ["".join(p) for p in l]
            without_large_values = [x for x in together if len(x) < 20]
            with open(cls.__comb_path, mode='a', encoding='utf-8') as f:
                f.write('\n'.join(without_large_values))

        cls.johnCombination()

    @classmethod
    def johnCombination(cls):
        cmd = ['john', '--rules=jumbo', '--stdout', '--wordlist='+cls.__comb_path, '-min-len=8', '-max-len=14']
        with open(cls.__wordlist_path, "w") as outfile:
            sb.run(cmd, stdout=outfile)




