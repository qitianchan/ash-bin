# -*- coding: utf-8 -*-

from flask import Blueprint, request, redirect, flash, url_for, jsonify
from flask import render_template
from jinja2 import TemplateNotFound
from flask import abort
from ashbin.auth.forms import LoginForm, RegisterForm
from wechat_sdk import WechatBasic
from flask_login import (login_user, current_user, login_required, logout_user)
from ashbin.user.views import user
from ashbin.user.models import User
from ashbin.extensions import csrf
from string import lower
from ashbin.configs.default import DefaultConfig
from random import randint
from ashbin.extensions import redis_store
from redis import Redis, ResponseError
from sqlalchemy.exc import IntegrityError

AUTH_KEY_EXPIRE = getattr(DefaultConfig, 'AUTH_KEY_EXPIRE', 5)            # 微信验证码过去时间（min）
auth = Blueprint('auth', __name__, template_folder='templates')

@csrf.exempt
@auth.route('/auth/register', methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            # if form.validate_username():
            try:
                user = form.save()
            except IntegrityError as e:
                return ajax_response(422, message='User name is existed')
            login_user(user)
            return redirect(url_for('devices.devices_list'))
    try:
        return render_template('auth/register.html', title='Register', form=form)
    except TemplateNotFound:
        abort(404)


def ajax_response(status_code, message='success', data=None):
    res = {}
    res['message'] = message
    res['data'] = data
    response = jsonify(res)
    response.status_code = status_code
    return response

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
                from flask import session
                s = session
                # return redirect(url_for('auth.login'))
                return url_for('devices.devices_list')
            else:
                return {'message': 'not'}

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


