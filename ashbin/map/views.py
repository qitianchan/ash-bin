# -*- coding: utf-8 -*-
__author__ = 'qitian'
from flask import Blueprint, redirect, request, url_for, render_template, abort, flash
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from sqlalchemy.exc import IntegrityError
from ashbin.devices.models import Device
from flask_paginate import Pagination
from ashbin.gdata.models import Data
from sqlalchemy import desc
from ..extensions import socketio
from datetime import datetime
from datetime import timedelta
from flask_socketio import emit
from threading import Thread
from flask import jsonify
map = Blueprint('map', __name__, template_folder='templates')


@map.route('/devices_on_map')
@login_required
def devices_on_map():
    try:
        return render_template('map/devices_on_map.html')
    except TemplateNotFound:
        abort(404)


@map.route('/devices_lnglat')
@login_required
def devices_lnglat():
    data = []
    devices = current_user.devices.all()
    for device in devices:
        d = {}
        d['device_id'] = device.id
        d['lng'] = device.longitude
        d['lat'] = device.latitude
        device_data = device.datas.order_by(desc('create_time')).first()
        if device_data:
            d['occupancy'] = device.datas.order_by(desc('create_time')).first().occupancy
        else:
            d['occupancy'] = 0
        data.append(d)
    return jsonify({'data': data})


@map.route('/device_data')
@login_required
def device_data():
    res = []
    device_id = request.args['device_id']
    device = Device.get(device_id)
    if device:
        datas = device.datas.order_by(desc('create_time')).limit(200).all()
        datas = reversed(datas)
        for d in datas:
            data = dict()
            data['occupancy'] = d.occupancy
            data['temperature'] = d.temperature
            data['electric_level'] = d.electric_level
            data['create_time'] = d.create_time.strftime('%m-%d %H:%M')
            res.append(data)
    return jsonify({'data': res})