import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange

plt.rcParams['font.sans-serif'] = ['simHei']
plt.rcParams['axes.unicode_minus'] = False

def Lagrange_interpolate(degree):
    global a1, a2, a3
    xs = np.linspace(-1, 1, 1000)
    for i in range(degree + 1):
        l = np.array(np.linspace(-1, 1, i + 1))
        y = 1 / (1 + 25 * (l ** 2))
        L = lagrange(l, y)
        for i in range(degree + 1):
            if i == 5:
                a1, = plt.plot(xs, L(xs), color='red')
            elif i == 10:
                a2, = plt.plot(xs, L(xs), color='green')
            elif i == 20:
                a3, = plt.plot(xs, L(xs), color='blue')
            else:
                pass
        plt.legend([a1, a2, a3], ['5次插值', '10次插值', '20次插值'])
        plt.plot(xs, L(xs))
        plt.plot(xs, 1 / (1 + 25 * (xs ** 2)), 'black')
    plt.ylim((-4, 4))
    plt.yticks(np.linspace(-4, 4, 10))
    plt.title('{}次拉格朗日插值的龙格现象(红色为5次插值，绿色为10次，蓝色为20次插值)'.format(degree))
    plt.show()
Lagrange_interpolate(20)

# x = np.array(np.linspace(-1, 1, 6))
# y = 1 / (1 + 25 * (x ** 2))
# a = lagrange(x, y)
# print(x)
# print(a)
# plt.plot(x, a, 'r')
# plt.show()
# print(a.order)

# def lagelangri(order):
#     x = np.array(np.linspace(-1, 1, order + 1))
#     y = 1 / (1 + 25 * (x ** 2))
#     a = lagrange(x, y)
#     return a
# def draw(f,order):
#     x=np.array(np.linspace(-1, 1, order + 1))
#     plt.plot(x,f,'r')
#     plt.show()
# draw(lagelangri(10),10)
# xs = np.linspace(-1, 1, 1000)
# x1 = np.array(np.linspace(-1, 1, 6))
# x3 = np.array(np.linspace(-1, 1, 11))
# x5 = np.array(np.linspace(-1, 1, 21))
#
# y = 1 / (1 + 25 * (xs ** 2))
# y1 = 1 / (1 + 25 * (x1 ** 2))
# y3 = 1 / (1 + 25 * (x3 ** 2))
# y5 = 1 / (1 + 25 * (x5 ** 2))
#
# a1 = lagrange(x1, y1)
# a3 = lagrange(x3, y3)
# a5 = lagrange(x5, y5)
#
# plt.title('高次拉格朗日差值的龙格现象')
# y = plt.plot(xs, y, 'black')  # 原函数
# r = plt.plot(xs, a1(xs), 'red')  # 5次Lagrange插值
# g = plt.plot(xs, a3(xs), 'green')  # 10次Lagrange插值
# b = plt.plot(xs, a5(xs), 'blue')  # 20次Lagrange插值
# plt.show()
