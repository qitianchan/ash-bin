#-*-coding:utf-8
__author__ = 'qitian'

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

_basedir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(
                            os.path.dirname(__file__)))))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.dirname(__file__) + '/' + \
                            'test.sqlite'
print 'sqlite:///' + _basedir + '/' + \
                            'test.sqlite'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


if __name__ == '__main__':
    db.create_all()
    print 'Create database successed.'