# -*- coding: utf-8 -*-

from flask import Blueprint, request, redirect, flash
from flask import render_template
from jinja2 import TemplateNotFound
from flask import abort
from midstation.auth.forms import LoginForm


auth = Blueprint('button', __name__, template_folder='templates')



# @auth.route('/auth/register')
# def register():
#     try:
#         return render_template('auth/register.html')
#     except TemplateNotFound:
#         abort(404)
#
#
# @auth.route("/auth/login", methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash('Login requested for OpenID="' + form.username.data + '", remember_me=' +str(form.remember_me.data))
#         name = form.username.data
#         password = form.password.data
#         return redirect('/station/button_list.html')
#         # return redirect('/auth/register')
#     return render_template('auth/login.html',
#         title='Sign In',
#         form=form)