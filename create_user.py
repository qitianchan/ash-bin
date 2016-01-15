#-*-coding:utf-8
__author__ = 'qitian'

from alchemy import db, User
from relationship_test import Post, Category
# admin = User('qitian', 'qitianchan@sina.com')
# guest = User('chan', 'qitian_job@sina.com')
#
#
# db.session.add(admin)
# db.session.add(guest)
# db.session.commit()


# user = User.query.all()
# print user
#
# admin = User.query.filter_by(username='qitian').first()
# print admin
#
#
# py = Category('Python')
# p = Post('Hello Python!', "python is pretty cool", py)
# db.session.add(py)
# db.session.add(p)
# db.session.commit()

redis = Category('redis')
print redis.posts
print redis.posts.all()
