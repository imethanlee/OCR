from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilenames
import tkinter as tk
import util


def read_file(image_path):
    f = None
    try:
        f = open(image_path, 'rb')
        return f.read()
    except:
        print('image path', image_path)
        print('read image file fail')
        return None
    finally:
        if f:
            f.close()


def upload_callback():
    messagebox.showinfo("Hello Python", "Hello Runoob")
    # selectPath()


def select_path():
    path = askopenfilenames(filetypes=[("all", "*.*")])
    pathname.set(path)
    return path


def upload():
    fns = root.tk.splitlist(pathname.get())
    # print(repr(fns))
    count = 0
    print(fns)
    for picName in fns:
        if count == 0:
            picName = picName[1:]
            # print("start",picName)
        if count == len(fns) - 1:
            picName = picName[:-1]
            # print("end",picName)
        if count == len(fns) - 1 and len(fns) != 1:
            result = util.ocr_general_basic(picName[1:-1])
            print(result)
        else:
            result = util.ocr_general_basic(picName[1:-2])
            count = count + 1
            print(result)



root = Tk()  # 创建窗口对象的背景色
pathname = StringVar()
choose_btn = Button(root, text="选择图片", command=select_path)
choose_btn.pack()
path_entry = Entry(root, textvariable=pathname)
path_entry.pack(side=RIGHT)

upload_btn = Button(root, text="上传图片", command=upload)
upload_btn.pack()

root.mainloop()

# print(pathname.get())
