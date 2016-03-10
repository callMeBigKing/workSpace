爬虫学习  scrapy 爬虫框架

基本原理就是程序来代替浏览器对web服务器进行访问
向web服务器发送请求然后得到响应，通过程序对所得到的响应进行处理
这里需要理解html 正则表达式 还有浏览器和服务器的交互方式post get respond request 交互方式
这些响应可以通过fiddler这个软件来学习

简单的伪代码
网页中的连接可以简单的看成一颗树，根节点是第一个访问的网页，通过广度优先搜索可以
遍历所有的连接

queue Q
# 队列
set S
# 集合S
startPoint="http://www.baidu.com"
Q.push(startPoint)
S.insert(startPoint)
# 访问之前标记已访问
while (Q.empyt==False):
    T=Q.top()
    # 队首元素出列
    for point in PageUrl(T)：
    # PageUrl 是指在T中的连接
        if (point not in S):
            Q.push(point)
            S.insert(point)

set 集合可以换成 Bloom Filter   优点是时间空间复杂度低，缺点是误算率高

用python 抓取指定页面
#encoding:UTF-8
# 说明编码
import urllib.request
url="http://www.baidu.com"
data=urllib.request.urlopen(url).read()
data=data.decode("UTF-8")
print(data)

urllib.request.urlopen(url, data=None, [timeout, ]*, cafile=None, capath=None, cadefault=False)
返回一个 <class ‘http.client.HTTPResponse’>

data['word']='Jecvay Notes'
url_values=urllib.parse.urlencode(data)
# 把dict 转换成 str

#
#
list 拥有队列的全部功能，但是效率不够高，这里我们的队列用 collection。deque
集合用set() 创建空集 ，{"1"，"2"} 创建非空集合

import re
import urllib.request
import urllib

from collections import deque

queue = deque()
visited = set()

url = 'http://news.dbanotes.net'  # 入口页面, 可以换成别的

queue.append(url)
cnt = 0

while queue:
  url = queue.popleft()  # 队首元素出队
  visited |= {url}  # 标记为已访问

  print('已经抓取: ' + str(cnt) + '   正在抓取 <---  ' + url)
  cnt += 1
  urlop = urllib.request.urlopen(url)
  if 'html' not in urlop.getheader('Content-Type'):
    continue
  # 我们用getheader()函数来获取抓取到的文件类型, 是html再继续分析其中的链接.
  # 避免程序异常中止, 用try..catch处理异常
  try:
    data = urlop.read().decode('utf-8')
  except:
    continue

  # 正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列
  linkre = re.compile('href=\"(.+?)\"')
  for x in linkre.findall(data):
    if 'http' in x and x not in visited:
        # 有可能是图片连接 加了http 就肯定是网页链接
      queue.append(x)
      print('加入队列 --->  ' + x)

在这个版本中并没有超时跳过的功能
改为 urlop = urllib.request.urlopen(url, timeout = 2)
支持自动跳转
在爬 http://baidu.com 爬回来的是没有用的东西，因为浏览器在访问的时候是自动跳转到www.baidu.com
在html 中跳转一般这样写
<html>
 <meta http-equiv=”refresh” content=”0;url=http://www.baidu.com/”>
</html>
