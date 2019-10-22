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


def menu(user):
	cur_user_id = user.current_id()
	if cur_user_id:
		status = user.status(cur_user_id)
		return [{'link': '/user/%d' % cur_user_id, 'name': status['username']},
                {'link': '/account/posts', 'name': '留言板'},
                {'link': '/account/settings', 'name': '个人中心'},
                {'link': '/logout', 'name': '退出'}]
	else:
		return [{'link': '/visit', 'name': '游客'},
				{'link': '/login', 'name': '登录'},
				{'link': '/register', 'name': '注册'},
                {'link': '/contact', 'name': '联系我们'}]


