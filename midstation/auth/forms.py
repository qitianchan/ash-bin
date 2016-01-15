# -*- coding: utf-8 -*-

from datetime import datetime

from flask_wtf import Form, RecaptchaField
from wtforms import (StringField, PasswordField, BooleanField, HiddenField,
                     SubmitField)
from wtforms.validators import (DataRequired, InputRequired, Email, EqualTo,
                                regexp, ValidationError, Length)
from midstation.user.models import User

USERNAME_RE = r'^[\w.+-]+$'
is_username = regexp(USERNAME_RE,
                     message="You can only use letters, numbers or dashes.")


class LoginForm(Form):
    username = StringField(u'用户名', [Length(min=4, max=25)])
    password = PasswordField(u'密码', [Length(min=6, max=25)])
    remember_me = BooleanField(u'记住我', default=False)

    submit = SubmitField(u'登 录')

    def auth(self):
        users = User.query.filter_by(username=self.username.data).all()
        for user in users:
            if user.id == self.password.data:
                return True

        return False


class RegisterForm(Form):
    username = StringField(u"用户名", validators=[
        DataRequired(message=u"请填入用户名")])

    password = PasswordField(u'密码', validators=[
        InputRequired(),
        EqualTo('confirm_password', message=u'两次密码不一致')])

    confirm_password = PasswordField(u'确认密码')

    submit = SubmitField(u'注册')


    def save(self):

        return User.create_user(self.username.data, self.password.data)
