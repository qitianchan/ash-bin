# -*- coding: utf-8 -*-
__author__ = 'qitian'

from flask import Blueprint, request, render_template, abort, redirect, url_for
from jinja2 import TemplateNotFound
from midstation.user.models import User
from midstation.user.models import Button
from midstation.configs.default import DefaultConfig as Config
from wechat_sdk import WechatBasic

wechat = Blueprint('wechat', __name__, template_folder='templates')


@wechat.route('/send_template_massage')
def send_template_massage():
    try:
        token = Config.WECHAT_TOKEN

        args = request.args
        echostr = args['echostr']
        signature = args['signature']
        timestamp = args['timestamp']
        nonce = args['nonce']


        # 实例化 wechat
        wechat = WechatBasic(token=token)
        # 对签名进行校验
        if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            user_id = 'o5lpBuCdBW7HABytpcAbMy3QbBPs'
            template_id = 'grsshOaPw-0pCrkdZwjOS4Mr4AaQQVteEG-2R_RK6BY'
            data = {
                "first": {
                   "value": "恭喜你购买成功！",
                   "color": "#173177"
                },
                "keynote1":{
                   "value": "巧克力",
                   "color": "#173177"
                },
                "keynote2": {
                   "value": "39.8元",
                   "color": "#173177"
                },
                "keynote3": {
                   "value": "2014年9月16日",
                   "color": "#173177"
                },
                "remark":{
                   "value": "欢迎再次购买！",
                   "color": "#173177"
                }
            }
            WechatBasic.send_template_message(user_id, template_id, data)

        print 'wechat token'
        return 'Hello'
    except TemplateNotFound:
        abort(404)