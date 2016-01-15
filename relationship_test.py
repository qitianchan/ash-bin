#-*-coding:utf-8
__author__ = 'qitian'

from alchemy import db
from datetime import datetime

# tags = db.Table('tags',
#     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
#     db.Column('page_id', db.Integer, db.ForeignKey('page.id'))
# )
#
# class Page(db.Model):
#     #文章对象,标签是多对多
#     __tablename__ = 'page'
#     id = db.Column(db.Integer, primary_key=True)
#     tags = db.relationship('Tag', secondary=tags,
#         backref=db.backref('pages', lazy='dynamic'))
#     title = db.Column(db.String(200), unique=True)
#     date = db.Column(db.DateTime)
#     page = db.Column(db.String(20000))
#
#     def __init__(self, title, date, page):
#         self.title = title
#         self.date = date
#         self.page = page
#
#     def __repr__(self):
#         return '<Page %r>' % self.title
#
# class Tag(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20), unique=True)
#     def __init__(self, name):
#         self.name = name
#
#     def __repr__(self):
#         return '<Tag: %r>' % self.name
#
#
# if __name__ == '__main__':
#     db.create_all()
#
#     def gen_tags():
#         ''' 生成一个 Tag 对象组成的列表'''
#         tags_list = []
#         for i in list(range(10)):
#             tag_name = "tag_" + str(i)
#             tag = Tag(name=tag_name)
#             tags_list.append(tag)
#         return tags_list
#
#
#     def gen_pages(count=10):
#         ''' 生成一个 Page 对象组成的列表，每个 Page 对象，都有 X 个 tags，来自上面 gen_tags 生成的列表。 '''
#         pages_list = []
#         tags = gen_tags()
#         for i in list(range(10)):
#             title = page = "page" + str(i)
#
#             page_obj = Page(title=title, page=page, date=datetime.utcnow())
#             page_obj.tags = tags # 将 gen_tags 生成的 Tag 对象们添加进去。
#             pages_list.append(page_obj)
#
#         return pages_list
#
#     pages = gen_pages() # 生成的 Page 对象列表。
#     db.session.add_all(pages) # 一次性添加所有 Page。
#     db.session.commit() # 提交到数据库
#
#
#     测试
#     import random
#
#     tag_name = 'python'
#     tag = Tag(name=tag_name)
#     tags = []
#     tags.append(tag)
#     page_obj = Page(title='Python orm', page='page10', date=datetime.utcnow())
#     page_obj.tags = tags
#     db.session.add(page_obj)
#     db.session.commit()
#
#     python_page = Tag.query.filter_by(name='python').first().pages.first()
#     print python_page.title
#     # print("tag.pages.all():", tag.pages.all())
#
#
#
#
#     obj_id = random.choice(list(range(10)))
#
#     tag_name = "tag_" + str(obj_id)
#     tag = Tag.query.filter_by(name=tag_name).first()
#     print("tag.pages.all(): ", tag.pages.all())
#
#     page_title = "page_" + str(obj_id)
#     page = Page.query.filter_by(title='page4').first()
#     print("page.tags", page.tags)
#
#     # new_tag_name = ''.join(random.choice(chars) for _ in list(range(10)))
#     # tag_obj = Tag(new_tag_name) # 或者查询出来的某个 Tag 实例。
#     # page.tags.append(tag_obj) # 为 page 增加一个 Tag。
#     # db.session.commit()
#
#     tag = Tag.query.filter_by(name=tag_name).first()
#
#
#
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    # addr_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    # addresses = db.relationship('Address',
    #                             foreign_keys=[addr_id],
    #                             backref='users'
    #                             )
    addresses = db.relationship('Address',
                                primaryjoin='Address.user_id == Users.id',
                                backref='users'
                                )

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Users %r>' % self.name


class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init(self, email):
        self.email = email

    def __repr__(self):
        return '<Address %r>' % self.email
#


if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()

    # # add address
    # addr = Address(email='Chan@sina.com')
    # # user = Users('Chan')
    # user = Users.query.filter_by(name='Chan').first()
    # if user is not None:
    #     user.addresses.append(addr)
    #     db.session.add(user)
    #     db.session.commit()
    # else:
    #     print "Not user named 'Chan'"

    # get user addresses

    user = Users.query.filter_by(name='Chan').first()
    if user is not None:
        print user.addresses

    addr = Address.query.filter_by(email='Chan@sina.com').first()
    if addr is not None:
        print addr.users