# -*- coding: utf-8 -*-
from __future__ import division
from ashbin.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from sqlalchemy import desc
from flask_login import current_user
from ashbin.devices.models import Device
from sqlalchemy import and_

class Data(db.Model):
    __tablename__ = 'data'
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    data = db.Column(db.VARCHAR(255))
    occupancy = db.Column(db.Integer, default=0)            # 垃圾占用率
    temperature = db.Column(db.Integer)                     # 温度
    electric_level = db.Column(db.Integer)                  # 电量等级
    create_time = db.Column(db.DateTime, primary_key=True)

    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    def save(self, device_id=None, data=None,  create_time=None):
        """
        Saves an order and return an order object
        :param button:
        :param user:
        :return: Order object
    """
        if device_id:
            self.device_id = device_id
        if data:
            self.data = data
        if create_time:
            self.create_time = create_time

        if not self.create_time:
            self.create_time == datetime.now()

        device = Device.get(device_id)

        res = (0, 0, 0)
        if device and hasattr(device, 'garbage_can_obj'):
            bt_height = device.garbage_can_obj.bottom_height
            tp_height = device.garbage_can_obj.top_height
            res = parse_data(data, bt_height, tp_height)

        self.occupancy = res[0]
        self.temperature = res[1]
        self.electric_level = res[2]

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
    def get_gdatas(cls, user, device, page=1, per_page=15):
        if user.is_authenticated():
            return device.datas.order_by(desc(cls.create_time)).paginate(page, per_page, True).items

    @classmethod
    def get_datas_in_date(cls, device_id, limit_date):
        return cls.query.filter(and_(cls.device_id == device_id, cls.create_time >= limit_date)).all()


def parse_data(raw_data, bottom_height, top_height):
    """
    解析出数据
    :param raw_data: 原始数据
    :param height: 探头到垃圾桶底部距离
    :return:  (占用率， 温度， 剩余电量等级)
    数据解析如下：
    例如：a8c63b90bb00180713000371为服务器收到的16进制数据，解析如下：
        第0~3字节：a8c63b90为终端的32位设备地址
        第4字节：bb为超声波探头到被测平面的测量值，单位cm.转化十进制为187cm
        第5字节：00为第二路超声波测量值，默认没有第二路超声波，为0。意义同上。
        第6字节：18为终端测量的16进制温度值。转化为十进制为24℃。
        第7字节：07为终端电池剩余电量等级，一共7个等级。
                  07表示剩余电量为95%~100%，06为85%，06为70%，04为50%，04为50%，03为35%，02为25%，01为10%，00为0%
        第8~10字节：13 00 03为本终端的时间值，以BCD码形式表示，采24小时制，分别为时、分和秒，当终端收到服务器的同步时间后，此值为实际实时时间。
        第11字节：71为前面11个字节有异或校验值
    """
    assert bottom_height > top_height, u'底部高度应该大于顶部高度'
    current_height = int(raw_data[8:10], 16)
    # 占用率， 0 - 100， 以5为最小单位
    t = ((bottom_height - current_height) / (bottom_height - top_height)) * 100
    dm = divmod(t, 5)
    occupancy = dm[0] * 5
    temperature = int(raw_data[12:14], 16)
    electric_level = int(raw_data[14:16], 16)

    return (occupancy, temperature, electric_level)


if __name__ == '__main__':
    t = parse_data('a8c63b90bb00180713000371', 300, 100)
    print t[0]
    print t