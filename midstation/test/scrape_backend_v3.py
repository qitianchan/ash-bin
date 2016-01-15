# -*- coding: utf-8 -*-
'''
日期：20150908
功能：打印所有基站最新的一条消息。可以通过修改gateway_mac来增加基站。
特点：利用map()实现并发。
'''
import requests
import json
import datetime
import sys
from functools import partial
import time
import pprint

from string import atoi

gateway_mac = ["000db93db79c", "000db93db700", "000db93db804", "000db93db7c0", "000db93db6f8", "000db93db784"]
gateway_id = ["a2d790e1-1670-1217-0000-" + mac for mac in gateway_mac]

ORGANIZATION = "niot"
USERNAME = "niot.user"
PASSWORD = "Ni0t!0715"


def main():
    requests.packages.urllib3.disable_warnings()

    while True:
        i = 0
        try:
            data = get_received_messages(ORGANIZATION, gateway_id, USERNAME, PASSWORD, 20*60)
            # print(list(enumerate(data)))
            # print(data)
            print_message(data)
            time.sleep(5)
        except KeyboardInterrupt:
            sys.exit()


def print_message(data):

    gw_data = []
    for event in data:
        try:
            d = {"rssi": event["events"][0]["networkMessage"]["signalMetadata"]["rssi"],
                 "node": event["events"][0]["networkMessage"]["nodeMetadata"]["nodeId"],
                 "time": event["events"][0]['networkMessage']['routerMetadata']['receiptTime'],
                 "payload_hex": event["events"][0]["networkMessage"]["payloadHex"],
                }
            # change time zone
            hour = int(d['time'][9:11])
            hour += 8
            if hour > 24:
                hour -= 24
            d['time'] = d['time'][:9] + '{:0>2d}'.format(hour) + d['time'][11:]
        except IndexError:
            d = {}
        gw_data.append(d)
    pprint.pprint(list(enumerate(gw_data, start=1)))
    print('='*40)


def get_received_messages(organization, gateway_id, username, password, num_minutes_back):
    urls = build_urls(organization, gateway_id, num_minutes_back)
    auth = requests.auth.HTTPBasicAuth(username, password)
    data = []

    req_get = partial(requests.get, verify=False, auth=auth)
    resp = map(req_get, urls)

    for i in resp:
        if i.status_code == requests.codes['ok']:
            data.append(json.loads(i.content.decode()))

    return data


def build_urls(organization, gateway_id, num_minutes_back):
    url_base = 'https://dataaccess.link-labs.com/data/dataFlow/' + organization + '/gateway/'
    curr_time = get_current_time()
    return [(url_base + ident + '/events/timeRange?refTime=' +\
        curr_time + '&minsBack=' + str(num_minutes_back)) for ident in gateway_id]


def get_current_time():
    return datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%S.%f')[:-3]

if __name__ == "__main__":
    main()
