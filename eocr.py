# ocr图片文字
import easyocr
import sys

reader = easyocr.Reader(['ch_sim', 'en'])
# path = '../../../mikhp/Desktop/1.jpg'
path = sys.argv[1]
print(path)
txt = reader.readtext(path)
for i in txt:
    print(i[1])
