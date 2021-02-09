# -*- coding: utf-8 -*

import web
import settings
import model
import util
import os
import json
import hashlib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

urls = (
    "/", "Index",
    '/addmessage', 'AddMessage',
    '/addbulletin', 'AddBulletin',
    '/addFood', 'AddFood',
    '/edit/(\d+)', 'Edit',
    '/del/(\d+)', 'Del',
    '/del_b/(\d+)', 'Del_B',
    '/del_m/(\d+)', 'Del_M',
    '/del_c/(\d+)', 'Del_C',
    '/view/(\d+)', 'View',
    '/register', 'Register',
    '/login', 'Login',
    #'/find', 'Find',
    '/admin', 'Admin',
    '/ManagerLogin','ManagerLogin',
    '/logout', 'Logout',
    "/contact", "Contact",
    '/user/(\d+)', 'Profile',
    '/manager/(\d+)', 'Canteen',
    '/password', 'Password',
    '/QZcanteen', 'QZcanteen',
    '/HYcanteen', 'HYcanteen',
    '/XYcanteen', 'XYcanteen',
    '/HKcanteen', 'HKcanteen',
    '/MessageBoard', 'MessageBoard'
)

app = web.application(urls, globals(), autoreload=True)


##### BEG: 模板渲染 #####
curdir = os.path.abspath(os.path.dirname(__file__))
templates = curdir + '/templates/'
def render(params={}, partial=False):
    global_vars = dict(settings.GLOBAL_PARAMS.items() + params.items())
    
    if partial:
        return web.template.render(templates, globals=global_vars)
    else:
        return web.template.render(templates, base='layout', globals=global_vars)

def titled_render(subtitle=''):
    subtitle = subtitle + ' - ' if subtitle else ''
    return render({'title': subtitle + settings.SITE_NAME, 'make_html': util.make_html,
                   'trim_utf8': util.trim_utf8, 'menu': util.menu(model.User(), model.Manager())})
##### END: 模板渲染 #####


                                                                                                
class Index:
    def GET(self):
        return titled_render().visit()
    def POST(self):
        i = web.input(name='')
        foodname = i.name.decode('utf-8')
        food_id = model.Foods().find(foodname)
        raise web.seeother("/view/%d" % food_id)


class Contact:
	def GET(self):
		return titled_render('联系我们').contact()

class QZcanteen:
    def GET(self):
        i = web.input(page='1')
        page = int(i.page)
        page_foods, page_count = model.Foods().show(111,page)
        bulletin = model.BulletinBoard().show(111)
        return titled_render('清真食堂').QZcanteen(bulletin, page_foods, page_count, page)

class AddMessage:
    def GET(self):
        if model.User().current_id(): # 用户已登录
            return titled_render('发帖').addmessage()
        else:
            return titled_render().failed('操作受限，请先<a href="/login">登录</a>')

    def POST(self):
        i = web.input(content='')
        post_id = model.MessageBoard().new(i.content, model.User().current_id())
        raise web.seeother('/MessageBoard')


class AddBulletin:
    def GET(self):
        return titled_render('').addbulletin()
    def POST(self):
        i = web.input(content='')
        bulletin_id = model.BulletinBoard().new(i.content, model.Manager().current_id())
        manager_id = model.Manager().current_id()
        if manager_id:
            raise web.seeother('/manager/%d' % manager_id)
        else:
            raise web.notfound()


class AddFood:
    def GET(self):
        return titled_render('').addfood()
    def POST(self):
        i = web.input(name='', description='', foodpic={})
        if 'foodpic' in i:
            filepath = i.foodpic.filename.replace('\\','/') # 将Windows风格的斜杠转换为Linux风格
            filename = filepath.split('/')[-1] # 文件名（带后缀）
            ext = filename.split('.')[-1] # 扩展名
            # 扩展名不为空时才更新头像
            if ext:
                # 网站主页的相对路径
                rel_filename = settings.IMG_DIR + '/' + str(i.name) + ext
                # 服务器上的绝对路径
                abs_filename = curdir + '/' + rel_filename

        food_id = model.Foods().new(i.name, i.description, model.Manager().current_id(), rel_filename)
        fout = open(abs_filename, 'w')
        fout.write(i.foodpic.file.read())
        fout.close()
        raise web.seeother("/view/%d" % food_id)




        
