
import pandas as pd
import os, glob
import time
from typing import Union

#Folder and files
folder_name = "temp"
wifi_file = folder_name + "/scan"
target_dump = folder_name + "/target_dump" 

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

