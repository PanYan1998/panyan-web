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
    '/register', 'Register',
    '/login', 'Login',
    '/logout', 'Logout',
    "/contact", "Contact",
    '/user/(\d+)', 'Profile',
    '/QZcanteen', 'QZcanteen',
    '/HYcanteen', 'HYcanteen',
    '/XYcanteen', 'XYcanteen',
    '/HKcanteen', 'HKcanteen',
    '/MessageBoard', 'MessageBoard'
)

app = web.application(urls, globals())


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
                   'trim_utf8': util.trim_utf8, 'menu': util.menu(model.User())})
##### END: 模板渲染 #####


                                                                                                
class Index:
    def GET(self):
    	page=1
        return titled_render().visit()


class Contact:
	def GET(self):
		return titled_render('联系我们').contact()

class QZcanteen:
	def GET(self):
		return titled_render('清真食堂').QZcanteen()

class Login:
    def GET(self):
        return titled_render('登录').login()

    def POST(self):
        i = web.input(username='', password='')
        user_id = model.User().login(i.username, i.password)
        if user_id:
            # 设置cookie
            web.setcookie('user_id', str(user_id), settings.COOKIE_EXPIRES)
            raise web.seeother('/user/%d' % user_id)
        else:
            return titled_render().failed('登录验证失败，请检查帐号和密码是否正确')

class Register:
    def GET(self):
        return titled_render('注册').register()

    def POST(self):
        try:
            i = web.input()
            user_id = model.User().new(i.email, i.username, i.password)
        except Exception as e:
            return titled_render().failed('邮箱或帐号已存在，请重新<a href="/register">注册</a>')
        else:
            if user_id:
                # 设置cookie
                web.setcookie('user_id', str(user_id), settings.COOKIE_EXPIRES)
                raise web.seeother('/user/%d' % user_id)

class MessageBoard:
	def GET(self):
		return titled_render('留言板').MessageBoard()


class Logout:
    def GET(self):
        if model.User().current_id(): # 用户已登录
            # 取消cookie
            web.setcookie('user_id', '', -1)
        raise web.seeother('/')
		
class Profile:
    def GET(self, user_id):
        user_id = int(user_id)
        status = model.User().status(user_id)
        if status['username']:
            if user_id == model.User().current_id():
                return titled_render(status['username']).master_profile(status['username'], status['picture'], status['description'])
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



if __name__ == "__main__":
	app.run()