# -*- coding: utf-8 -*-
__author__ = 'qitian'
from flask import Blueprint, redirect, request, url_for, render_template, abort, flash
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from sqlalchemy.exc import IntegrityError
from ashbin.devices.models import Device
from flask_paginate import Pagination
from .forms import DeviceProfileForm
from .models import get_garbage_can_choice
from ashbin.gdata.models import Data
from sqlalchemy import desc
from ..extensions import socketio
from datetime import datetime
from datetime import timedelta
from flask_socketio import emit
from threading import Thread
devices = Blueprint('devices', __name__, template_folder='templates')
from flask import jsonify

@devices.route('/devices_list')
@login_required
def devices_list():
    try:

        search = False
        q = request.args.get('q')
        if q:
            search = True
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1

        devices_count = Device.devices_count()
        pagination = Pagination(page=page, per_page=15, total=devices_count, css_framework='bootstrap3',
                                search=search, record_name='devices')

        devices_datas = []

        devices = Device.get_devices(current_user, page, per_page=15)
        for o in devices:
            data = {}
            data['device_id'] = o.id
            data['mac'] = o.mac
            data['eui'] = o.eui
            data['garbage_can'] = o.garbage_can
            d = o.datas.order_by(desc(Data.create_time)).first()
            if d:
                data['occupancy'] = d.occupancy
                data['temperature'] = d.temperature
                data['electric_level'] = d.electric_level
            else:
                data['occupancy'] = 0
                data['temperature'] = 0
                data['electric_level'] = 0
            devices_datas.append(data)

        return render_template('devices/devices_list.html', devices_datas=devices_datas, pagination=pagination)
    except TemplateNotFound:
        abort(404)



@devices.route('/device_profile/<device_id>', methods=['GET', 'POST'])
@login_required
def device_profile(device_id):

    # 如果 devices_id == '0',则是新增客户
    if device_id == '0':
        device = Device()
    else:
        device = Device.query.filter_by(id=device_id).first()

    if device is None:
        device = Device()
    can_id = 1
    if getattr(device, 'garbage_can_obj'):
        can_id = device.garbage_can_obj.id
    form = DeviceProfileForm(request.form, garbage_can=can_id)
    if current_user:
            form.garbage_can.choices = get_garbage_can_choice()

    if request.method == 'POST' and form.validate_on_submit():
        form.save_form(device)
        flash(u'保存成功', category='success')
        return redirect(url_for('devices.devices_list'))

    return render_template('devices/device_profile.html', form=form, device=device)


@devices.route('/device/<id>/data', methods=['GET', 'POST'])
@login_required
def device_profile_data(id):
    search = False
    q = request.args.get('q')
    if q:
        search = True
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1
    else:
        page = 1
    device = Device.get(id)
    if device:
        # datas = device.datas.order_by(desc(cls.create_time)).paginate(page, per_page, True).items
        datas = Data.get_gdatas(current_user, device)
        count = len(datas)
        pagination = Pagination(page=page, per_page=15, total=count, css_framework='bootstrap3',
                                search=search, record_name='devices')

        return render_template('devices/device_data.html', datas=datas, device=device, pagination=pagination)
    else:
        abort(404)

@devices.route('/device/<id>/data_one_month', methods=['GET', 'POST'])
@login_required
def device_ajax_data(id):
    one_month_ago = datetime.now() - timedelta(days=30)
    datas = Data.get_datas_in_date(id, one_month_ago)
    # datas = device.datas.order_by(desc('create_time')).limit(200).all()
    res = []
    if datas:
        for d in datas:
            data = dict()
            data['occupancy'] = d.occupancy
            data['temperature'] = d.temperature
            data['electric_level'] = d.electric_level
            data['create_time'] = d.create_time.strftime('%m-%d %H:%M')
            res.append(data)

    return jsonify({'data': res})
