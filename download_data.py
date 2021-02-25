import requests as rq
import utils
import datetime
import time
import shutil
import os
from threading import Thread


class Store:
    def __init__(self):
        state_data = {}
        state_code = []
        update_data = {}


def load_state_data():

    data = eval(utils.readfile('state_data.json'))
    store.state_data = data
    store.state_code = list(data.keys())



def load_update_data():
    store.update_data = eval(utils.readfile('update_data.json'))
    # should be a dict
    
    
def check_state(state = None):
    '''Check if the state needs to be update
Return a list containing name and download link for state
'''
    load_update_data()
    load_state_data()
    
    update_list = []
    # convert string to list
    if isinstance(state, str):
        state = [state]

    # if no state is mentioned change it to all states
    if not state:
        state = store.state_code

    # remove redundant states
    state = list(set(state))
    # check if the data is updated in last 24 hours

    for code in state:
        # current time -  last updated time should be greader than 86400 seconds
        # takes care of the data for which code is not available
        
        if time.time() - store.update_data.get(code, time.time()- 86401) > 86400 or not os.path.isfile('./covid_data/' + store.state_data[code]['json_name']):
            update_list.append({'code': code, **store.state_data[code]})

    return update_list


def download(state = None):
    # contain state name and ocde to be update after filtering.
    update_list  = check_state(state)

    # if list is empty return function
    if not update_list:
        return
    # modifies the list content to thread instance
    update_Thread = [Thread( target = download_file, args = (data['code'], data['json_name'])) for data in update_list]

    # download file with threads
    for thread in update_Thread:
        thread.start()

    for thread in update_Thread:
        thread.join()
        
    # update the file "update_data.json"

    new_data = {}
    for state_code in update_list:
        new_data[state_code['code']] = timestamp()
    new_data = {**store.update_data, **new_data}

    utils.writefile('./update_data.json', new_data)

    # reload all data
    load_state_data()
    load_update_data()

def timestamp():
    return int(datetime.datetime.now().timestamp())

def download_file(name, json_name):

    with sess.get(f'https://api.covid19india.org/v4/min/timeseries-{name}.min.json') as r:
        with open(f'./covid_data/{json_name}', 'w') as f:
            f.write(str(r.text))

store = Store()
sess = utils.session()

