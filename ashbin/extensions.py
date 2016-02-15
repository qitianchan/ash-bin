# -*- coding: utf-8 -*-
__author__ = 'qitian'


"""
    ashbin.extensions
    ~~~~~~~~~~~~~~~~~~~~

    The extensions that are used by FlaskTest.

    :copyright: (c) 2015 by the Niot Team.
    :license: BSD, see LICENSE for more details.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_cache import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_redis import FlaskRedis
from flask_migrate import Migrate
from flask_themes2 import Themes
from flask_plugins import PluginManager
from flask_babelex import Babel
from flask_wtf.csrf import CsrfProtect
from flask_admin import Admin
from flask_socketio import SocketIO
import time
from threading import Thread
from flask_socketio import emit
from flask import Flask
import os

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.dirname(os.path.dirname(__file__)) + '/' + \
#                             'test.sqlite'
# Database
db = SQLAlchemy()

# Login
login_manager = LoginManager()

# Mail
mail = Mail()

# Caching
cache = Cache()

# Redis
redis_store = FlaskRedis()

# Debugtoolbar
debugtoolbar = DebugToolbarExtension()

# Migrations
migrate = Migrate()

# Themes
themes = Themes()

# PluginManager
plugin_manager = PluginManager()

# Babel
babel = Babel()

# CSRF
csrf = CsrfProtect()

# Admin
admin = Admin()

# SocketIO
socketio = SocketIO()

