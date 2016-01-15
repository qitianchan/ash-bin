# -*- coding: utf-8 -*-
__author__ = 'qitian'
from flask import Blueprint, redirect, request, url_for, render_template, abort, flash
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from midstation.user.models import User, Service, Customer
from midstation.customer.forms import CustomerProfileForm
from sqlalchemy.exc import IntegrityError


devices = Blueprint('devices', __name__, template_folder='templates')

# services list
@devices.route('/devices_list')
@login_required
def devices_list():
    try:
        devices = current_user.devices
        return render_template('devices/devices_list.html', devices=devices)
    except TemplateNotFound:
        abort(404)


# 修改或添加顾客信息
@devices.route('/devices_profile/<devices_id>', methods=['GET', 'POST'])
@login_required
def devices_profile(devices_id):

    # 如果 devices_id == '0',则是新增客户
    if devices_id == '0':
        cust = devices()
    else:
        cust = devices.query.filter_by(id=devices_id).first()

    if cust is None:
        cust = devices()

    form = devicesProfileForm(request.form, address=cust.addr or '')

    if request.method == 'POST' and form.validate_on_submit():
        form.save_form(cust)
        flash(u'保存成功', category='success')
        return redirect(url_for('devices.devices_list'))

    devicess = current_user.devicess

    return render_template('devices/devices_profile.html', form=form, devices=cust)


@devices.route('/devices/<id>/delete', methods=['GET', 'POST'])
@login_required
def delete_devices(id):
    devices = devices.get(id)
    if devices is None:
        flash(u'不存在该客人', category='danger')
        return redirect(url_for('devices.devices_list'))

    try:
        devices.delete()
    except IntegrityError:
        flash(u'删除失败，存在引用到该服务的记录', 'danger')
    except Exception:
        flash(u'删除失败', category='danger')

    return redirect(url_for('devices.devices_list'))