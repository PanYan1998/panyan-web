#!/usr/bin/python
# -*- coding: utf-8 -*-
import web
import datetime
import util
import hashlib
import settings

# 连接MySQL数据库
db = web.database(dbn='mysql', db='pyweb', user=settings.MYSQL_USERNAME, pw=settings.MYSQL_PASSWORD)


class User:
    def new(self, studentID, email, username, password):
        pwdhash = hashlib.md5(password).hexdigest()
        return db.insert('users', id=studentID, email=email, name=username, password=pwdhash,
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




class Manager:
    def new(self, managerID, email, username, password):
        pwdhash = hashlib.md5(password).hexdigest()
        return db.insert('Manager', id=managerID, email=email, name=username, password=pwdhash)

    def update(self, id, **kwd):
        try:
            if 'email' in kwd and kwd['email']:
                db.update('Manager', where='id=$id', email=kwd['email'], vars=locals())

            if 'password' in kwd and kwd['password']:
                pwdhash = hashlib.md5(kwd['password']).hexdigest()
                db.update('Manager', where='id=$id', password=pwdhash, vars=locals())

            return True
        except Exception, e:
            print e
            return False

    def login(self, managername, password):
        '''登录验证'''
        #pwdhash = hashlib.md5(password).hexdigest()
        Managers = db.select('Manager', what='id', where='name=$managername AND password=$password', vars=locals())
        #users = db.where('users', name=username, password=pwdhash)
        if Managers:
            m = Managers[0]
            return m.id
        else:
            return 0

    def status(self, id):
        '''查询id对应的用户信息'''
        email = ''
        managername = ''
        password = ''
       

        managers = db.query('SELECT email, name, password FROM Manager WHERE id=%d' % id)
        if managers:
            m = managers[0]
            email = m.email
            managername = m.name
            password = m.password
            

        return {'email': email, 'managername': managername, 'password': password}

    def matched_id(self, **kwd):
        '''根据kwd指定的查询条件，搜索数据库'''
        users = db.select('Manager', what='id', where=web.db.sqlwhere(kwd, grouping='OR'))
        if users:
            # 目前只用于单条记录查询，因此只取第一个
            u = users[0]
            return u.id
        else:
            return 0

    def current_id(self):
        '''当前登录用户的id'''
        manager_id = 0
        try:
            manager_id = int(web.cookies().get('manager_id'))
        except Exception, e:
            print e
        else:
            # 刷新cookie
            web.setcookie('manager_id', str(manager_id), settings.COOKIE_EXPIRES)
        finally:
            return manager_id





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

    def list(self, page ):
        '''获取第page页的所有文章'''
        per_page = settings.POSTS_PER_PAGE

        # 获取从offset开始共per_page个post
        offset = (page - 1) * per_page
        messages = db.query('''SELECT messages.id, content, messages.time, user_id, users.name AS username
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

        return (page_messages, page_count)

    def show(self, user_id):
        messages = db.query('''SELECT messages.id, content, messages.time, user_id
                            FROM messages JOIN users
                            ON messages.user_id = users.id
                            WHERE user_id = %d''' % user_id)
        my_messages = []
        for m in messages:
            my_messages.append({'id': m.id, 'content': m.content, 'userid': m.user_id, 'message_time': m.time })
        return (my_messages)

    def show_all(self):
        messages = db.query('''SELECT messages.id, content, messages.time, user_id
                            FROM messages JOIN users
                            ON messages.user_id = users.id''' )
        all_messages = []
        for m in messages:
            all_messages.append({'id': m.id, 'content': m.content, 'userid': m.user_id, 'message_time': m.time })
        return (all_messages)

    def count(self):
        '''获取message总数'''
        return db.query("SELECT COUNT(*) AS count FROM messages")[0].count



class BulletinBoard:
    def new(self, content, manager_id):
        if manager_id:
            return db.insert('bulletins', manager_id=manager_id, content=content)
        else:
            return 0

    def ddel(self, id):
        try:
            db.delete('bulletins', where='id=$id', vars=locals())
        except Exception, e:
            print e

    def show(self, managerid):
        
        bulletins = db.query('''SELECT bulletins.id, content, bulletins.time, manager_id, Manager.name AS managername
                            FROM bulletins JOIN Manager
                            ON bulletins.manager_id = Manager.id
                            WHERE manager_id = %d''' % managerid)
        page_bulletins = []
        for b in bulletins:
            page_bulletins.append({'id': b.id, 'content': b.content, 'managerid': b.manager_id, 'managername': b.managername, 'bulletin_time': b.time })


        return (page_bulletins)

    def show_all(self):
        bulletins = db.query('''SELECT bulletins.id, content, bulletins.time, manager_id, Manager.name AS managername
                            FROM bulletins JOIN Manager
                            ON bulletins.manager_id = Manager.id''')
        page_bulletins = []
        for b in bulletins:
            page_bulletins.append({'id': b.id, 'content': b.content, 'managerid': b.manager_id, 'managername': b.managername, 'bulletin_time': b.time })


        return (page_bulletins)

    def count(self):
        '''获取message总数'''
        return db.query("SELECT COUNT(*) AS count FROM bulletins")[0].count


class Comment:
    def new(self, content, user_id, food_id):
        try:
            return db.insert('comments', content=content, user_id=user_id, parent_id=food_id)
        except Exception, e:
            print e
            return 0

    def del_ones(self, id):
        try:
            #db.delete('comments', where='parent_id=$self.__parent_id', vars=locals())
            db.delete('comments', where='id=$id', vars=locals())
        except Exception, e:
            print e

    def ddel(self, food_id):
        try:
            #db.delete('comments', where='parent_id=$self.__parent_id', vars=locals())
            db.query('DELETE FROM comments WHERE parent_id=%d' % food_id)
        except Exception, e:
            print e

    def list(self,food_id):
        '''获取当前菜品（创建Comment实例时指定了food_id）下面的所有评论'''
        comments = db.query('''SELECT comments.id, content, comments.time, users.name AS username, user_id, users.picture AS user_face
                               FROM comments JOIN users
                               ON comments.user_id = users.id
                               WHERE comments.parent_id=%d
                               ORDER BY comments.id''' % food_id)
        return comments

    def show_ones(self, user_id):
        comments = db.query('''SELECT comments.id, content, comments.time, foods.id AS foodid,foods.name AS foodname
                               FROM comments JOIN users
                               ON comments.user_id = users.id
                               JOIN foods ON comments.parent_id = foods.id
                               WHERE comments.user_id=%d
                               ORDER BY comments.id''' % user_id)
        my_comments = []
        for m in comments:
            my_comments.append({'id': m.id, 'content': m.content, 'foodid': m.foodid, 'foodname': m.foodname,'comment_time': m.time })
        return (my_comments)



    def last(self,food_id):
        '''获取当前文章下面的最新评论'''
        last_comments = db.query('''SELECT comments.id, content, comments.time, users.name AS username, user_id, users.picture AS user_face
                                    FROM comments JOIN users
                                    ON comments.user_id = users.id
                                    WHERE comments.id=(SELECT MAX(id) FROM comments WHERE parent_id=%d)''' % food_id)
        if last_comments:
            return last_comments[0]

        return None

    def count(self, food_id):
        '''获取当前文章下面的评论总数'''
        return db.query("SELECT COUNT(*) AS count FROM comments WHERE parent_id=%d" % food_id)[0].count



class Foods:
    def new(self, name, description, manager_id, picture):
        if manager_id:
            return db.insert('foods', name=name, description=description, picture=picture, manager_id=manager_id)
        else:
            return 0

    def update(self, id, **kwd):
        try:
            if 'name' in kwd and kwd['name']:
                db.update('foods', where='id=$id', name=kwd['name'], vars=locals())

            if 'picture' in kwd and kwd['picture']:
                db.update('foods', where='id=$id', picture=kwd['picture'], vars=locals())

            if 'description' in kwd and kwd['description']:
                db.update('foods', where='id=$id', description=kwd['description'], vars=locals())

            return True
        except Exception, e:
            print e
            return False



    def view(self, id):
        '''获取id对应的菜品'''
        foods = db.query('''SELECT foods.id, foods.name, foods.description, foods.time, foods.manager_id, foods.picture
                            FROM foods JOIN Manager
                            ON foods.manager_id = Manager.id
                            WHERE foods.id = %d''' % id)
        if foods:
            return foods[0]

        return None

    def ddel(self, id):
        try:
            db.delete('foods', where='id=$id', vars=locals())
            #db.query('DELETE FROM posts WHERE id=%d' % id)
        except Exception, e:
            print e

    def show(self, managerid, page):
        per_page = settings.POSTS_PER_PAGE

        # 获取从offset开始共per_page个post
        offset = (page - 1) * per_page
        foods = db.query('''SELECT foods.id, foods.name, foods.description, foods.time, foods.manager_id, foods.picture
                            FROM foods JOIN Manager
                            ON foods.manager_id = Manager.id
                            WHERE Manager.id = %d
                            LIMIT %d OFFSET %d''' % (managerid, per_page, offset))
        page_foods = []
        for f in foods:
            page_foods.append({'id': f.id, 'name': f.name,'food_time': f.time,'picture':f.picture, 'description':f.description })

        # 计算总页数
        post_count = self.count()
        page_count = post_count / per_page
        if post_count % per_page > 0:
            page_count += 1

        return (page_foods, page_count)
        

    def list(self):
        foods = db.query('''SELECT id, name, time FROM foods
                            ORDER BY id DESC''' )
        return foods


    def show_all(self, manager_id):
       
        foods = db.query('''SELECT id, name, time FROM foods
                            WHERE manager_id=%d
                            ORDER BY id DESC''' % manager_id)
        return foods

    def find(self, foodname):
        foods = db.query('''SELECT foods.id, foods.name, foods.description, foods.time, foods.manager_id, foods.picture FROM foods
                           WHERE foods.name LIKE "%s" ''' % foodname)
        if foods:
            return foods[0].id

        return None

    def count(self):
        '''获取文章总数'''
        return db.query("SELECT COUNT(*) AS count FROM foods")[0].count



        
