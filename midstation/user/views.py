# -*- coding: utf-8 -*-
__author__ = 'qitian'

from flask import Blueprint, request, render_template, abort, redirect, url_for, flash
from jinja2 import TemplateNotFound
from midstation.user.models import User
from flask_login import login_required, current_user
from midstation.user.forms import UserInfoForm, AuthWechatForm
from midstation.extensions import db
from sqlalchemy.exc import IntegrityError

user = Blueprint('user', __name__, template_folder='templates')


@user.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    form = UserInfoForm(request.form)
    auth_form = AuthWechatForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.save_form()
            flash(u'保存成功', category='success')

        if auth_form.validate_on_submit():
            auth_form.save_wechat_id()
            flash(u'验证成功', category='success')

    return render_template('user/user_profile.html',  form=form,auth_form=auth_form)

