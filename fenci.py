# coding=utf-8
'''
通过输入的txt文本获取用于最强大脑字词记忆的分词文件
'''
import jieba
import jieba.posseg as pseg
import time


def file_unique(filename, savefile, stopword='', encoding='utf-8'):
    '''文本文档去重去停用词

    :param filename: 需要处理的文本文档
    :param savefile: 保存路径
    :param stopword: 停用词文本文档
    :param encoding: 编码
    :return: 处理后的行数
    '''

    def read(filename, encoding='utf-8'):
        '''读取文本文档生成器'''
        encoding = 'ISO-8859-1'
        with open(filename, encoding=encoding) as f:
            for line in f:
                yield line.strip()  # 去除空格换行

    file = set(list(read(filename, encoding)))
    if stopword:
        stopword = set(list(read(stopword, encoding)))
    newfile = []
    for i in file:
        if i not in stopword:
            newfile.append(i)
    with open(savefile, mode='w', encoding=encoding) as f:
        for i in newfile:
            f.write(i + '\n')
    return len(newfile)


t1 = time.time()
f = open("input.txt", "rb")  # 读取文本
string = f.read().decode("utf-8")

words = pseg.cut(string)  # 进行分词
result = ""  # 记录最终结果的变量
for w in words:
    # 获取两个字符的名词
    # if len(w.word) > 1 and w.word != "" and w.word != " " and w.flag == "n":  # 加词性标注
    if len(w.word) > 2 and w.word != "" and w.word != " ":  # 不加词性标注
        result += str(w.word) + "\n"
print(result)
f = open("temp.txt", "w")  # 将结果保存到另一个文档中
f.write(result)
f.close()
file_unique(filename='temp.txt',
            savefile='out.txt', stopword='', encoding='ISO-8859-1')
t2 = time.time()
print("分词及词性标注完成,生成文件:out.txt，耗时："+str(t2-t1)+"秒。")  # 反馈结果
