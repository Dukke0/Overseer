
import pandas as pd 

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

