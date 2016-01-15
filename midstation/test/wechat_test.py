# -*- coding: utf-8 -*-
__author__ = 'qitian'
import json
from wechat_sdk import WechatBasic

wechat = WechatBasic(token='midstation', appid='wx6b84ff9cb6f9a54e', appsecret='4e09e5b35198bdbf35b90a65d5f76af4')

data = {}
res = wechat.send_template_message(user_id='o5lpBuCdBW7HABytpcAbMy3QbBPs',
                             template_id='grsshOaPw-0pCrkdZwjOS4Mr4AaQQVteEG-2R_RK6BY', data=data)

print res
