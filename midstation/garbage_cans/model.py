# -*- coding: utf-8 -*-
__author__ = 'qitian'
from midstation.extensions import db
from flask_login import current_user
from midstation.configs.default import DefaultConfig
from sqlalchemy import desc


class GarbageCan(db.Model):
    __tablename__ = 'garbage_can'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), nullable=False)
    bottom_height = db.Column(db.Integer, nullable=False)               # 探头距离底部高度
    top_height = db.Column(db.Integer, nullable=False)                  # 探头距离垃圾桶边沿高度
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # device_id = db.Column(db.Integer, db.ForeignKey('device.id'))

    # def __init__(self, type, height):
    #     self.type = type
    #     self.height = height

    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    def save(self):
        """

        :param user:
        :return:
        """
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """

        :return:
        """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get(cls, id):
        return cls.query.filter(GarbageCan.id == id).first()



    @classmethod
    def can_count(cls):
        if current_user.is_authenticated():
            return current_user.garbage_cans.count()


    @classmethod
    def get_garbage_cans(cls, user, page=1, per_page=DefaultConfig.PER_PAGE):
        if user.is_authenticated():
            return user.garbage_cans.paginate(page, per_page, True).items