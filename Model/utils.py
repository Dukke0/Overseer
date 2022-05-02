
import pandas as pd
import os, glob
import time

#Folder and files
folder_name = "temp"
wifi_file = folder_name + "/scan"
target_dump = folder_name + "/target_dump" 

def parse_networks_file(filename):
    '''
    Returns a list of networks, parsed with pandas. 
    TODO parse it without pandas
    '''
    df = pd.read_csv(filename)
    df.dropna(subset=[' ID-length'],inplace=True)
    df = df[[' ESSID', 'BSSID',' channel', ' Privacy', ' Cipher', ' Authentication']].copy()
    print(df)
    print(df.to_dict())
    return ['A','B','C']

def set_temp(name):
    global folder_name
    folder_name = name

def temp_folder():
    current_path = os.getcwd()
    try:
        os.mkdir(current_path + '/temp')
        return 0
    except FileExistsError as e:
        return 1

def delete_file(file):
   for f in glob.glob(file + "*"):
      os.remove(f)

def delete_temp():
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

