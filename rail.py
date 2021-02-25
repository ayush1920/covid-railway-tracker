import utils
import sys

def getstation(train_no):
    sess = utils.session()
    train_id = sess.get(f'https://api.railbeeps.com/api/searchTrains/api-key/web-cfc8cf88fa0ac3b6fd8f9570608c6911?trainno={train_no}').json()[0]['id']
    stations = sess.get(f'https://api.railbeeps.com/api/fetchAvailability/api-key/web-cfc8cf88fa0ac3b6fd8f9570608c6911/trainno/{train_id}/').json()['train']['stations']
    return [code['source_code'].upper() for code in stations]
