import string
import random
import sys
import math
from PIL import Image,ImageDraw,ImageFont,ImageFilter
def gene_text():
    source = list(string.letters)
    for index in range(0,10):
        source.append(str(index))
    return ''.join(random.sample(source,4))#number是生成验证码的位数

if __name__=="__main__":
    print(gene_text())

