# -*- coding: utf-8 -*-

from datetime import datetime

from flask_wtf import Form, RecaptchaField
from wtforms import (StringField, SelectField, SubmitField)
from wtforms.validators import DataRequired
from midstation.user.models import User, Service, Customer, Button
from midstation.utils.tools import get_service_choice
from flask_login import current_user


class ButtonForm(Form):

    node_id = StringField(u'node_id', validators=[DataRequired()])
    service = SelectField(u'服务')
    customer = SelectField(u'客户')

    def save_form(self, button):
        button.node_id = self.node_id.data
        service_id = int(self.service.data)
        if service_id > 0:
            button.service_id = service_id

        customer_id = int(self.customer.data)
        if customer_id > 0:
            button.customer_id = customer_id

        button.user_id = current_user.id

        button.save()
