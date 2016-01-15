# -*- coding: utf-8 -*-
from midstation.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from midstation.user.models import Button
from sqlalchemy import desc
from flask_login import current_user

class Data(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    button_id = db.Column(db.Integer, db.ForeignKey('buttons.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    service_name = db.Column(db.VARCHAR(255))
    price = db.Column(db.Integer)
    customer_name = db.Column(db.VARCHAR(64))
    customer_addr = db.Column(db.VARCHAR(512))
    phone = db.Column(db.VARCHAR(15))
    create_time = db.Column(db.DateTime, default=datetime.utcnow())
    solved = db.Column(db.Boolean, default=False)
    status = db.Column(db.SmallInteger, default=0)              # 订单状态：0-正在处理， 1-已处理，2-取消

    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    def save(self, button=None, create_time=None):
        """
        Saves an order and return an order object
        :param button:
        :param user:
        :return: Order object
        """
        if self.id:
            db.session.add(self)
            db.session.commit()
        elif button:
            self.button_id = button.id
            self.user_id = button.user.id
            service = button.service
            self.service_id = service.id
            self.service_name = service.name
            self.price = service.price
            customer = button.customer
            self.customer_name = customer.name
            self.phone = customer.telephone
            self.customer_addr = customer.addr
            if create_time:
                self.create_time = create_time
            self.status = 0
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
    def get_orders(cls, user, page=1, per_page=15):
        if user.is_authenticated():
            return user.orders.order_by(desc(cls.create_time), cls.button_id).paginate(page, per_page, True).items

    @classmethod
    def orders_count(cls):
        if current_user.is_authenticated():
            return current_user.orders.count()

def create_order(node_id):
    order = Order()
    button = Button.query.filter_by(node_id=node_id).first()

    if button.service_id is None or button.customer_id:
        raise ValueError(u'按鍵还未绑定服务或者客户,请先绑定')
    order.save(button=button)


