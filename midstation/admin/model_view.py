# -*- coding: utf-8 -*-
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from midstation.app import app
from midstation.user.models import User
from midstation.extensions import db

class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')


