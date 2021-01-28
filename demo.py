# coding: utf-8

# =================
# Author: wenxiangyu
# Time: 2021/1/28
# =================

import matplotlib.pyplot as plt
import numpy as np
import random

from PIL import Image

# 全局参数
r = 0.5  # 离散点保留比例,越大保留比例越少
GRAY = 200  # 二值化阈值

# 获取二值图片中曲线的坐标
def get_idx(img):
    shape = img.shape
    
    x = list()
    y = list()
    
    for j in range(shape[1]):
        for i in range(shape[0]):
            # 使用random保留不同个数的散点值
            ran = random.random()
            if img[i][j] == 0 and ran >= r:
                x.append(j)
                # shape[0] - i 表示将坐标进行转换，从左下角作为坐标原点
                y.append(shape[0] - i)

    return x, y

# 绘制函数图像
def plot_func(img):

    x, y = get_idx(img)

    #定义x、y散点坐标
    # x = [10,20,30,40,50,60,70,80]
    x = np.array(x)
    print('x is :\n',x)
    # num = [174,236,305,334,349,351,342,323]
    y = np.array(y)
    print('y is :\n',y)

    #用多项式拟合
    f1 = np.polyfit(x, y, 3)
    print('f1 is :\n',f1)

    # 显示出多项式
    p1 = np.poly1d(f1)
    print('p1 is :\n',p1)
    
    # 显示出y值（用于测试）
    yvals = p1(x)  #拟合y值
    print('yvals is :\n',yvals)

    #绘图
    plot1 = plt.plot(x, y, 's',label='original values')
    plot2 = plt.plot(x, yvals, 'r',label='polyfit values')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(loc=4) #指定legend的位置右下角
    plt.title('polyfitting')
    plt.show()

# 二值化图片
def binarize_img(img_path):
    img = Image.open(img_path)
    
    # 模式L为灰色图像，它的每个像素用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度。
    Img = img.convert('L')
    Img.save("test1.jpg")
    
    # 自定义灰度界限，大于这个值为黑色，小于这个值为白色
    threshold = GRAY

    # 图片二值化    
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    photo = Img.point(table, '1')
    photo.save("test2.jpg")
    return photo

# 将二值化图片中较粗的函数图像，直接转为较细
# 的图像,(例如从10pix转为1pix),降低对函数拟合
# 的影响
def thin_curve(img):
    # from Image to Numpy
    b_img = np.array(img)

    # shape = (370, 460)
    shape = b_img.shape

    for i in range(shape[0]):
        flag = 0
        for j in range(shape[1]):
            # 判断是否到达曲线的左边缘
            if b_img[i][j] == 0 and flag == 0 and j < shape[1]-10:
                counter_black = 0
                # 这里的10和下面的10都是阈值,表示连续多少个相同的像素值,达到判别标准
                for k in range(10):
                    if b_img[i][j+k] == 0:
                        counter_black += 1
                if counter_black >= 1:
                    flag = 1
                    continue
            
            # 判断是否到达大部分空白区域
            if b_img[i][j] == 1 and flag == 1 and j < shape[1]-10:
                counter_white = 0
                for k in range(10):
                    if b_img[i][j+k] == 1:
                        counter_white += 1
                if counter_white >= 10:
                    flag = 0
                    continue
            
            if flag == 1:
                b_img[i][j] = 1
            
    im = Image.fromarray(b_img)
    im.save("test3.jpg")
    return b_img

if __name__ == "__main__":
    
    # 任意函数图像输入
    img_path = '5.jpg'
    b_img = binarize_img(img_path)

    t_img = thin_curve(b_img)

    plot_func(t_img)