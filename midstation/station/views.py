# -*- coding: utf-8 -*-
__author__ = 'qitian'

from flask import Blueprint, request, render_template, abort
from jinja2 import TemplateNotFound

station = Blueprint('station', __name__, template_folder='templates')


# @station.route('/button_list')
# def member_list():
#     try:
#         #get buttons
#         buttons =
#         return render_template("station/button_list.html")
#     except TemplateNotFound:
#         abort(404)
