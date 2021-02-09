#!/usr/bin/python
# -*- coding: utf-8 -*-
import web
import markdown

def make_html(c):
    return markdown.markdown(c)

def trim_utf8(text, length):
    '''utf8字符截取'''
    extra_flag = '...' if length < len(text.decode('utf-8')) else ''
    return text.decode('utf-8')[0:length].encode('utf-8') + extra_flag




def menu(user,manager):
    '''导航菜单'''
    cur_user_id = user.current_id()
    cur_manager_id = manager.current_id()
    if cur_user_id:
        status = user.status(cur_user_id)
        return [{'link': '/user/%d' % cur_user_id, 'name': status['username']},
				{'link': '/MessageBoard', 'name': '留言板'},
                {'link': '/logout', 'name': '退出'}]
    else:
    	if cur_manager_id:
	    	status = manager.status(cur_manager_id)
	    	return [{'link': '/manager/%d' % cur_manager_id, 'name': status['managername']},
					{'link': '/MessageBoard', 'name': '留言板'},
	        		{'link': '/logout', 'name': '退出'}]
        else:
        	return [{'link': '/ManagerLogin', 'name': '管理食堂'},
					{'link': '/login', 'name': '学生登录'},
					{'link': '/register', 'name': '注册'},
	                {'link': '/contact', 'name': '联系我们'}]