class Edit:
    def GET(self, food_id):
        food_id = int(food_id)
        food = model.Foods().view(food_id)
        return titled_render().edit(food)
        

    def POST(self, food_id):
        i = web.input(name='', description='', foodpic={})
        food_id = int(food_id)

        food = model.Foods()
        if 'foodpic' in i:
            filepath = i.foodpic.filename.replace('\\','/') # 将Windows风格的斜杠转换为Linux风格
            filename = filepath.split('/')[-1] # 文件名（带后缀）
            ext = filename.split('.')[-1] # 扩展名
            # 扩展名不为空时才更新头像
            if ext:
                # 网站主页的相对路径
                rel_filename = settings.IMG_DIR + '/' + str(food_id) + ext
                # 服务器上的绝对路径
                abs_filename = curdir + '/' + rel_filename
                # 1.更新头像路径和简介
                if food.update(food_id, picture=rel_filename):
                    # 2.更新数据库成功后，保存头像
                    fout = open(abs_filename, 'w')
                    fout.write(i.foodpic.file.read())
                    fout.close()
        food.update(food_id, name=i.name)
        food.update(food_id, description=i.description)
        raise web.seeother("/view/%d" % food_id)
        

class Del:
    def GET(self, food_id):
        food_id = int(food_id)
        model.Comment().ddel(food_id)
        model.Foods().ddel(food_id)
        manager_id = model.Manager().current_id()
        if manager_id:
            raise web.seeother('/manager/%d' % manager_id)
        else:
            raise web.notfound()
        

class Del_B:
    def GET(self, bulletin_id):
        model.BulletinBoard().ddel(bulletin_id)
        manager_id = model.Manager().current_id()
        if manager_id:
            raise web.seeother('/manager/%d' % manager_id)
        else:
            raise web.notfound()


class Del_M:
    def GET(self, message_id):
        model.MessageBoard().ddel(message_id)
        user_id = model.User().current_id()
        manager_id = model.Manager().current_id()
        if user_id:
            raise web.seeother('/user/%d' % user_id)
        else:
            if manager_id:
                raise web.seeother('/manager/%d' % manager_id)
            else:
                raise web.notfound()

class Del_C:
    def GET(self, comment_id):
        model.Comment().del_ones(comment_id)
        user_id = model.User().current_id()
        manager_id = model.Manager().current_id()
        if user_id:
            raise web.seeother('/user/%d' % user_id)
        else:
            if manager_id:
                raise web.seeother('/manager/%d' % manager_id)
            else:
                raise web.notfound()



class View:
    def GET(self, food_id):
        food_id = int(food_id)
        food = model.Foods().view(food_id)
        if food:
            comment = model.Comment().list(food_id)
            return titled_render().view(food, comment)
        else:
            raise web.seeother('/')

    def POST(self, food_id):
        i = web.input(mycomment='')
        food_id = int(food_id)

        cur_user_id = model.User().current_id()
        if cur_user_id:
            #comment = model.Comment(int(food_id))
            comment_id = model.Comment().new(i.mycomment, cur_user_id, food_id)
            raise web.seeother("/view/%d" % food_id)
        else:
            return titled_render().failed('操作受限，请先<a href="/login">登录</a>')



class Login:
    def GET(self):
        return titled_render('学生登录').login()

    def POST(self):
        i = web.input(username='', password='')
        user_id = model.User().login(i.username, i.password)
        if user_id:
            # 设置cookie
            web.setcookie('user_id', str(user_id), settings.COOKIE_EXPIRES)
            raise web.seeother('/user/%d' % user_id)
        else:
            return titled_render().failed('登录验证失败，请检查帐号和密码是否正确')


class ManagerLogin:
    def GET(self):
        return titled_render('管理登录').managerlogin()

    def POST(self):
        i = web.input(managername='', password='')
        manager_id = model.Manager().login(i.managername, i.password)
        if manager_id:
            # 设置cookie
            if manager_id == int(1):
                raise web.seeother('/admin')
            else:
                web.setcookie('manager_id', str(manager_id), settings.COOKIE_EXPIRES)
                raise web.seeother('/manager/%d' % manager_id)
        else:
            return titled_render().failed('登录验证失败，请检查帐号和密码是否正确')




class Register:
    def GET(self):
        return titled_render('注册').register()

    def POST(self):
        try:
            i = web.input()
            user_id = model.User().new(i.studentID, i.email, i.username, i.password)
        except Exception as e:
            return titled_render().failed('邮箱或帐号已存在，请重新<a href="/register">注册</a>')
        else:
            if user_id:
                # 设置cookie
                web.setcookie('user_id', str(user_id), settings.COOKIE_EXPIRES)
                raise web.seeother('/user/%d' % user_id)

