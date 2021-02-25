import utils
import re
import string

sess = utils.session()

final_list = []

for letter in list(string.ascii_uppercase):
    num = 1
    while(True):
        data = sess.get(f'https://www.railyatri.in/stations?name={letter}&page={num}').text
        data = re.findall('<td>(.*?)<\\/td>', data)
        if not data:
            break
        final_list.extend([[data[i], re.findall('>(.*?)<\\/a>', data[i+1])[0] , data[i+2], data[i+3]] for i in range(0, len(data), 5)])
        print(letter, num)
        num+=1
    
utils.writefile('station_data.json', final_list)

