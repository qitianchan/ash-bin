# -*- coding: utf-8 -*-
__author__ = 'qitian'
from flask import Blueprint, redirect, request, url_for, render_template, abort, flash
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from ashbin.devices.models import Device
from sqlalchemy import desc
from flask import jsonify
theme = Blueprint('theme', __name__, static_folder='static')


@theme.route('/theme')
@login_required
def index():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)

@theme.route('/login')
def login():
    return render_template('login.html')
