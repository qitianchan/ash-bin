# -*- coding: utf-8 -*-
__author__ = 'qitian'

from flask import Blueprint, redirect, request, url_for, render_template, abort, flash, jsonify
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from ashbin.garbage_cans.model import GarbageCan
from flask_paginate import Pagination
from .forms import GarbageCanForm
from ashbin.extensions import csrf

garbage_can = Blueprint('garbage_can', __name__, template_folder='templates')

# services list
@garbage_can.route('/garbage_can_list', methods=['GET', 'POST'])
# @login_required
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
        try:
            if int(form.bottom_height.data) <= int(form.top_height.data):
                flash(u'垃圾桶底部高度应该大于顶部高度', category='error')
                return render_template('garbage_can/garbage_can_profile.html', form=form, can=can)
            form.save_form(can)
        except TypeError as e:
            flash(u'数据类型错误', category='error')
            return render_template('garbage_can/garbage_can_profile.html', form=form, can=can)
        flash(u'保存成功', category='success')
        return redirect(url_for('garbage_can.garbage_can_list'))

    return render_template('garbage_can/garbage_can_profile.html', form=form, can=can)


@garbage_can.route('/edit', methods=['POST', 'UPDATE'])
@login_required
@csrf.exempt
def edit_can():
    data = request.form
    try:
        try:
            bottom = int(data['bottom'])
            top = int(data['top'])
        except ValueError as e:
            res = {'message': 'Value error'}
            res.status_code = 422
            return res

        type = data['type']

        if request.method == 'UPDATE':
            can_id = int(data['can_id'])
            can = GarbageCan.get(can_id)
        elif request.method == 'POST':
            can = GarbageCan()

        can.type = type
        can.bottom_height = bottom
        can.top_height = top
        try:
            can.save()
            return jsonify({'message': 'Update success', 'can_id': can.id})
        except Exception as e:
            res = jsonify({'message': 'Update failed'})
            res.status_code = 422
            return res
    except Exception as e:
        res = jsonify({'message': e.message})
        res.status_code = 422
        return res


@garbage_can.route('/delete', methods=['DELETE'])
@login_required
@csrf.exempt
def delete_can():
    try:
        can_id = int(request.form['can_id'])
        can = GarbageCan.get(can_id)
        if can:
            can.delete()
        return jsonify({'message': 'delete success'})
    except ValueError as e:
        res = jsonify({'message': 'field can_id value error'})
        res.status_code = 422

    return jsonify({'message': 'success'})