class MessageBoard:
	def GET(self):
         i = web.input(page='1')
         page = int(i.page)
         page_posts, page_count = model.MessageBoard().list(page)
         return titled_render('').MessageBoard(page_posts, page_count, page)


class Logout:
    def GET(self):
        if model.User().current_id() or model.Manager().current_id(): # 用户已登录
            # 取消cookie
            web.setcookie('user_id', '', -1)
            web.setcookie('manager_id', '', -1)
        raise web.seeother('/')
		
class Profile:
    def GET(self, user_id):
        user_id = int(user_id)
        status = model.User().status(user_id)
        if status['username']:
            if user_id == model.User().current_id():
                my_messages=model.MessageBoard().show(user_id)
                my_comments=model.Comment().show_ones(user_id)
                return titled_render(status['username']).master_profile(status['username'], status['picture'], status['description'], status['email'], my_messages, my_comments)
            else:
                return titled_render(status['username']).user_profile(status['username'], status['picture'], status['description'])
        else:
            raise web.notfound()

    def POST(self, user_id):
        # 获取当前登录用户的状态
        user_id = int(user_id)
        user = model.User()
        status = user.status(user_id)
        # 将头像和简介
        i = web.input(mypic={}, description='')
        #print(i)
        if 'mypic' in i:
            filepath = i.mypic.filename.replace('\\','/') # 将Windows风格的斜杠转换为Linux风格
            filename = filepath.split('/')[-1] # 文件名（带后缀）
            ext = filename.split('.')[-1] # 扩展名
            # 扩展名不为空时才更新头像
            if ext:
                # 网站主页的相对路径
                rel_filename = settings.IMG_DIR + '/' + str(user_id) + '_head.' + ext
                # 服务器上的绝对路径
                abs_filename = curdir + '/' + rel_filename
                # 1.更新头像路径和简介
                if user.update(user_id, picture=rel_filename):
                    # 2.更新数据库成功后，保存头像
                    fout = open(abs_filename, 'w')
                    fout.write(i.mypic.file.read())
                    fout.close()
            # 对简介不做检查，直接更新
            user.update(user_id, description=i.description)
        raise web.seeother('/user/%d' % user_id)


class Canteen:
    def GET(self, manager_id):
        manager_id = int(manager_id)
        status = model.Manager().status(manager_id)

        if status['managername']:
            if manager_id == model.Manager().current_id():
                page_bulletins=model.BulletinBoard().show(manager_id)
                page_foods=model.Foods().show_all(manager_id)
                return titled_render(status['managername']).manager_canteen(status['managername'], status['email'],page_bulletins, page_foods)
        else:
            raise web.notfound()

    def POST(self, manager_id):
        # 获取当前登录用户的状态
        manager_id = int(manager_id)
        manager = model.Manager()
        status = manager.status(manager_id)
        
        raise web.seeother('/manager/%d' % manager_id)

class Admin:
    def GET(self):
        page_bulletins=model.BulletinBoard().show_all()
        page_messages=model.MessageBoard().show_all()
        page_foods=model.Foods().list()
        return titled_render('admin').admin(page_bulletins,page_foods,page_messages)





class Password:
    def GET(self):
        return titled_render('密码').password()

    def POST(self):
        i = web.input(email='')
        web.header('Content-Type', 'application/json')
        user = model.User()
        user_id = user.matched_id(email=i.email)
        if user_id:
            status = user.status(user_id) # 获取当前状态
            temp_password = status['password_hash'][0:8] # 使用原来密码的“MD5值前8位”作为临时密码
            # 发送邮件
            subject = '请尽快修改您的密码'
            message = '''尊敬的%s：
                             您的临时密码是"%s"，请用该密码登录后，尽快修改密码，谢谢！
                      ''' % (status['username'], temp_password)
            try:
                web.sendmail(settings.SITE_SMTP_USERNAME, i.email, subject, message)
            except e: # 发送失败
                print e
            else: # 发送成功
                if user.update(user_id, password=temp_password): # 设置临时密码
                    return json.dumps({'result': True})
        # 邮箱未注册
        return json.dumps({'result': False})

        

# 导出的wsgi函数
application = app.wsgifunc()

if __name__ == "__main__":
	app.run()







