# -*- coding: utf-8 -*-
from midstation.user.models import Service, Customer
from flask_login import current_user


def get_service_choice():
    if current_user:
        li =  [(str(obj.id), obj.name) for obj in Service.query\
                    .filter_by(user_id=current_user.id).all()
                ]
        li.insert(0, ('0', u'--不选择--'))
        return li
    else:
        return []



def get_customer_choice():
    if current_user:
        li = [(str(obj.id), obj.name) for obj in Customer.query\
                    .filter_by(user_id=current_user.id).all()
                ]
        li.insert(0, ('0', u'--不选择--'))
        return li
    else:
        return []
