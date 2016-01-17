# -*- coding: utf-8 -*-
__author__ = 'qitian'
from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, DecimalField, IntegerField
from wtforms.validators import DataRequired
from flask_login import current_user


class GarbageCanForm(Form):
    type = StringField(u'垃圾桶类型', validators=[DataRequired()])
    bottom_height = IntegerField(u'距离底部高度（cm）', validators=[DataRequired()])
    top_height = IntegerField(u'距离顶部高度(cm)', validators=[DataRequired()])

    def save_form(self, garbage_can):
        garbage_can.user_id = current_user.id
        garbage_can.type = self.type.data
        garbage_can.bottom_height = int(self.bottom_height.data)
        garbage_can.top_height = int(self.top_height.data)

        garbage_can.save()

