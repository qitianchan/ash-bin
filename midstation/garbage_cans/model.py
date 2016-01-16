# -*- coding: utf-8 -*-
__author__ = 'qitian'
from midstation.extensions import db


class GarbageCan(db.Model):
    __tablename__ = 'garbage_can'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


    def __init__(self, type, height):
        self.type = type
        self.height = height

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