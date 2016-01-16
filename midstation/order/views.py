# -*- coding: utf-8 -*-
__author__ = 'qitian'

from flask import Blueprint, request, render_template, abort, redirect, url_for, flash
from jinja2 import TemplateNotFound
from midstation.user.models import User
from midstation.user.models import Button
from flask_login import login_required, current_user
from midstation.order.models import Order
from flask_login import current_user
from flask_paginate import Pagination

order = Blueprint('order', __name__, template_folder='templates')


@order.route('/order_list')
@login_required
def order_list():
    try:
        search = False
        q = request.args.get('q')
        if q:
            search = True
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1

        order_count = Order.orders_count()
        pagination = Pagination(page=page, per_page=15, total=order_count, css_framework='bootstrap3',
                                search=search, record_name='orders')

        order_datas = []

        orders = Order.get_orders(current_user, page, per_page=15)
        for o in orders:
            data = {}
            data['order_id'] = o.id
            data['service'] = o.service_name
            data['price'] = o.price
            data['customer'] = o.customer_name
            data['address'] = o.customer_addr
            data['create_time'] = o.create_time.strftime('%Y-%m-%d %H:%M:%S')
            data['phone'] = o.phone
            data['status'] = o.status
            order_datas.append(data)

        return render_template('order/order_list.html', order_datas=order_datas, pagination=pagination)
    except TemplateNotFound:
        abort(404)

