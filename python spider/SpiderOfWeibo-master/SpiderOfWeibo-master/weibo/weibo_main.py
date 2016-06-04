#coding:utf-8
import urllib2
import post_encode
from weibo_login import WeiboLogin
import get_weibo
if __name__ == '__main__':
	Login = WeiboLogin('17089368196', 'tttt5555')
	if Login.login() == True:
		print "登录成功"
	#可以根据page来循环以便达到爬取多页的目的
	html = urllib2.urlopen("http://s.weibo.com/weibo/%25E5%2591%25A8%25E6%2589%25AC%25E9%259D%2592&page=3").read()
	#调用解析html内容的函数	
	get_weibo.write_all_info(html)