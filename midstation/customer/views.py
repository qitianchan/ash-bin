# -*- coding: utf-8 -*-
__author__ = 'qitian'
from flask import Blueprint, redirect, request, url_for, render_template, abort, flash
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from midstation.user.models import User, Service, Customer
from midstation.customer.forms import CustomerProfileForm
from sqlalchemy.exc import IntegrityError


customer = Blueprint('customer', __name__, template_folder='templates')

# services list
@customer.route('/customer_list')
@login_required
def customer_list():
    try:
        customers = current_user.customers
        return render_template('customer/customer_list.html', customers=customers)
    except TemplateNotFound:
        abort(404)


# 修改或添加顾客信息
@customer.route('/customer_profile/<customer_id>', methods=['GET', 'POST'])
@login_required
def customer_profile(customer_id):

    # 如果 customer_id == '0',则是新增客户
    if customer_id == '0':
        cust = Customer()
    else:
        cust = Customer.query.filter_by(id=customer_id).first()

    if cust is None:
        cust = customer()

    form = CustomerProfileForm(request.form, address=cust.addr or '')

    if request.method == 'POST' and form.validate_on_submit():
        form.save_form(cust)
        flash(u'保存成功', category='success')
        return redirect(url_for('customer.customer_list'))

    customers = current_user.customers

    return render_template('customer/customer_profile.html', form=form, customer=cust)


@customer.route('/customer/<id>/delete', methods=['GET', 'POST'])
@login_required
def delete_customer(id):
    customer = Customer.get(id)
    if customer is None:
        flash(u'不存在该客人', category='danger')
        return redirect(url_for('customer.customer_list'))

    try:
        customer.delete()
    except IntegrityError:
        flash(u'删除失败，存在引用到该服务的记录', 'danger')
    except Exception:
        flash(u'删除失败', category='danger')

    return redirect(url_for('customer.customer_list'))