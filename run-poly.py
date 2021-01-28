import numpy as np
import matplotlib.pyplot as plt

#定义x、y散点坐标
x = [10,20,30,40,50,60,70,80]
x = np.array(x)
print('x is :\n',x)
num = [174,236,305,334,349,351,342,323]
y = np.array(num)
print('y is :\n',y)

#用3次多项式拟合
f1 = np.polyfit(x, y, 3)
print('f1 is :\n',f1)

# 显示出多项式
p1 = np.poly1d(f1)
print('p1 is :\n',p1)
 
# 显示出y值（用于测试）
#也可使用yvals=np.polyval(f1, x)
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