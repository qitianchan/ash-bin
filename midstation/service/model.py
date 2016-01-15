# -*- coding: utf-8 -*-
__author__ = 'qitian'
from midstation.extensions import db


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    wechat_template_id = db.Column(db.String(60))
    wechat_template = db.Column(db.String(500))                                                 # 微信模板内容
    count = db.Column(db.Integer, default=1)                                                    # 数量
    unit = db.Column(db.String(6), default=u'桶')                                                # 单位
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # One-to-Many
    buttons = db.relationship('Button', backref='service',
                              primaryjoin='Button.service_id == Service.id')

    # One-to-Many
    orders = db.relationship('Order', backref='service',
                             primaryjoin='Order.service_id == Service.id')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    def save(self, user=None):
        """

        :param user:
        :return:
        """
        if user:
            self.user_id = user.id
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """

        :return:
        """
        db.session.delete(self)
        db.session.commit()