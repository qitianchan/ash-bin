# -*- coding: utf-8 -*-
__author__ = 'qitian'
from threading import Thread
from random import randint
import time
from datetime import datetime

from random import Random



def create_salt():
    salt = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    len_chars = len(chars) - 1
    random = Random()
    for i in xrange(32):
        # 每次从chars中随机取一位
        salt += chars[random.randint(0, len_chars)]
    return salt



if __name__ == '__main__':
    print create_salt()