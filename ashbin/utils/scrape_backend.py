# -*- coding: utf-8 -*-
__author__ = 'qitian'
import datetime
import time
import os
from midstation.configs.default import DefaultConfig as Config
from midstation.button.models import Message
from midstation.user.models import User, Button
import json
from wechat_sdk import WechatBasic
from midstation.order.models import Order, create_order
import requests

requests.packages.urllib3.disable_warnings()

GATEWAY_ID = Config.GATEWAY_ID
ORGANIZATION = Config.ORGANIZATION
USERNAME = Config.LINKLAB_USERNAME
PASSWORD = Config.LINKLAB_PASSWORD
NUM_MINUTES_BACK = 1


def detect_button_events(interval=5):
    """
    get messages sent from buttons
    :param interval:
    :return:
    """
    if GATEWAY_ID == '' or ORGANIZATION == '' or USERNAME == '' or PASSWORD == '':
        print ('Please fill out your username, password, and gateway ID in the script')
        return

    try:
        while True:
            data = get_received_messages(ORGANIZATION, GATEWAY_ID, USERNAME, PASSWORD, NUM_MINUTES_BACK)
            if data:
                for d in data['events']:
                    eventUUID = d['routerMetadata']['eventUUID']
                    node_id = d['networkMessage']['nodeMetadata']['nodeId']
                    receipt_time = d['routerMetadata']['receiptTime']

                    # change to datatime object
                    receipt_time = receipt_time[:8] + receipt_time[9:15]
                    receipt_time = datetime.datetime.strptime(receipt_time, '%Y%m%d%H%M%S')

                    # 判断是否已经处理过了
                    msg = Message.query.filter_by(eventUUID=eventUUID).first()
                    if not msg:
                        message = Message(eventUUID=eventUUID, node_id=node_id, receipt_time=receipt_time)
                        message.save()

                        # 发送微信消息
                        send_wechat(node_id)
                        # 创建订单
                        create_order(node_id)
                        # 发送确认消息
                        send_command(USERNAME, PASSWORD, GATEWAY_ID, node_id, '0XFF')

            time.sleep(interval)

    except KeyboardInterrupt:
        os.exit()


# 发送微信消息
def send_wechat(node_id):
    button = Button.query.filter_by(node_id=node_id).first()
    if button:
        wechat_id = button.user.wechat_id
        template_id = button.service.wechat_template_id

    # wechat = WechatBasic(token='midstation', appid='wx6b84ff9cb6f9a54e', appsecret='4e09e5b35198bdbf35b90a65d5f76af4')
    wechat = WechatBasic(token=Config.WECHAT_TOKEN, appid=Config.WECHAT_APPID, appsecret=Config.WECHAT_APPSECRET)

    data = {}
    # res = wechat.send_template_message(user_id=wechat_id,
    #                              template_id=template_id, data=data)
    res = wechat.send_template_message(user_id='o5lpBuCdBW7HABytpcAbMy3QbBPs',
                                 template_id='grsshOaPw-0pCrkdZwjOS4Mr4AaQQVteEG-2R_RK6BY', data=data)
    if res['errcode']:
        raise Exception('Send wechat message failed')


# 发送成功消息
def send_command(username, password, target_gateway_id, target_node_id, payload_hex, needs_ack=False):
    """
    Sends a message to a node through a specified gateway
    The gateway and node ids must be strings
    Returns the command id, or None if the send was unsuccessful
    """
    command_url = 'https://ingest.link-labs.com/api/command/Gateway/' + target_gateway_id
    command_headers = {'content-type': 'application/json', 'Accept': 'application/json'}

    target_node_id_hex = '{0:x}'.format(target_node_id & int('1' * 36, 2))
    cmd_data = {'commandType': target_node_id_hex + ':' + ('Ack' if needs_ack else 'NoAck'),
                'payloadHex': payload_hex}
    auth = requests.auth.HTTPBasicAuth(username, password)
    response = requests.post(command_url, json.dumps(cmd_data), verify=False,
                             headers=command_headers, auth=auth)
    if response.status_code == requests.codes['created']:
        return json.loads(response.text)['commandId']
    else:
        raise RuntimeError(response.reason)


def validate_hex_payload(x):
    hex(int(x, 16))
    return x


def get_received_messages(organization, gateway_id, username, password, num_minutes_back):
    url = build_url(organization, gateway_id, num_minutes_back)
    auth = requests.auth.HTTPBasicAuth(username, password)
    try:
        resp = requests.get(url, verify=False, auth=auth)
    except Exception:
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


