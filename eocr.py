# ocr图片文字
import easyocr
import sys

reader = easyocr.Reader(['ch_sim', 'en'])
# path = '../../../mikhp/Desktop/1.jpg'
path = sys.argv[1]
print(path)
txt = reader.readtext(path)
with open("ocr.txt", "a+") as f:
    for i in txt:
        f.writelines(i[1])

f.close()