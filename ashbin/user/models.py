#-*-coding:utf-8
__author__ = 'qitian'

from ashbin.extensions import db
from datetime import datetime
from ashbin.utils.helpers import create_salt
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
                                    lazy='dynamic',
                                  primaryjoin="GarbageCan.user_id == User.id",
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
    def create_user(cls, username, password):
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
        except Exception as e:
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



if __name__ == '__main__':

    pass
