# -*- coding: utf-8 -*-

from flask import Blueprint, request, redirect, flash, url_for
from flask import render_template
from jinja2 import TemplateNotFound
from flask import abort
from midstation.auth.forms import LoginForm, RegisterForm
from wechat_sdk import WechatBasic
from flask_login import (login_user, current_user, login_required, logout_user)
from midstation.user.views import user
from midstation.user.models import User
from midstation.extensions import csrf
from string import lower
from midstation.configs.default import DefaultConfig
from random import randint
from midstation.extensions import redis_store
from redis import Redis, ResponseError


AUTH_KEY_EXPIRE = getattr(DefaultConfig, 'AUTH_KEY_EXPIRE', 5)            # 微信验证码过去时间（min）
auth = Blueprint('auth', __name__, template_folder='templates')

# @csrf.exempt
# @auth.route('/', methods=['GET', 'POST'])
# def wechat_token():
#     print '------------------------------------'
#     args = request.args
#     print args
#     if request.method == 'GET':
#         if hasattr(args, 'echostr'):
#             token = 'midstation'
#             echostr = args['echostr']
#
#             signature = args['signature']
#             timestamp = args['timestamp']
#             nonce = args['nonce']
#
#
#             # 实例化 wechat
#             wechat = WechatBasic(token=token)
#             # 对签名进行校验
#             if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
#                 print 'wechat check_signature'
#                 return echostr
#
#         return redirect(url_for('auth.login'))
#
#     # 微信消息监听
#     if request.method == 'POST':
#         print args
#         print '--------------------- wechat ----------------------'
#         token = 'midstation'
#
#         signature = args['signature']
#         timestamp = args['timestamp']
#         nonce = args['nonce']
#
#         # 实例化 wechat
#         wechat = WechatBasic(token=token, appid='wx6b84ff9cb6f9a54e', appsecret='4e09e5b35198bdbf35b90a65d5f76af4')
#         if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
#             # 对 XML 数据进行解析 (必要, 否则不可执行 response_text, response_image 等操作)
#             print request.data
#             wechat.parse_data(request.data)
#             # 获得解析结果, message 为 WechatMessage 对象 (wechat_sdk.messages中定义)
#             print 'check signature'
#             message = wechat.get_message()
#             response = None
#             if message.type == 'text':
#
#                 if lower(message.content) == '/a':
#                     key = auth_key()
#                     response = wechat.response_text(unicode(key))
#                     # 存入内容，openid, 对应的验证码
#                     save_auth_key(message.source, key, AUTH_KEY_EXPIRE)
#
#                     print '得到的验证码为: {0}'.format(redis_store.get(message.source))
#                 else:
#                     response = wechat.response_text(u'如果要绑定微信，请输入/a获取验证码，验证码将会在%s秒内失效'
#                                                     % AUTH_KEY_EXPIRE)
#             elif message.type == 'image':
#                 response = wechat.response_text(u'图片')
#             else:
#                 response = wechat.response_text(u'未知')
#
#             return response
#
#     return 'auth token fail'


@auth.route('/auth/register', methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            # if form.validate_username():
            user = form.save()
            login_user(user)
            flash("Thanks for registering. %s" % current_user.username, "success")
            return redirect(url_for('devices.devices_list'))
    try:
        return render_template('auth/register.html', title='Register', form=form)
    except TemplateNotFound:
        abort(404)

@csrf.exempt
@auth.route('/', methods=['GET', 'POST'])
@auth.route("/auth/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user, authenticated = User.authenticate(form.username.data,
                                                form.password.data)

            if user and authenticated:
                login_user(user, remember=form.remember_me.data)
                flash('Logged successfully %s' % current_user.username, 'success')
                return redirect(url_for('devices.devices_list'))

            flash("Wrong Username or Password.", "danger")
            print 'Wrong Username'
            # return redirect('/auth/register')
    return render_template('auth/login.html', title='Sign In', form=form)


@auth.route('/auth/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


def auth_key(length=6):
    """
    获取随机验证码
    :param length: 验证码长度
    :return: 0-9长度为length（默认6）的0-9的字符串 例如：'0324'
    """
    while(True):
        s = ''
        for i in range(length):
            s += str(randint(0, 9))
        if not redis_store.exists(s):
            break
    return s


def save_auth_key(openid, key, expire):
    """
    保存验证码，设置验证码生存时效
    :param openid: 用户微信openid
    :param key:  验证码
    :param expire: 生存周期 (秒)
    :return:
    """
    try:
        print openid, key, expire
        redis_store.set(key, openid)
        redis_store.expire(key, expire)
    except ResponseError:
        flash('redis连接失败', 'danger')


if __name__ == '__main__':
    redis = Redis(host='183.230.40.230', port=6379, db=0)
    redis.set('name', '0nndk')
    redis.expire('name', 20)
    print redis.get('name')


