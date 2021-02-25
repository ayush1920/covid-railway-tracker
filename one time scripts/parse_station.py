import utils
import os


station = utils.readfile('station_data.json', _eval = True)

parsed_data = {}

state_list = [i.replace('.json', '') for i in os.listdir('covid_data')]

count = 0
count1 = 0
for data in station:
    state_name = data[-1].replace(' ', '').lower()
    if state_name not in state_list:
        count1+=1
        continue

    parsed_data[data[0]] = [data[1], data[2], state_name]
    count+=1
    
print(count, count1)
print(len(parsed_data))
utils.writefile('parsed_station.json', parsed_data)
