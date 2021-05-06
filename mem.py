# 此文件用来生成记忆大赛的训练字母数字表册
import datetime
import random


# 定义记忆表参数
# 记忆数字=0、字母=1 缺省为数字
MEM_type = 0
# 记忆数字或字符的宽度 10【1-9】数字、100【0-99】数字、1000【0-999】
MEM_width = 10
# 行数
MEM_row = 20
# 列数
MEM_col = 40

# 输出记忆表标题及头部信息
title = "最强大脑记忆表"
# 记忆表生成时间
t = str(datetime.datetime.now())
i = 1
j = 1
num = 1
print(title+"-----"+t+"\n")
f = open("mem.txt", "w+")
f.write(title+"-----"+t+"\n")
while i <= MEM_row:
    while j < MEM_col:
        num = str(random.randrange(MEM_width))
        f.write(num + "  ")
        print(num, end="  ")
        j += 1
    # f.write("row" + str(i))
    num = str(random.randrange(MEM_width))
    f.write(num + "  ")
    print(num, end="  ")
    f.write("  row")
    f.write(str(i))
    f.write("\n")
    print("\n")
    i += 1
    j = 1
f.close()
