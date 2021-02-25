import rail
import utils
import time
import download_data
import os
import time
from tabulate import tabulate

station_list = utils.readfile('parsed_station.json', _eval = True)
update_data = utils.readfile('update_data.json', _eval = True)
state_code_dict = {'andhrapradesh': 'AP', 'arunachalpradesh': 'AR', 'assam': 'AS', 'bihar': 'BR', 'chhattisgarh': 'CT', 'goa': 'GA', 'gujarat': 'GJ', 'haryana': 'HR', 'himachalpradesh': 'HP', 'jharkhand': 'JH', 'karnataka': 'KA', 'kerala': 'KL', 'madhyapradesh': 'MP', 'maharashtra': 'MH', 'manipur': 'MN', 'meghalaya': 'ML', 'mizoram': 'MZ', 'nagaland': 'NL', 'odisha': 'OR', 'punjab': 'PB', 'rajasthan': 'RJ', 'sikkim': 'SK', 'tamilnadu': 'TN', 'telangana': 'TG', 'tripura': 'TR', 'uttarakhand': 'UT', 'uttarpradesh': 'UP', 'westbengal': 'WB', 'andamannicobarislands': 'AN', 'chandigarh': 'CH', 'dnh-and-dd': 'DN', 'delhi': 'DL', 'jammukashmir': 'JK', 'ladakh': 'LA', 'lakshadweep': 'LD', 'puducherry': 'PY', 'india': 'TT'}


class Storage:
    def __init__(self):
        self.covid = {}
        self.update_data = {}

    def update_values(self, covid_data = None, update_data = None):
        if covid_data:
            self.covid = covid_data
        if update_data:
            self.update_data = update_data
        

def load_covid_data():
    files = os.listdir('./covid_data')
    try:
        files.remove('india.json')
    except:
        pass

    temp_dict = {}
    for name in files:
        state_data = utils.readfile('covid_data/'+ name, True)
        temp_dict[name.split('.')[0]] = state_data

    storage.update_values(temp_dict, utils.readfile('./update_data.json', True))
    
    

def parse_covid_data(dis_30):
    delta_values= [0,0,0,0,0]
    covid_keys = ['confirmed','deceased', 'recovered', 'tested', 'vaccinated']
    
    for data in dis_30:
        delta =  data.get('delta', None)
        if delta:
            for index, val in enumerate(covid_keys):
                delta_values[index] += delta.get(val, 0)
                
    delta = ["{:.2f}".format(val/30) for  val in delta_values]
    total = dis_30[-1]['total']
    total = [str(total.get(key, 0)) for key in covid_keys] 
    return delta, total
            
    
    
def route_data(train_no = None):
    if not train_no:
        train_no = input('Enter Trian number:')
    if not train_no.isnumeric:
        print('Train number not numeric')
        
    station_code = rail.getstation(train_no)


    route_data = []
    for code in station_code:
        station_data = station_list.get(code, None)
        if not station_data:
            print(f"Station {code} doesn't exists in database.")
            continue
        route_data.append(station_data)

    ## get list of states whose data is not downloaded or in not updated within a day

    no_data_state_code = []
    route_state_code = []

    for data in route_data:
        state = data[-1]
        state_code = state_code_dict[data[-1]]
        route_state_code.append(state_code)
        if not storage.covid.get(state, False) or storage.update_data.get( state_code, time.time() - 86401)> 86400:
            no_data_state_code.append(state_code)
            

    ## download and update list
    if no_data_state_code:
        download_data.download(no_data_state_code)
        load_covid_data()

    route_covid_data = []
    for station, state_code in zip(route_data, route_state_code):
        name, district, state = station
        covid = utils.readfile('covid_data/'+state +'.json', True)[state_code]
        district_data = covid['districts'].get(district, {}).get('dates', None)
        if not district_data:
            route_covid_data.append((False, name, district))
            continue
    
        date_list = sorted(list(district_data.keys()))

        # contains the data of last 30 days
        dis_30 = [district_data[date] for date in date_list[len(date_list)-30:]]
        delta, total  = parse_covid_data(dis_30)
        route_covid_data.append((True, name, district, state, delta, total))

    return route_covid_data
        
        
storage = Storage()
load_covid_data()
