# 此文件用来生成记忆大赛的训练字母数字表册
import datetime
import random

# 随机生成字母或者数字


def randme(MEM_type, MEM_width, list):
    randstr = ""
    count = len(list)

    if MEM_type == 0:
        randstr = str(random.randrange(MEM_width))
    elif MEM_type == 2:
        randstr = str(lst[random.randrange(count)]).replace("\n", "")
    else:
        if MEM_width == 10:
            randstr = chr(random.randint(97, 122))
        elif MEM_width == 100:
            a = chr(random.randint(97, 122))
            b = chr(random.randint(97, 122))
            randstr = "{0}{1}".format(a, b)
        else:
            a = chr(random.randint(97, 122))
            b = chr(random.randint(97, 122))
            c = chr(random.randint(97, 122))
            randstr = "{0}{1}{2}".format(a, b, c)
    return randstr


# 定义记忆表参数
# 记忆数字=0、字母=1 词组=2缺省为数字
MEM_type = 2
# 记忆数字或字符的宽度 10【1-9】数字、100【0-99】数字、1000【0-999】
MEM_width = 100
# 行数
MEM_row = 52
# 列数
MEM_col = 15

# 输出记忆表标题及头部信息
title = "最强大脑记忆表"
# 记忆表生成时间
t = str(datetime.datetime.now())
letgo = False
with open('out.txt') as f:  # 读取词语表文件
    lst = f.readlines()
    count = len(lst)  # 词组数量
    totol = MEM_col * MEM_row  # 要显示的总个数
    if count > totol:
        letgo = True  # 词组总个数超过要显示的个数，则表示可以继续生成词语表


if MEM_type == 2 and letgo == False:  # 词组
    print("out.txt文件中的词组数少于要显示的词组数，减少row、col满足显示需求")
    exit()

i = 1
j = 1
num = 1
print(title+"-----"+t+"\n")
f = open("mem.txt", "w+")
f.write(title+"-----"+t+"\n")
while i <= MEM_row:
    while j < MEM_col:
        num = randme(MEM_type, MEM_width, lst)
        f.write(num + "  ")
        print(num, end="  ")
        j += 1
    num = randme(MEM_type, MEM_width, lst)
    f.write(num + "  ")
    print(num, end="  ")
    f.write("  row")
    f.write(str(i))
    print("  row"+str(i))
    f.write("\n")
    print("\n")
    i += 1
    j = 1
f.close()
