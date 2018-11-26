#!C:/Python27
# coding=utf-8

# from pytesser import *
import shutil

from PIL import Image, ImageEnhance, ImageFilter
import os
import fnmatch
import re, time

import urllib, random


# import hashlib

def getGray(image_file):
    tmpls = []
    for h in range(0, image_file.size[1]):  # h
        for w in range(0, image_file.size[0]):  # w
            tmpls.append(image_file.getpixel((w, h)))

    return tmpls


def getAvg(ls):  # 获取平均灰度值
    return sum(ls) / len(ls)


def getMH(a, b):  # 比较100个字符有几个字符相同
    dist = 0;
    for i in range(0, len(a)):
        if a[i] == b[i]:
            dist = dist + 1
    return dist


def getImgHash(fne):
    image_file = Image.open(fne)  # 打开
    image_file = image_file.resize((12, 12))  # 重置图片大小我12px X 12px
    image_file = image_file.convert("L")  # 转256灰度图
    Grayls = getGray(image_file)  # 灰度集合
    avg = getAvg(Grayls)  # 灰度平均值
    bitls = ''  # 接收获取0或1
    # 除去变宽1px遍历像素
    for h in range(1, image_file.size[1] - 1):  # h
        for w in range(1, image_file.size[0] - 1):  # w
            if image_file.getpixel((w, h)) >= avg:  # 像素的值比较平均值 大于记为1 小于记为0
                bitls = bitls + '1'
            else:
                bitls = bitls + '0'
    return bitls


'''         
   m2 = hashlib.md5()   
   m2.update(bitls)
   print m2.hexdigest(),bitls
   return m2.hexdigest()
'''


def get_compare(filename1, filename2):
    a = getImgHash(filename1)  # 图片地址自行替换
    b = getImgHash(filename2)
    compare = getMH(a, b)
    return compare


if __name__ == '__main__':
    for i in range(300):
        print(i)
        for j in range(4):
                filename1 = './image1/%s_%s.jpg' % (i, j)
                img1 = Image.open(filename1)
                if img1:
                    for x in range(i + 1, 300):
                        for y in range(4):
                            filename2 = './image1/%s_%s.jpg' % (x, y)
                            img2 = Image.open(filename2)
                            if img2:
                                im = Image.open(filename2)
                                for _ in range(3):
                                    # 指定逆时针旋转的角度
                                    # 旋转图片
                                    im_rotate = im.rotate(90)
                                    # im_rotate.show()
                                    im = im_rotate
                                    im.save(filename2)
                                    compare = get_compare(filename1, filename2)
                                    # print(compare)
                                    if compare > 90 and filename1 != filename2:
                                        shutil.move("./image1/" + filename1, "./image3/" + filename1)


