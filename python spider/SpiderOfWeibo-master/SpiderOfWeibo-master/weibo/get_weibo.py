#coding:utf-8
import urllib
import urllib2
import re
import os
import time
import random
#使用beautifulsoup对HTML页面进行解析
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#get_html()函数用于获取所爬取的页面的html源码
def decode_html(original_html):
	#将获取到的html源码分行，因为新浪微博将网页进行了压缩
	lines = original_html.splitlines()
	for line in lines:
		#以<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_weibo_direct开头的是所有微博内容
		#如果报错的话，说明被识别成机器人了，然后手动将最后输出的URL用浏览器打开，输入验证码
		#一般爬取30几页就会被识别为爬虫，但是这个程序也有用，因为新浪微博搜索最多显示50页
		if line.startswith('<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_weibo_direct","js":["apps'):
			#print "not caught"
			n = line.find('"html":"')
			if n > 0:
				decoded_html = line[n + 8: ].encode("utf-8").decode('unicode_escape').encode("utf-8").replace("\\", "")
			#else:
			#	print "caught"
	# print "@@@@@"
	# print decoded_html
	return decoded_html
#get_details()用于获得每条味浓的具体信息，如果看不懂的话可以去看看源码的HTML结构
def get_details(decoded_html):
	# html = decode_html(decoded_html)
	soup=BeautifulSoup(decoded_html)
	#得到作者、作者链接、微博正文
	div_content=soup.find_all(attrs={'class': 'content clearfix'})
	#得到发微博时间
	div_time=soup.find_all(attrs={'class':'feed_from W_textb'})
	#将用户名称，用户主页地址、微博正文、发微博时间初始化
	nick_name=[]
	nickname_href=[]
	content_text=[]
	time=[]
	#print get_content[0]
	for i in range(len(div_content)):
		#查找a标签
		a_tag=div_content[i].find('a')
		nick_name.append(a_tag.get('nick-name'))
		nickname_href.append(a_tag.get('href'))
		#查找p标签
		p_tag=div_content[i].find('p')
		content_text.append(p_tag.get_text())
	#得到发微博时间
	for j in range(len(div_time)):
		a_time=div_time[j].find('a')
		time.append(a_time.get('title'))
	# print content_text
	# print nickname_href
	return (nick_name,nickname_href,content_text,time)
#get_number_info()用于获得转发、评论、赞的数据
def get_number_info(decoded_html):#一次性得到所有数字
	# html = decoded_html(decoded_html)
	soup = BeautifulSoup(decoded_html)
	#获取标签内容
	#查找

	get=soup.find_all(attrs={'class': 'feed_action_info feed_action_row4'})
	# print get[1]
	#收集转发、评论、赞的数据
	get_number_info=[]
	for i in range(len(get)):
		#转发
		forward=get[i].find(attrs={'action-type':'feed_list_forward'})
		forward_em=forward.find_all('em')
		#判断数据是否为0，
		if (len(forward_em[0].get_text())==0):
			temp_forward="0"
			get_number_info.append(temp_forward)
		else:
			temp_forward=forward_em[0].get_text()
			get_number_info.append(temp_forward)
		#评论
		comment=get[i].find(attrs={'action-type':'feed_list_comment'})
		if bool(comment.find_all('em')):
			comment_em=comment.find_all('em')
			temp_comment=comment_em[0].get_text()
			get_number_info.append(temp_comment)
		else:
			temp_comment="0"
			get_number_info.append(temp_comment)
		#赞
		like=get[i].find(attrs={'action-type':'feed_list_like'})
		like_em=like.find_all('em')
		if (len(like_em[0].get_text())==0):
			temp_like="0"
			get_number_info.append(temp_like)
		else:
			temp_like=like_em[0].get_text()
			get_number_info.append(temp_like)
	return get_number_info
#write_all_info()将所有数据写入文本
def write_all_info(original_html):
	get_decoded_html = decode_html(original_html)
	(nick_name_list, nick_name_href_list, content_text_list, time_list) = get_details(get_decoded_html)
	number_info_list = get_number_info(get_decoded_html)
	#文件保存路径
	path='/home/ruansongsong/work/ruansongsong/' 
	isExists=os.path.exists(path)
	if not isExists:
	    os.makedirs(path)
	temp=0
	for i in range(len(nick_name_list)):
		write_all_list=open(path+"weibo.txt",'a')
		write_all_list.writelines("微博用户名称："+nick_name_list[i]+"\n"+"微博链接："+nick_name_href_list[i]+"\n"+"正文:"+"\n"+content_text_list[i]+"\n"+"发微博时间："+time_list[i]+"\n")
		j=0
		#由于我是将转发、评论、赞的数据储存到一个list中的，所以每一个微博正文要写入3个数据。
		while (j!=3):
			write_all_list.writelines("==="+number_info_list[temp]+"==="+"\n")
			j+=1
			temp+=1
		write_all_list.close()