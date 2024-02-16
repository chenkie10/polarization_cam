import os
import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title('snapshot window')
window.geometry('400x400')
var1 = tk.StringVar()  # 输入文件名
# 图片格式,Radiobutton通过将传入的字符串变量（variable）换为value来实现按钮选择，再通过命令函数将value传到指定的位置
var2 = tk.StringVar()
entry = tk.Entry(window, textvariable=var1, show=None)  # 输入文本
entry.pack()


# copy功能对entry中的内容进行复制，调用了pyperclip库
def copy_filename():
    pyperclip.copy(entry.get())


def documents():
    pass


menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='New(N)')
filemenu.add_separator()
filemenu.add_command(label='Save as(S)')
filemenu.add_command(label='Print(P)')
filemenu.add_separator()
filemenu.add_command(label='Exit(E)', command=window.quit)

editmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Edit', menu=editmenu)
editmenu.add_command(label='Copy(C)', command=copy_filename)
tools = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Tools', menu=tools)
tools.add_command(label='Pencil(P)')
tools.add_command(label='Highlight(H)')
tools.add_command(label='Eraser(E)')
tools.add_separator()
tools.add_command(label='Option(O)')
helps = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=helps)
helps.add_command(label='Help(H)', command=documents)
helps.add_command(label='About(A)')

window.config(menu=menubar)


# clear_all函数用于清除entry中的文本
def clear_all():
    var1.set('')


# save函数用于在text中传入文件名并且清空entry
def save():
    msg = tk.messagebox.askyesno(
        title='Question', message='Do you want to save file as ' + entry.get())
    if msg == 1:
        text.insert('end', entry.get())
        clear_all()
    else:
        pass


# 判断text中是否有字符串（通过布尔值），若没有则跳过，若有则清空
def check_clear():
    if bool(text) == 0:
        pass
    else:
        text.delete('1.0', 'end')


def clear_entry():
    words = str(entry.get())
    if '.' in words:
        entry.delete(len(entry.get()) - 4, len(entry.get()))
    else:
        message = tk.messagebox.askyesno(
            title='Warning', message='Clear filename?')
        if message == 1:
            entry.delete(0, 'end')
        else:
            pass


# Save按钮用于在text框中输出最终的文件名，Clear按钮用于消除文件名后缀，重新选择新的文件后缀
button1 = tk.Button(window, text='Save', width=18, height=2, command=save)
button1.pack()
button2 = tk.Button(window, text='Clear Suffix', width=18,
                    height=2, command=clear_entry)
button2.pack()


# picture_format函数用于添加文件后缀和清空text
def picture_format():
    entry.insert('end', var2.get())
    check_clear()


r1 = tk.Radiobutton(window, text='JPG', variable=var2,
                    value='.jpg', command=picture_format)
r2 = tk.Radiobutton(window, text='BMP', variable=var2,
                    value='.bmp', command=picture_format)
r3 = tk.Radiobutton(window, text='PNG', variable=var2,
                    value='.png', command=picture_format)
r4 = tk.Radiobutton(window, text='GIF', variable=var2,
                    value='.gif', command=picture_format)
r1.pack()
r2.pack()
r3.pack()
r4.pack()
text = tk.Text(window, height=2)  # 得到的文本高度t
text.pack()

window.mainloop()

# def print_selection():
#     label_list.config(text='you have selected'+var1.get())
#
#
# r1 = tk.Radiobutton(window, text='Option A', variable=var1, value='A', command=print_selection)
# r1.pack()
