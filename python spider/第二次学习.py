上次只做了一个简单的读取web页面的广度优先遍历
这次我们学习如何通过向web服务器发送post请求进行登录
主要还是搬一下网上的东西

第一步用Fiddler观察浏览器的行为，发送的post请求里面有哪些内容
这里我写给自己看的就不截图了，看一下fiddler中的webForm 和header就可以了
在header 里面我们可以看到request header里面有：
Accept-Encoding: gzip, deflate

所以我们需要对页面进行gzip解压

解压缩
import gzip
def ungzip(data):
    # data 为opener.open.reade
    try:
        print('正在解压...')
        data=gzip.decompress(data)
        print('解压完毕...')
    except:
        print('没有压缩无需解压')
    return data
第二步
表单中有_xsrf选项，所以我们需要从初始页面获取采用正则表达式
import re
def getXSRF(data):
    # data 为opener.open.reade
    cer=re.compile('name=\"_xsrf\" value=\"(.*)\"', flags = 0)
    strlist=cer.findall(data)
    return strlist[0]
第三步
发送post请求， 发射后系统会返回一个cookies，但是python有http.cookiejar
处理，无需自己处理
import http.cookiejar
import urllib.request
def getOpener(head):
    # head (dict 类) post请求中要发送的header
    cj=http.cookiejar.CookieJar()
    # 创建一个cookiejar 然后放进HTTPCookieProcessor
    pro=urllib.request.HTTPCookieProcessor(cj)
    opener=urllib.request.build_opener()
    # 创建一个opener 此时还未指定url
    header=[]
    for key , value in head.items():
        elem=(key,value)
        header.append(elem)
        # header 为元祖list
    opener.addheaders=header
    # 自动发出请求的时候会将header也发出去
    return opener

第四部正式运行
正式运行还差一点点, 我们要把要 POST 的数据弄成 opener.open() 支持的格式.
所以还要  urllib.parse 库里的 urlencode() 函数. 这个函数可以把 字典 或者 元组集合 类型的数据转换成 & 连接的 str.
url='https://www.zhihu.com/#signin/'
opener=getOpener(header)
op=opener.open(url,timeout=2)
data=op.read()
data=ungzip(data)
_xsrf=getXSRF(data.decode())
url+='login/phone_num'
phone_num='15605190875'
password='xiao123'
postDict={
    '_xsrf':_xsrf，
    'phone_num':phone_num,
    'password':password,
    'remember_me':'true'
}
postData=urllib.parse.urlencode(postDict).encode()
op=opener.open(url,postData)
data=op.read()
data=ungzip(data)
print(data.decode())

完整代码如下
import gzip
import re
import http.cookiejar
import urllib.request
import urllib.parse

def ungzip(data):
    try:        # 尝试解压
        print('正在解压.....')
        data = gzip.decompress(data)
        print('解压完毕!')
    except:
        print('未经压缩, 无需解压')
    return data

def getXSRF(data):
    cer = re.compile('name=\"_xsrf\" value=\"(.*)\"', flags = 0)
    strlist = cer.findall(data)
    return strlist[0]

def getOpener(head):
    # deal with the Cookies
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener

header = {

    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Accept-Encoding': 'gzip, deflate',
    'Host': 'www.zhihu.com',
    'DNT': '1'
}

url='https://www.zhihu.com/#signin/'
opener = getOpener(header)
op = opener.open(url)
data = op.read()
data = ungzip(data)     # 解压
_xsrf = getXSRF(data.decode())
url+='login/phone_num'
phone_num='15605190875'
password='xiao123'
postDict={
    '_xsrf':_xsrf，
    'phone_num':phone_num,
    'password':password,
    'remember_me':'true'
}
postData=urllib.parse.urlencode(postDict).encode()
op=opener.open(url,postData)
data=op.read()
data=ungzip(data)
print(data.decode())
