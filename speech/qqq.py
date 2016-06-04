import re

# 去掉文件文本中的换行符号，用于pdf阅读

path=r"C:\Users\imgos\Desktop\file.txt"
file=open(path,'r')
data=file.read()
file.close()
data=re.sub(r'\.','。', data)

file=open(path,'w')
file.write(data)
file.close()
