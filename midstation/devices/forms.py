# -*- coding: utf-8 -*-
__author__ = 'qitian'
from flask_wtf import Form
from wtforms.fields import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from flask_login import current_user
from midstation.user.models import Customer
from midstation.devices.models import Device
from midstation.garbage_cans.model import GarbageCan

class DeviceProfileForm(Form):
    mac = StringField(u'硬件地址', validators=[DataRequired()])
    eui = StringField(u'EUI', validators=[DataRequired()])
    garbage_can = SelectField(u'垃圾桶类型')

    def save_form(self, device):
        if isinstance(device, Device):
            device.user_id = current_user.id
            device.mac = self.mac.data.upper()
            device.eui = self.eui.data
            garbage_can_id = int(self.garbage_can.data)
            if garbage_can_id > 0:
                device.garbage_can_id = garbage_can_id
            garbage_can = GarbageCan.get(garbage_can_id)
            if garbage_can:
                device.garbage_can = garbage_can.type

            device.save()
        else:
            raise ValueError()
