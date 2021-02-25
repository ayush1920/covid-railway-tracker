import os
import requests as rq

def readfile(filename, _eval = False):
    # _eval enables eval function after rading file.
    
    if not os.path.isfile(filename):
        print("Warning!! File doesn't exist. Creating new file with fillename : ", filename)
        writefile(filename, "{}")
        
    with open(filename, encoding = 'utf-8') as f:
        data = f.read()
    if _eval:
        data = eval(data)
    return data


def writefile(filename, data):
    with open(filename, 'w+', encoding = 'utf-8') as f:
        f.write(str(data))


def session():
    sess = rq.session()
    sess.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.5'}
    return sess


def validate_folders(folder_list):
    if isinstance(folder_list, str):
        folder_list = [folder_list]

    for path in folder_list:
        if not os.path.isdir(path):
            os.makedirs(path)
    
