# -*- coding: utf-8 -*-
import sys
import os
import qrcode
import shutil


def del_file(filepath):
    """
    删除某一目录下的所有文件或文件夹
    :param filepath: 路径
    :return:
    """
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


if len(sys.argv) < 3:
    print("qr.py 文件名 字符数")
    sys.exit()

inputfile = sys.argv[1]
batch_size = int(sys.argv[2])

if os.path.isfile(inputfile) == False:
    print("文件不存在")
    sys.exit()

if batch_size > 450:
    batch_size = 450
    print("二维码字数超过最大值450，使用最大值")

if os.path.exists("qrimg") == True:
    print("目录存在，清空目录里面二维码图片文件,并删除")
    del_file("qrimg")
    # os.rmdir("qrimg")
else:
    print("qrimg目录不存在，创建存放二维码")
    os.mkdir("qrimg")

qr = qrcode.QRCode(
    version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=1)
with open(inputfile, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    f.close()
    print('行数：', len(lines))
    j = 0
    rqs = ""
    for line in lines:
        if len(line) + len(rqs) < batch_size:
            rqs = rqs + line
        else:
            rqs = rqs + line
            j = j+1
            print(rqs)
            qr.clear()
            qr.add_data(rqs)
            qr.make(fit=True)
            img = qr.make_image()
            filename = "./qrimg/" + str(j) + ".png"
            img.save(filename)
            rqs = ""
    j = j+1
    print(rqs)
    qr.clear()
    qr.add_data(rqs)
    qr.make(fit=True)
    img = qr.make_image()
    filename = "./qrimg/" + str(j) + ".png"
    img.save(filename)
