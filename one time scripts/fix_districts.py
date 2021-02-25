import utils
import os
# The list is for manually fixing district names in "parsed_station.json" file.
# List out the names of all the districts which do not match with covid districts data.


station = utils.readfile('parsed_station.json', True)
station = list(station.values())

state_code_dict = {'andhrapradesh': 'AP', 'arunachalpradesh': 'AR', 'assam': 'AS', 'bihar': 'BR', 'chhattisgarh': 'CT', 'goa': 'GA', 'gujarat': 'GJ', 'haryana': 'HR', 'himachalpradesh': 'HP', 'jharkhand': 'JH', 'karnataka': 'KA', 'kerala': 'KL', 'madhyapradesh': 'MP', 'maharashtra': 'MH', 'manipur': 'MN', 'meghalaya': 'ML', 'mizoram': 'MZ', 'nagaland': 'NL', 'odisha': 'OR', 'punjab': 'PB', 'rajasthan': 'RJ', 'sikkim': 'SK', 'tamilnadu': 'TN', 'telangana': 'TG', 'tripura': 'TR', 'uttarakhand': 'UT', 'uttarpradesh': 'UP', 'westbengal': 'WB', 'andamannicobarislands': 'AN', 'chandigarh': 'CH', 'dnh-and-dd': 'DN', 'delhi': 'DL', 'jammukashmir': 'JK', 'ladakh': 'LA', 'lakshadweep': 'LD', 'puducherry': 'PY', 'india': 'TT'}

mem = {}
def read_all():
    files = os.listdir('./covid_data')
    files.remove('india.json')
    for name in files:
        state_data = utils.readfile('covid_data/'+ name, True)
        state_code = list(state_data.keys())[0]
        district_list = list(state_data[state_code]['districts'].keys())
        mem[name.split('.')[0]] = district_list
        

def readstate(rail_district, state_name):
    covid_district = mem[state_name]
    return rail_district in covid_district

read_all()

count=0
for data in station:
    name, rail_district, state = data
    
    isAvailable = readstate(rail_district, state)
    if not isAvailable:
        if state in ['assam', 'telangana']:
            continue
        print( name, rail_district, state)
        count+=1

print('total', count)


