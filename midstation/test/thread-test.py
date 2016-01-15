# -*- coding: utf-8 -*-
__author__ = 'qitian'
import time
import datetime
from threading import Thread
import random

def thread_1():
    while True:
        print 'thread_1'
        time.sleep(random.randint(1, 5))

def thread_2():
    while True:
        print 'thread_2'
        time.sleep(random.randint(1, 5))

def daemon_thread():
    while True:
        f = open('daemon.txt', 'a+')

        f.write(time.strftime('%H:%M:%S'))
        f.write('\r\n')
        time.sleep(1)
t = Thread(target=daemon_thread)
t.setDaemon(True)
t.start()

if __name__ == '__main__':
    # t1 = Thread(target=thread_1)
    # t2 = Thread(target=thread_2)
    # print 'start thread 1...'
    # t1.start()
    # print 'thread 1 started'
    # print 'start thread 2...'
    # t2.start()
    # print 'thread 2 started'

    # t = Thread(target=daemon_thread)
    # t.setDaemon(True)
    # t.start()
    # while True:
    #     print time.strftime('%H:%M:%S')
    #     time.sleep(1)
    receipt_time = "20150820T012605.617"
    receipt_time = receipt_time[:8] + receipt_time[9:15]
    print receipt_time
    receipt_time = datetime.datetime.strptime(receipt_time, '%Y%m%d%H%M%S')
    print receipt_time.__class__