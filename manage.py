# -*- coding: utf-8 -*-
#!/usr/bin/env python
import time
from threading import Thread

from flask_script import (Manager, Shell, Server, prompt, prompt_pass,
                          prompt_bool)
from flask_migrate import MigrateCommand, upgrade

from ashbin.app import create_app
from ashbin.extensions import db, plugin_manager
from ashbin.utils.scrape_backend import detect_button_events
from ashbin.extensions import socketio
# Use the development configuration if available
from ashbin.configs.default import DefaultConfig as Config

app = create_app()
manager = Manager(app)


# Run local server
# manager.add_command("runserver", Server("localhost", port=8099))

@manager.command
def runserver():
    socketio.run(app, host='localhost', port=8098)

@manager.command
def initdb():
    """Creates the database."""

    upgrade()


@manager.command
def dropdb():
    """Deletes the database."""

    db.drop_all()


if __name__ == "__main__":
    manager.run()
    # db.drop_all(app=app)
    # db.create_all(app=app)
