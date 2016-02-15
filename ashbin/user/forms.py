# -*- coding: utf-8 -*-
__author__ = 'qitian'
from flask_wtf import Form
from flask import flash
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from ashbin.user.models import User
from flask_login import current_user
from ashbin.extensions import redis_store
from redis import Redis

class UserInfoForm(Form):
    username = StringField(u'用户名', validators=[DataRequired()])
    telephone = StringField(u'电话')
    mobile_phone = StringField(u'手机')
    address = StringField(u'地址')

    def save_form(self):
        current_user.username = self.username.data
        current_user.telephone = self.telephone.data
        current_user.mobile_phone = self.mobile_phone.data
        current_user.address = self.address.data

        current_user.save()

class AuthWechatForm(Form):
    auth_key = StringField(u'微信验证码', validators=[DataRequired()])
    submit = SubmitField(u'验证')

    def save_wechat_id(self):
        # 验证验证码是否存在
        redis = Redis()


        if redis_store.exists(self.auth_key.data):
            current_user.wechat_id = redis_store.get(self.auth_key.data)
            current_user.save()
        else:
            flash(u'验证码错误', 'danger')