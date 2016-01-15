"""
This script connects to the backend, reads some info on the packets we've
received, and plots the results

Be sure to provide your username, password, and gateway ID
"""
import requests
import json
import datetime
from pprint import pprint
import time
import os

GATEWAY_ID = 'a2d790e1-1670-1217-0000-000db93db700'
ORGANIZATION = 'niot'
USERNAME = 'niot.user'
PASSWORD = 'Ni0t!0715'

def main():
    requests.packages.urllib3.disable_warnings()
    # f = open("lora.log", 'w')
    if GATEWAY_ID == '' or ORGANIZATION == '' or USERNAME == '' or PASSWORD == '':
        print ('Please fill out your username, password, and gateway ID in the script')
        return

    try:
        while True:
            data = get_received_messages(ORGANIZATION, GATEWAY_ID, USERNAME, PASSWORD, 60)
            print_messages(data)
            time.sleep(5)
    except KeyboardInterrupt:
        os.exit()

def print_messages(data):
    # Keep the information that we want to print
    try:
        pretty_data = [
            {
                'rssi': data['events'][0]['networkMessage']['signalMetadata']['rssi'],
                'node': data['events'][0]['networkMessage']['nodeMetadata']['nodeId'],
                'time': data['events'][0]['ingestMetadata']['ingestTime'],
                'payload_hex': data['events'][0]['networkMessage']['payloadHex'],
            } 
        ]
        hour = int(pretty_data[0]['time'][9:11])
        hour += 8
        if hour > 24:
            hour -= 24
        pretty_data[0]['time'] = pretty_data[0]['time'][:9] + '{:0>2d}'.format(hour) + pretty_data[0]['time'][11:]
    except IndexError:
        pretty_data = []

    pprint(pretty_data)
    '''
    f.write(time.asctime())
    f.write(str(pretty_data))
    f.write("\n\r")
    '''
def get_received_messages(organization, gateway_id, username, password, num_minutes_back):
    url = build_url(organization, gateway_id, num_minutes_back)
    auth = requests.auth.HTTPBasicAuth(username, password)
    resp = requests.get(url, verify=False, auth=auth)

    if resp.status_code != requests.codes['ok']:
        raise RuntimeError(resp.reason)

    return json.loads(resp.content.decode())

def build_url(organization, gateway_id, num_minutes_back):
    url_base = 'https://dataaccess.link-labs.com/data/dataFlow/' + organization + '/gateway/'
    curr_time = get_current_time()
    return url_base + gateway_id + '/events/timeRange?refTime=' +\
        curr_time + '&minsBack=' + str(num_minutes_back)

def get_current_time():
    return datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%S.%f')[:-3]


if __name__ == '__main__':
    main()
