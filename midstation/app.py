# -*-coding:utf-8 -*-
from flask import Flask
from midstation.auth.views import auth
from midstation.station.views import station
from midstation.user.views import user
from midstation.customer.views import customer
from midstation.utils.listen_ws import ws_listening
from threading import Thread
from midstation.wechat.views import wechat
from midstation.utils.scrape_backend_v3 import detect_button_events
from extensions import login_manager
from midstation.user.models import User, Button
from midstation.devices.models import Device
from midstation.gdata.models import Data
from midstation.garbage_cans.model import GarbageCan
from midstation.service.views import service
from midstation.extensions import csrf, redis_store, admin, db
from flask_admin.contrib.sqla import ModelView
from wtforms.fields import SelectField
from midstation.order.views import order
from midstation.devices.views import devices
from midstation.garbage_cans.views import garbage_can
import websocket

def create_app(config=None):
    """Creates the app."""

    app = Flask(__name__)

    # Use the default config and override it afterwards
    app.config.from_object('midstation.configs.default.DefaultConfig')
    # Update the config
    app.config.from_object(config)

    configure_blueprint(app)
    configure_extensions(app)
    ws_listening_thread = Thread(target=ws_listening)
    ws_listening_thread.start()
    app.debug = app.config['DEBUG']
    return app


def configure_blueprint(app):
    app.register_blueprint(auth)
    app.register_blueprint(station, url_prefix=app.config['STATION_URL_PREFIX'])
    app.register_blueprint(user, url_prefix=app.config['USER_URL_PREFIX'])
    app.register_blueprint(service, url_prefix=app.config['SERVICE_URL_PREFIX'])
    app.register_blueprint(customer, url_prefix=app.config['CUSTOMER_URL_PREFIX'])
    app.register_blueprint(order, url_prefix=app.config['ORDER_URL_PREFIX'])
    app.register_blueprint(devices, url_prefix=app.config['DEVICES_URL_PREFIX'])
    app.register_blueprint(garbage_can, url_prefix=app.config['GARBAGE_CAN_URL_PREFIX'])
    # app.register_blueprint(wechat, url_prefix=app.config['WECHAT_URL_PREFIX'])


class MyView(ModelView):
    can_create = False
    column_list = ['username', 'telephone']
    form_overrides = dict(status=SelectField)
    form_args = dict(
        # Pass the choices to the `SelectField`
        status=dict(
            choices=[(0, 'waiting'), (1, 'in_progress'), (2, 'finished')]
        ))

    def __init__(self, session, **kwargs):
        super(MyView, self).__init__(User, session, endpoint='users', **kwargs)


def configure_extensions(app):

    db.init_app(app)
    login_configure(app)
    # Flask-WTF CSRF
    csrf.init_app(app)
    # redis
    redis_store.init_app(app)

    # Admin
    # admin.init_app(app)
    # admin.template_mode = 'bootstrap3'
    # admin.add_view(MyView(db.session))


def login_configure(app):
    login_manager.init_app(app)
    login_manager.login_view = app.config['LOGIN_VIEW']

    @login_manager.user_loader
    def load_user(user_id):
        user_instance = User.query.filter_by(id=user_id).first()
        if user_instance:
            return user_instance
        else:
            return None

# def init_app(app):
#
#     @app.before_first_request
#     def before_first_request():
#         try:
#             # listen = Listening()
#             # ws = websocket.WebSocket()
#             # ws.connect(LORIOT_URL)
#
#             # ws_listening_thread = Thread(target=ws_listening)
#             # ws_listening_thread.start()
#         except Exception, e:
#             print e.message
#             raise e

def get_signal():
    pass

# app = create_app()
 
if __name__ == '__main__':
    app = create_app()
    app.debug = True
    user = User.query.filter_by(id=5).first()
    print user

    # app.run()
