import time
from multiprocessing.pool import ThreadPool
import os
import numpy as np
import csv
from PIL import Image
import pytesseract

store_file = os.path.dirname(__file__) + 'phone_number.csv'
# 打开(创建)文件
file = open(store_file, 'w')
# csv写法
writer = csv.writer(file)

writer.writerow(["图片", '数字'])


def ocr_image(path, index):
    codes = pytesseract.image_to_string(Image.open(path))
    codes = codes.strip()
    correct_result = codes.replace(
        '—', '-').replace('-—', '-').replace('--', '-').replace(' ', '').replace('$', '8').replace(',', '|')
    print(index+1, 'ocr识别结果: ', correct_result)
    url = "https://www.listcompany.org/"+path.split('/')[1]
    writer.writerow([url, correct_result])


if __name__ == "__main__":
    # codes = pytesseract.image_to_string(
    #     Image.open('phone_images/phone-1-890461.png'))

    # 下面这张图片识别不了??? 拉吉
    # codes = pytesseract.image_to_string(
    #     Image.open('phone_images/phone-1-1527476.png'))

    # print('ocr识别结果', codes)

    download_list = os.listdir('phone_images')
    print('图片文件夹共读到', len(download_list), '个数据')
    for index, item in enumerate(download_list):
        ocr_image('phone_images/'+item, index)
