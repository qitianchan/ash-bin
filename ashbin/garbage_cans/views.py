# -*- coding: utf-8 -*-
__author__ = 'qitian'

from flask import Blueprint, redirect, request, url_for, render_template, abort, flash
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from ashbin.garbage_cans.model import GarbageCan
from flask_paginate import Pagination
from .forms import GarbageCanForm

garbage_can = Blueprint('garbage_can', __name__, template_folder='templates')

# services list
@garbage_can.route('/garbage_can_list')
@login_required
def garbage_can_list():
    try:
        search = False
        q = request.args.get('q')
        if q:
            search = True
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1

        can_count = GarbageCan.can_count()
        pagination = Pagination(page=page, per_page=15, total=can_count, css_framework='bootstrap3',
                                search=search, record_name='cans')

        can_datas = []

        cans = GarbageCan.get_garbage_cans(current_user, page, per_page=15)
        for o in cans:
            data = {}
            data['id'] = o.id
            data['bottom_height'] = o.bottom_height
            data['top_height'] = o.top_height
            data['type'] = o.type
            can_datas.append(data)

        return render_template('garbage_can/garbage_can_list.html', can_datas=can_datas, pagination=pagination)
    except TemplateNotFound:
        abort(404)


@garbage_can.route('/garbage_can_profile/<can_id>', methods=['GET', 'POST'])
@login_required
def garbage_can_profile(can_id):
    form = GarbageCanForm(request.form)
    can = GarbageCan.get(can_id)
    if can is None:
        can = GarbageCan()
    if request.method == 'POST' and form.validate_on_submit():
        form.save_form(can)
        flash(u'保存成功', category='success')
        return redirect(url_for('garbage_can.garbage_can_list'))

    return render_template('garbage_can/garbage_can_profile.html', form=form, can=can)

#
# @service.route('/service/<id>/delete', methods=['GET', 'POST'])
# @login_required
# def delete_service(id):
#     service = Service.get(id)
#     if service is None:
#         flash(u'不存在该服务', category='danger')
#         return redirect(url_for('service.service_list'))
#
#     try:
#         service.delete()
#     except IntegrityError:
#         flash(u'删除失败，存在引用到该服务的记录', 'danger')
#     except Exception:
#         flash(u'删除失败', category='danger')
#
#     return redirect(url_for('service.service_list'))
