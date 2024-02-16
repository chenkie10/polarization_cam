# -*- coding: utf-8 -*-
import datetime
import os
from arena_api.system import system
import tkinter as tk
from tkinter import messagebox
from examples import py_acquisition_multi_buffers
from examples import py_live_Mono8
from examples import py_live_Aolp_Mono8
from examples import py_live_Dolp_Mono8
from examples import py_live_Aolp_Mono8_hsv
from examples import py_live_Dolp_Mono8_hsv
window = tk.Tk()
window.title('Polarization Camera')  # 窗口标题
window.geometry('300x200')  # 窗口尺寸
var = tk.StringVar()
label_default = tk.Label(window, textvariable=var, bg='yellow', font=('Arial', 12), width=15,
                         height=2)  # 窗口内的标签及其细节
label_default.pack()
state = False  # 相机状态
var.set('No camera')  # 无相机的初始状态

def Aolp():
    py_live_Aolp_Mono8.example_entry_point()

def Dolp():
    py_live_Dolp_Mono8.example_entry_point()


def cam_view():
    py_live_Mono8.example_entry_point()

def Aolp_HSV():
    py_live_Aolp_Mono8_hsv.example_entry_point()

def Dolp_HSV():
    py_live_Dolp_Mono8_hsv.example_entry_point()
# situation函数为按钮的控制命令，改变相机的状态名称和Label的颜色
def situation():
    global state
    if state == 0:
        py_acquisition_multi_buffers.example_entry_point()
        state = True
        var.set('camera on')
        label_default.config(bg='green')
    else:
        system.destroy_device()
        print('Destroyed all created devices')
        state = False
        var.set('camera off')
        label_default.config(bg='red')


# 主菜单有两个选项‘Cam’和‘Help’,Cam的子菜单Camera Switch可以控制相机的开关，Exit用于关闭窗口
menubar = tk.Menu(window)
Cams = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Cam(C)', menu=Cams)
Cams.add_command(label='Camera Switch(C)', command=situation)
Cams.add_command(label='Camera View_Mono8(V)', command=cam_view)
Cams.add_separator()
Cams.add_command(label='Exit(E)', command=window.quit)


Polarization = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Polarization(P)', menu=Polarization)
Polarization.add_command(label='PolarizationAolp', command=Aolp)
Polarization.add_command(label='PolarizationDolp', command=Dolp)


HSV = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='HSV(H)', menu=HSV)
HSV.add_command(label='PolarizationAolp', command=Aolp_HSV)
HSV.add_command(label='PolarizationDolp', command=Dolp_HSV)


helps = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help(H)', menu=helps)
helps.add_command(label='Help(H)')
helps.add_command(label='About(A)')

# 按钮为off/on,单机一次，状态变换一次
button = tk.Button(window, text='off/on', bg='blue', height=2, width=15, command=situation)

button.pack()
window.config(menu=menubar)
window.mainloop()  # 主循环
