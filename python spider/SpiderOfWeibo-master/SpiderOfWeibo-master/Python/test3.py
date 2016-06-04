#coding:utf-8
import urllib
import urllib2
import Image
url ='http://login.sina.com.cn/cgi/pin.php?r=29129078&s=0&p=xd-578119aa4d3cd13389e6941274288af744d9'
html = urllib2.urlopen(url).read()
urllib.urlretrieve(url, '/home/ruansongsong/work/code.png')
image = Image.open('/home/ruansongsong/work/code.png')
image.show()