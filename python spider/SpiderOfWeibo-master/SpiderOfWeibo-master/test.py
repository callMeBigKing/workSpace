#coding:utf-8
#验证码url
import random
import urllib2
import Image
pin_code_url = "http://login.sina.com.cn/cgi/pin.php"
#产生随机数
pcid = "xd-01ee4d114e1c59964396d92937c2de294e20"
url_random = str(int(random.random() * 100000000))
pin_code_url = pin_code_url + "?r=" + url_random + "&s=0" + "&p=" + pcid
pin_code = urllib2.urlopen(pin_code_url).read()
# os.mknod("/home/ruansonsong/work/code.png")
f = open("/home/ruansongsong/work/code", "wb")
f.write(pin_code)
f.close()
image = Image.open("/home/ruansongsong/work/code")
image.show()
input_code = raw_input()
print input_code