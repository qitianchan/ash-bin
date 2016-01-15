# -*- coding: utf-8 -*-
__author__ = 'qitian'
from flask_wtf import Form
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import DataRequired
from flask_login import current_user
from midstation.user.models import Customer


class CustomerProfileForm(Form):
    name = StringField(u'名字', validators=[DataRequired()])
    telephone = StringField(u'电话')
    mobile_phone = StringField(u'手机', validators=[DataRequired()])
    address = TextAreaField(u'地址', validators=[DataRequired()])

    def save_form(self, customer):
        if isinstance(customer, Customer):
            customer.user_id = current_user.id
            customer.name = self.name.data
            customer.mobile_phone = self.mobile_phone.data
            customer.telephone = self.telephone.data
            customer.addr = self.address.data

            customer.save()
        else:
            raise ValueError()
