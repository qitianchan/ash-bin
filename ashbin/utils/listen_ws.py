# -*- coding: utf-8 -*-
from __future__ import division
import websocket
from ashbin.configs.default import DefaultConfig
from ashbin.devices.models import Device
import sqlite3
import json
from datetime import datetime
from ashbin.extensions import socketio
from flask_socketio import emit
from flask import current_app

url = DefaultConfig.LORIOT_URL


def ws_listening():
    print(u'开始监听消息')
    # 一直连接直到连接成功
    try:
        # simulate(r)
        ws_app = websocket.WebSocketApp(url=url, on_message=_on_message, on_open=_on_open)
        ws_app.run_forever()
    except Exception as e:
        ws_listening()


def _on_message(ws, message):
    print(message)
    cx = sqlite3.connect(DefaultConfig.DATABASE_PATH)
    t = json.loads(message)
    # if t['h'] and t['data'][0:8] == '0027a208':
    if not hasattr(t, 'h'):
        data = t['data']
        if len(data) >= 24:
            insert_data(cx, data)



def _on_open():
    print(u'连接websocket成功')


def get_info(cx, mac):
    exe = "select id, garbage_can_id from device where mac='%s'" % mac
    res = cx.execute(exe).fetchone()
    if res:
        if res[1]:
            bt_exe = "select bottom_height, top_height from garbage_can where id=%s" % res[1]
            bottom_top_height = cx.execute(bt_exe).fetchone()
            if bottom_top_height:
                t = (res[0], bottom_top_height[0], bottom_top_height[1])
                return t
        else:
            return (res[0], None, None)
    else:
        return None


def insert_data(cx, data):
    mac = data[0:8].upper()
    res = get_info(cx, mac)
    if res:
        device_id = res[0]
        bottom_height = res[1]
        top_height = res[2]
        now = datetime.now()
        if device_id:
            if bottom_height and top_height and bottom_height > top_height:
                info = parse_data(data, bottom_height, top_height)
                ins_data = (device_id, data, info[0], info[1], info[2], now)
            else:
                ins_data = (device_id, data, 0, 0, 0, now)

            cx.execute('insert into data values (?,?,?,?,?,?)', ins_data)
            cx.commit()

            # emit new message to web
            socketio.emit(mac, {'occupancy': ins_data[2], 'temperature': ins_data[3],
                                'electric_level': ins_data[4], 'create_time': now.strftime('%Y-%m-%d %H:%M:%S')},
                          namespace='/device')


def parse_data(raw_data, bottom_height, top_height):
    """
    解析出数据
    :param raw_data: 原始数据
    :param height: 探头到垃圾桶底部距离
    :return:  (占用率， 温度， 剩余电量等级)
    数据解析如下：
    例如：a8c63b90bb00180713000371为服务器收到的16进制数据，解析如下：
        第0~3字节：a8c63b90为终端的32位设备地址
        第4字节：bb为超声波探头到被测平面的测量值，单位cm.转化十进制为187cm
        第5字节：00为第二路超声波测量值，默认没有第二路超声波，为0。意义同上。
        第6字节：18为终端测量的16进制温度值。转化为十进制为24℃。
        第7字节：07为终端电池剩余电量等级，一共7个等级。
                  07表示剩余电量为95%~100%，06为85%，06为70%，04为50%，04为50%，03为35%，02为25%，01为10%，00为0%
        第8~10字节：13 00 03为本终端的时间值，以BCD码形式表示，采24小时制，分别为时、分和秒，当终端收到服务器的同步时间后，此值为实际实时时间。
        第11字节：71为前面11个字节有异或校验值
    """
    assert bottom_height > top_height, u'底部高度应该大于顶部高度'
    current_height = int(raw_data[8:10], 16)
    # 占用率， 0 - 100， 以5为最小单位
    t = ((bottom_height - current_height) / (bottom_height - top_height)) * 100
    dm = divmod(t, 5)
    occupancy = dm[0] * 5
    if occupancy < 0:
        occupancy = 0
    if occupancy > 100:
        occupancy = 100

    temperature = int(raw_data[12:14], 16)
    electric_level = int(raw_data[14:16], 16)

    return (occupancy, temperature, electric_level)


def on_msg(ws, message):
    print(message)

if __name__ == '__main__':
    ws_app = websocket.WebSocketApp(url=url, on_message=on_msg, on_open=_on_open)
    ws_app.run_forever()
