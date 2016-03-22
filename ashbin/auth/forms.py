# -*- coding: utf-8 -*-

from datetime import datetime

from flask_wtf import Form, RecaptchaField
from wtforms import (StringField, PasswordField, BooleanField, HiddenField,
                     SubmitField)
from wtforms.validators import (DataRequired, InputRequired, Email, EqualTo,
                                regexp, ValidationError, Length)
from ashbin.user.models import User

USERNAME_RE = r'^[\w.+-]+$'
is_username = regexp(USERNAME_RE,
                     message="You can only use letters, numbers or dashes.")


class LoginForm(Form):
    username = StringField(u'User Name', [Length(min=4, max=25)])
    password = PasswordField(u'Password', [Length(min=6, max=25)])
    remember_me = BooleanField(u'Remember Me', default=False)

    submit = SubmitField(u'Login')

    def auth(self):
        users = User.query.filter_by(username=self.username.data).all()
        for user in users:
            if user.id == self.password.data:
                return True

        return False


class RegisterForm(Form):
    username = StringField(u"User Name", validators=[
        DataRequired(message=u"Input your user name")])

    password = PasswordField(u'Password', validators=[
        InputRequired(),
        EqualTo('confirm_password', message=u'Re-type password do not match password')])

    confirm_password = PasswordField(u'Re-type password')
    email = StringField(u'Email')

    submit = SubmitField(u'Register')

    def save(self):
        return User.create_user(self.username.data, self.password.data)
