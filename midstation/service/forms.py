# -*- coding: utf-8 -*-
__author__ = 'qitian'
from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, DecimalField, IntegerField
from wtforms.validators import DataRequired
from midstation.user.models import Service
from flask_login import current_user


class ServiceProfileForm(Form):
    name = StringField(u'服务名', validators=[DataRequired()])
    count = StringField(u'数量', validators=[DataRequired()])
    price = DecimalField(u'价格', validators=[DataRequired()])
    unit = StringField(u'单位')

    def save_form(self, service):
        service.user_id = current_user.id
        service.name = self.name.data
        service.count = self.count.data
        service.price = self.price.data
        service.unit = self.unit.data

        service.save()

