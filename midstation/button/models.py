# -*- coding: utf-8 -*-
__author__ = 'qitian'

from midstation.extensions import db

class Message(db.Model):
    __tablename__ = 'messages'
    eventUUID = db.Column(db.String(100), primary_key=True)
    node_id = db.Column(db.String(100), nullable=False)
    receipt_time = db.Column(db.DateTime)


    def __repr__(self):
        return '<Message %r>' % self.eventUUID

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()