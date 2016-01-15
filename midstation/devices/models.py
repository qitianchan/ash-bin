# -*- coding: utf-8 -*-
__author__ = 'qitian'

from flask import render_template, redirect, flash, blueprints
from flask_login import login_required, current_user
from midstation.extensions import db

class Device(db.Model):
    __tablename__ = 'buttons'

    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(120), nullable=False)
    eui = db.Column(db.String(120), nullable=False)
    garbage_can_id = db.Column(db.Integer, db.ForeignKey('garbage_can.id'))

    # one-to-many
    datas = db.relationship('Data', backref='device', primaryjoin="Order.device_id == Device.id")


    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    def save(self, user=None, service=None, customer=None):
        """
        Saves an button infomation
        :param user:
        :param service:
        :param customer:
        :return:
        """
        if user and user.id:
            self.user_id = user.id
        if service and service.id:
            self.service_id = service.id
        if customer and customer.id:
            self.customer_id = customer.id
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

