#-*-coding:utf-8
__author__ = 'qitian'

from midstation.extensions import db
from datetime import datetime
from midstation.utils.helpers import create_salt
from hashlib import sha1
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import IntegrityError

BUTTONS_PER_PAGE = 15

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    salt = db.Column(db.String(32), nullable=False)
    wechat_id = db.Column(db.String(200), unique=True)
    telephone = db.Column(db.String(15), unique=True)
    mobile_phone = db.Column(db.String(15), unique=True)
    address = db.Column(db.String(200))

    # One-to-many
    devices = db.relationship("Device", backref="user",
                              lazy='dynamic',
                              primaryjoin="Device.user_id == User.id",
                              cascade='all, delete-orphan'
                              )

    # One-to-many
    garbage_cans = db.relationship("GarbageCan", backref="user",
                              primaryjoin="GarbageCan.user_id == User.id",
                              cascade='all, delete-orphan'
                              )
    # One-to-many
    buttons = db.relationship("Button", backref="user",
                              primaryjoin="Button.user_id == User.id",
                              cascade='all, delete-orphan'
                              )
    #One-to-many
    services = db.relationship('Service',
                               backref='user',
                               primaryjoin='Service.user_id == User.id',
                               cascade='all, delete-orphan'
                               )
    # One-to-many
    customers = db.relationship('Customer',
                                backref='user',
                                primaryjoin='Customer.user_id == User.id',
                                cascade='all, delete-orphan'
                                )

    # One-to-many
    orders = db.relationship('Order',
                             backref='user',
                             lazy='dynamic',
                             primaryjoin='Order.user_id == User.id',
                             cascade='all, delete-orphan'
                             )

    # def __init__(self, username, wechat_id=None, telephone=None, mobile_phone=None):
    #     self.username = username
    #     self.wechat_id = wechat_id
    #     self.telephone = telephone
    #     self.mobile_phone = mobile_phone

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python

    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)


    def check_password(self, password):
        """Check passwords. If passwords match it returns true, else false"""

        if self.password is None:
            return False

        sha1_obj = sha1()
        sha1_obj.update(password+self.salt)

        return self.password == sha1_obj.hexdigest()

    @classmethod
    def create_user(cls,username, password):
        salt = create_salt()
        sha1_obj = sha1()
        sha1_obj.update(password+salt)

        user = User(username=username, password=sha1_obj.hexdigest(), salt=salt)
        return user.save()

    @classmethod
    def authenticate(cls, login, password):
        """A classmethod for authenticating users
        It returns true if the user exists and has entered a correct password

        :param login: This can be either a username or a email address.

        :param password: The password that is connected to username and email.
        """

        user = cls.query.filter_by(username=login).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False
        return user, authenticated

    def save(self):
        """
        Saves a user and return a user object.
        :param username: user name
        :param wechat_id: wechat id
        :param telephone:
        :param mobile_phone:
        :return:
        """

        db.session.add(self)
        try:
            db.session.commit()
        except Exception, e:
            db.session.rollback()
            raise e

        return self

    def delete(self):
        """
        delete a user
        :return:
        """
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception, e:
            db.session.rollback()
            raise e

    @classmethod
    def get_user_by_id(self, user_id):
        return User.query.filter_by(id=user_id).first()

    def all_buttons(self, page=1):
        """Returns a paginated result with all topics the user has created."""

        return Button.query.filter(Button.user_id == self.id).\
            order_by(Button.node_id.desc()).limit(page * BUTTONS_PER_PAGE).all()



class Button(db.Model):
    __tablename__ = 'buttons'

    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.String(50), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))

    orders = db.relationship('Order',
                             primaryjoin="Order.button_id == Button.id"
                             )


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



class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    wechat_template_id = db.Column(db.String(60))
    wechat_template = db.Column(db.String(500))                                                 # 微信模板内容
    count = db.Column(db.Integer, default=1)                                                    # 数量
    unit = db.Column(db.String(6), default=u'桶')                                                # 单位
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    price = db.Column(db.DECIMAL)
    # One-to-Many
    buttons = db.relationship('Button', backref='service',
                              primaryjoin='Button.service_id == Service.id')

    # One-to-Many
    orders = db.relationship('Order', backref='service',
                             primaryjoin='Order.service_id == Service.id')


    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    @classmethod
    def get(cls, id):
        id = int(id)
        return cls.query.filter_by(id=id).first()

    def save(self, user=None):
        """

        :param user:
        :return:
        """
        if user:
            self.user_id = user.id
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
        except SQLAlchemyError as e:
            db.session.rollback()
            raise

    def get_services(self, user):
        return user.services


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(30))
    addr = db.Column(db.String(120), nullable=False)
    telephone = db.Column(db.String(20))
    mobile_phone = db.Column(db.String(15))
    wechat_id = db.Column(db.String(50))

    # One-to-many
    buttons = db.relationship('Button', backref='customer', primaryjoin='Button.customer_id == Customer.id')


    def __init__(self, addr=None):
        self.addr = addr

    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    @classmethod
    def get(cls, id):
        id = int(id)
        return cls.query.filter_by(id=id).first()

    def save(self, user=None):
        """

        :param user:
        :return:
        """
        if self.id:

            db.session.add(self)
        else:
            if user:
                self.user_id = user.id
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
        if Button.query.filter_by(customer_id=self.id).first():
            raise IntegrityError

        db.session.delete(self)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e


if __name__ == '__main__':

    user = User.query.filter_by(username='qitian').first()
    if user is not None:
        print user.buttons

    # add service
    # service = Service(name=u'马杀鸡一个小时')
    # service.save(user=user)
    #

    # binding button
    service = Service.query.filter_by(name=u'马杀鸡一个小时').first()
    button = Button.query.filter_by(node_id='890087').first()
    if service and button:
        button = button.save(service=service)

    print button.service.name
    print service.buttons[0].node_id

    customer = Customer.query.filter_by(addr=u'南横村59号222房').first()
    # customer.save()
    if customer:
        button.save(customer=customer)
        print 'button binds with customer success!'
    else:
        print 'costomer is None'

    #
    print 'customer.buttons[0].node_id: ' + customer.buttons[0].node_id
    print customer.buttons[1].service.name

    # create an order by node id
    # def create_order(node_id):
    #     order = Order()
    #     button = Button.query.filter_by(node_id=node_id).first()
    #     service = button.service
    #
    #     order.save(button=button)
    #
    # order = Order.query.filter_by(button_id=Button.query.filter_by(node_id='890087').first().id).first()
    # print 'order service: ', order.service.name

