# -*-coding: utf-8 -*-
"""
    @Project: python-learning-notes
    @File   : download_image.py
"""

import time
from multiprocessing.pool import ThreadPool
import requests
import os
import numpy as np


def download_image(url, our_dir, index):
    '''
    根据url下载图片
    :param url:
    :return: 返回保存的图片途径
    '''
    basename = os.path.basename(url)
    try:
        res = requests.get(url)
        if res.status_code == 200:
            print("{} image download success:{}".format(index + 1, url))
            filename = os.path.join(our_dir, basename)
            with open(filename, "wb") as f:
                content = res.content
                # 使用Image解码为图片
                # image = Image.open(BytesIO(content))
                # image.show()
                # 使用opencv解码为图片
                # content = np.asarray(bytearray(content), dtype="uint8")
                # image = cv2.imdecode(content, cv2.IMREAD_COLOR)
                # cv2.imshow("Image", image)
                # cv2.waitKey(1000)
                f.write(content)
                f.close()
                # time.sleep(2)
            return filename
    except Exception as e:
        print(e)
        return None
    print("download image failed:{}".format(url))
    return None


def download_image_thread(url_list, our_dir, num_processes, remove_bad=False, Async=True):
    '''
    多线程下载图片
    :param url_list: image url list
    :param our_dir:  保存图片的路径
    :param num_processes: 开启线程个数
    :param remove_bad: 是否去除下载失败的数据
    :param Async:是否异步
    :return: 返回图片的存储地址列表
    '''
    # 开启多线程
    if not os.path.exists(our_dir):
        os.makedirs(our_dir)
    pool = ThreadPool(processes=num_processes)
    thread_list = []
    for index, image_url in enumerate(url_list):
        if Async:
            out = pool.apply_async(func=download_image, args=(image_url, our_dir, index))  # 异步
        else:
            out = pool.apply(func=download_image, args=(image_url, our_dir, index))  # 同步
        thread_list.append(out)

    pool.close()
    pool.join()
    # 获取输出结果
    image_list = []
    if Async:
        for p in thread_list:
            image = p.get()  # get会阻塞
            image_list.append(image)
    else:
        image_list = thread_list
    if remove_bad:
        image_list = [i for i in image_list if i is not None]
    return image_list


if __name__ == "__main__":
    our_dir = "./phone_images"
    url_list = ["https://www.listcompany.org/phone-1-1458257.png",
                "https://www.listcompany.org/phone-1-1446113.png",
                "https://www.listcompany.org/phone-1-1447152.png",
                "https://www.listcompany.org/phone-1-1412055.png"]
    startTime = time.time()
    image_list = download_image_thread(url_list, our_dir=our_dir, num_processes=4, remove_bad=True, Async=True)
    endTime = time.time()
    consumeTime = endTime - startTime
    print("程序运行时间：" + str(consumeTime) + " 秒")
    # print(image_list)
