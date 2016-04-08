# -*-coding:utf-8 -*-
from ashbin.auth.views import auth
from ashbin.user.views import user
from ashbin.utils.listen_ws import ws_listening
from ashbin.extensions import login_manager
from ashbin.user.models import User
from ashbin.devices.models import Device
from ashbin.gdata.models import Data
from ashbin.garbage_cans.model import GarbageCan
from ashbin.extensions import csrf, redis_store, admin, db
from flask_admin.contrib.sqla import ModelView
from wtforms.fields import SelectField
from ashbin.devices.views import devices
from ashbin.garbage_cans.views import garbage_can
from ashbin.map.views import map
import websocket
from ashbin.extensions import socketio
from flask import session, request
from flask import Flask
from threading import Thread

from flask_socketio import emit, rooms, close_room,leave_room, join_room, disconnect
from flask_socketio import SocketIO
async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

def create_app(config=None):
    """Creates the app."""

    app = Flask(__name__, template_folder='templates/v1')

    # Use the default config and override it afterwards
    app.config.from_object('ashbin.configs.default.DefaultConfig')
    # Update the config
    app.config.from_object(config)

    configure_extensions(app)
    configure_blueprint(app)
    init_app(app)
    app.debug = app.config['DEBUG']
    return app


def configure_blueprint(app):
    app.register_blueprint(auth)
    app.register_blueprint(user, url_prefix=app.config['USER_URL_PREFIX'])
    app.register_blueprint(devices, url_prefix=app.config['DEVICES_URL_PREFIX'])
    app.register_blueprint(garbage_can, url_prefix=app.config['GARBAGE_CAN_URL_PREFIX'])
    app.register_blueprint(map, url_prefix=app.config['MAP_URL_PREFIX'])
    # app.register_blueprint(theme)

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
    socketio.init_app(app, async_mode=async_mode)



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

thread = None
def init_app(app):
# #
    @app.before_first_request
    def before_first_request():
        try:
            # listen = Listening()
            # ws = websocket.WebSocket()
            # ws.connect(LORIOT_URL)

            global thread
            if thread is None:
                print('ws_socket')
                thread = Thread(target=ws_listening)
                thread.daemon = True
                thread.start()

            # ws_listening_thread = Thread(target=ws_listening)
            # ws_listening_thread.start()
        except Exception, e:
            print e.message
            raise e


@socketio.on('test', namespace='/device')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    print(u'接收到的信息：%s' % message['data'])
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})


app = create_app()
 
if __name__ == '__main__':
    app.debug = True

    socketio.run(app, host='127.0.0.1', port=8098)
    # app.run()
