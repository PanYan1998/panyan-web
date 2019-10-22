#!/usr/bin/python
# -*- coding: utf-8 -*-
import web
import datetime
import util
import hashlib
import settings

# 连接MySQL数据库
db = web.database(dbn='mysql', db='forum', user=settings.MYSQL_USERNAME, pw=settings.MYSQL_PASSWORD)


class User:
    def new(self, email, username, password):
        pwdhash = hashlib.md5(password).hexdigest()
        return db.insert('users', email=email, name=username, password=pwdhash,
                         picture='/static/img/user_normal.jpg', description='')

    def update(self, id, **kwd):
        try:
            if 'email' in kwd and kwd['email']:
                db.update('users', where='id=$id', email=kwd['email'], vars=locals())

            if 'password' in kwd and kwd['password']:
                pwdhash = hashlib.md5(kwd['password']).hexdigest()
                db.update('users', where='id=$id', password=pwdhash, vars=locals())

            if 'picture' in kwd and kwd['picture']:
                db.update('users', where='id=$id', picture=kwd['picture'], vars=locals())

            if 'description' in kwd and kwd['description']:
                db.update('users', where='id=$id', description=kwd['description'], vars=locals())

            return True
        except Exception, e:
            print e
            return False

    def login(self, username, password):
        '''登录验证'''
        pwdhash = hashlib.md5(password).hexdigest()
        users = db.select('users', what='id', where='name=$username AND password=$pwdhash', vars=locals())
        #users = db.where('users', name=username, password=pwdhash)
        if users:
            u = users[0]
            return u.id
        else:
            return 0

    def status(self, id):
        '''查询id对应的用户信息'''
        email = ''
        username = ''
        password_hash = ''
        picture = ''
        description = ''

        users = db.query('SELECT email, name, password, picture, description FROM users WHERE id=%d' % id)
        if users:
            u = users[0]
            email = u.email
            username = u.name
            password_hash = u.password
            picture = u.picture
            description = u.description

        return {'email': email, 'username': username, 'password_hash': password_hash,
                'picture': picture, 'description': description}

    def matched_id(self, **kwd):
        '''根据kwd指定的查询条件，搜索数据库'''
        users = db.select('users', what='id', where=web.db.sqlwhere(kwd, grouping='OR'))
        if users:
            # 目前只用于单条记录查询，因此只取第一个
            u = users[0]
            return u.id
        else:
            return 0

    def current_id(self):
        '''当前登录用户的id'''
        user_id = 0
        try:
            user_id = int(web.cookies().get('user_id'))
        except Exception, e:
            print e
        else:
            # 刷新cookie
            web.setcookie('user_id', str(user_id), settings.COOKIE_EXPIRES)
        finally:
            return user_id


class MessageBoard:
    def new(self, content, user_id):
        if user_id:
            return db.insert('messages', user_id=user_id, content=content)
        else:
            return 0

    def ddel(self, id):
        try:
            db.delete('messages', where='id=$id', vars=locals())
        except Exception, e:
            print e

    def list(self, page):
        '''获取第page页的所有文章'''
        per_page = settings.POSTS_PER_PAGE

        # 获取从offset开始共per_page个post
        offset = (page - 1) * per_page
        messages = db.query('''SELECT ,messages.id, content, messages.time, user_id, users.name AS username
                            FROM messages JOIN users
                            ON messages.user_id = users.id
                            ORDER BY messages.id DESC
                            LIMIT %d OFFSET %d''' % (per_page, offset))
        page_messages = []
        for m in messages:
            page_messages.append({'id': m.id, 'content': m.content, 'userid': m.user_id, 'username': m.username, 'message_time': m.time })

        # 计算总页数
        post_count = self.count()
        page_count = post_count / per_page
        if post_count % per_page > 0:
            page_count += 1

        return (page_posts, page_count)

    def count(self):
        '''获取message总数'''
        return db.query("SELECT COUNT(*) AS count FROM messages")[0].count




        
