# -*- coding: utf-8 -*-
__author__ = 'qitian'
from sqlalchemy.exc import SQLAlchemyError
from flask import render_template, redirect, flash, blueprints
from flask_login import login_required, current_user
from midstation.extensions import db
from midstation.configs.default import DefaultConfig
from sqlalchemy import desc
class Device(db.Model):
    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(120), nullable=False)
    eui = db.Column(db.String(120), nullable=False)
    garbage_can_id = db.Column(db.Integer, db.ForeignKey('garbage_can.id'))
    garbage_can = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    occupancy = db.Column(db.Integer, default=0)           # 垃圾占用率
    temperature = db.Column(db.Integer)         # 温度
    electric_level = db.Column(db.Integer)      # 电量等级


    # one-to-many
    datas = db.relationship('Data', backref='device', primaryjoin="Data.device_id == Device.id")


    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    def save(self, mac=None, eui=None, garbage_can=None):
        """
        Saves an button infomation
        :param service:
        :param customer:
        :return:
        """

        if garbage_can and garbage_can.id:
            self.garbage_can_id = garbage_can.id
            self.garbage_can = garbage_can.type
        if mac:
            self.mac = mac
        if eui:
            self.eui = eui

        db.session.add(self)

        try:
            db.session.commit()
        except SQLAlchemyError, e:
            db.session.rollback()
            raise e
        return self

    def delete(self):
        """

        :return:
        """
        db.session.delete(self)
        try:
            db.session.commit()
        except SQLAlchemyError, e:
            db.session.rollback()
            raise e

    @classmethod
    def devices_count(cls):
        if current_user.is_authenticated():
            return current_user.devices.count()
    @classmethod
    def get_devices(cls, user, page=1, per_page=DefaultConfig.PER_PAGE):
        if user.is_authenticated():
            return user.devices.order_by(desc(cls.garbage_can)).paginate(page, per_page, True).items


def get_garbage_can_choice():
    if current_user:
        li = [(str(obj.id), obj.type) for obj in current_user.garbage_cans
                ]
        li.insert(0, ('0', u'--不选择--'))
        return li
    else:
        return []
