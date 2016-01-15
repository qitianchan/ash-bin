# -*- coding: utf-8 -*-
__author__ = 'qitian'
from flask_wtf import Form
from wtforms.fields import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from flask_login import current_user
from midstation.user.models import Customer
from midstation.devices.models import Device


class DeviceProfileForm(Form):
    mac = StringField(u'硬件地址', validators=[DataRequired])
    eui = StringField(u'EUI', validators=[DataRequired])
    garbage_can = SelectField(u'垃圾桶类型', validators=[DataRequired])

    def save_form(self, device):
        if isinstance(device, Device):
            device.user_id = current_user.id
            device.name = self.name.data
            device.mobile_phone = self.mobile_phone.data
            device.telephone = self.telephone.data
            device.addr = self.address.data

            device.save()
        else:
            raise ValueError()
