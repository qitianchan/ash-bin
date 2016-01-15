# -*-coding:utf-8 -*-
from flask import Flask
from midstation.auth.views import auth
from midstation.station.views import station
from midstation.user.views import user
from midstation.customer.views import customer

from threading import Thread
from midstation.wechat.views import wechat
from midstation.utils.scrape_backend_v3 import detect_button_events
from extensions import login_manager
from midstation.user.models import User, Button
from midstation.service.views import service
from midstation.extensions import csrf, redis_store, admin, db
from flask_admin.contrib.sqla import ModelView
from wtforms.fields import SelectField
from midstation.order.views import order

def create_app(config=None):
    """Creates the app."""

    # 探测按钮消息后台线程
    # t = Thread(target=detect_button_events)
    # t.setDaemon(True)
    # t.start()
    print u'本地开发，没有开通微信消息处理，已在服务器上开通'

    # Initialize the app
    app = Flask(__name__)

    # Use the default config and override it afterwards
    app.config.from_object('midstation.configs.default.DefaultConfig')
    # Update the config
    app.config.from_object(config)

    configure_blueprint(app)
    configure_extensions(app)
    # configure_extensions(app)
    app.debug = app.config['DEBUG']
    return app


def configure_blueprint(app):
    app.register_blueprint(auth)
    app.register_blueprint(station, url_prefix=app.config['STATION_URL_PREFIX'])
    app.register_blueprint(user, url_prefix=app.config['USER_URL_PREFIX'])
    app.register_blueprint(service, url_prefix=app.config['SERVICE_URL_PREFIX'])
    app.register_blueprint(customer, url_prefix=app.config['CUSTOMER_URL_PREFIX'])
    app.register_blueprint(order, url_prefix=app.config['ORDER_URL_PREFIX'])
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
    admin.init_app(app)
    admin.template_mode = 'bootstrap3'
    admin.add_view(MyView(db.session))





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


def get_signal():
    pass
 
if __name__ == '__main__':
    app = create_app()
    app.debug = True
    user = User.query.filter_by(id=5).first()
    print user

    # app.run()
