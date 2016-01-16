# -*- coding: utf-8 -*-
from midstation.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from midstation.user.models import Button
from sqlalchemy import desc
from flask_login import current_user

class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    data = db.Column(db.VARCHAR(255))
    date = db.Column(db.DateTime)

    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    def save(self, carbage_can=None, create_time=None):
        """
        Saves an order and return an order object
        :param button:
        :param user:
        :return: Order object
    """
        db.session.add(self)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
        return self

    def delete(self):
        """
        :return:
        """
        db.session.delete(self)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()

    @classmethod
    def get_gdatas(cls, user, page=1, per_page=15):
        if user.is_authenticated():
            return user.orders.order_by(desc(cls.create_time), cls.button_id).paginate(page, per_page, True).items

    @classmethod
    def orders_count(cls):
        if current_user.is_authenticated():
            return current_user.orders.count()

