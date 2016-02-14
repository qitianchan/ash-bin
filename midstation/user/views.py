# -*- coding: utf-8 -*-
__author__ = 'qitian'

from flask import Blueprint, request, render_template, abort, redirect, url_for, flash
from jinja2 import TemplateNotFound
from midstation.user.models import User
from midstation.user.models import Button
from flask_login import login_required, current_user
from midstation.user.forms import UserInfoForm, AuthWechatForm
from midstation.button.forms import ButtonForm
from midstation.user.models import Service, Customer
from midstation.utils.tools import get_service_choice, get_customer_choice
from midstation.extensions import db
from sqlalchemy.exc import IntegrityError

user = Blueprint('user', __name__, template_folder='templates')



#按钮编辑
@user.route('/button/<node_id>', methods=['GET', 'POST'])
@login_required
def button_profile(node_id):
    if node_id == '0':
        button = Button()
    else:
        button = Button.query.filter_by(node_id=node_id).first()

    if not button:
        redirect(url_for('user.button_list'))
        flash(u'不存在该按钮', category='error')
    try:
        form = ButtonForm(request.form, service=getattr(button, 'service_id', None), customer=getattr(button, 'customer_id',None))
        if current_user:
            form.service.choices = get_service_choice()
            form.customer.choices = get_customer_choice()

            if request.method == 'POST' and form.validate_on_submit():
                if node_id == '0':
                    exit_button = Button.query.filter(db.and_(Button.user_id==current_user.id, Button.node_id==form.node_id.data)).first()
                    if exit_button:
                        flash(u'node_id 已经存在', 'warning')
                        return redirect(url_for('user.button_profile', node_id=node_id))

                form.save_form(button)
                return redirect(url_for('user.button_list'))

        return render_template('user/button_profile.html', button=button, form=form)
    except TemplateNotFound:
        abort(404)


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


@user.route('/button/<node_id>/delete', methods=['POST'])
@login_required
def delete_button(node_id):
    button = Button.query.filter_by(node_id=node_id).first()
    if button is None:
        flash(u'不存在改按钮', category='danger')

    try:
        button.delete()
    except IntegrityError:
        flash(u'删除失败，存在引用到该按键的记录', 'danger')
    except Exception:
        flash(u'删除失败', category='danger')

    return redirect(url_for('user.button_list'))


def get_buttons(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return user.all_buttons(page=1)

