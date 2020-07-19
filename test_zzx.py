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


def select_path():
    path = askopenfilenames(filetypes=[("all", "*.*")])
    pathname.set(path)
    return path


def upload():
    fns = root.tk.splitlist(pathname.get())
    # print(repr(fns))
    count = 0
    for picName in fns:
        if count == 0:
            picName = picName[1:]
            # print("start",picName)
        if count == len(fns) - 1:
            picName = picName[:-1]
            # print("end",picName)
        if count == len(fns) - 1 and len(fns) != 1:
            if ButtonList.get() == 0:
                result = util.ocr_general_basic(picName[1:-1])
            elif ButtonList.get() == 1:
                result = util.ocr_business_card(picName[1:-1])
            elif ButtonList.get() == 2:
                result = util.ocr_business_license(picName[1:-1])
            print(result)
            # TODO store result into system
        else:
            if ButtonList.get() == 0:
                result = util.ocr_general_basic(picName[1:-2])
            elif ButtonList.get() == 1:
                result = util.ocr_business_card(picName[1:-2])
            elif ButtonList.get() == 2:
                result = util.ocr_business_license(picName[1:-2])
            print(result)
        count = count + 1


root = Tk()
pathname = StringVar()

ButtonList = IntVar()  # IntVar 是tkinter的一个类，可以管理单选按钮

r1 = Radiobutton(root, variable=ButtonList, value=0, text="普通文本")
r2 = Radiobutton(root, variable=ButtonList, value=1, text="名片")
r3 = Radiobutton(root, variable=ButtonList, value=2, text="执照")
# variable=从属的“管理类” value=索引/ID
ButtonList.set(0)
r1.pack()
r2.pack()
r3.pack()

choose_btn = Button(root, text="选择图片", command=select_path)
choose_btn.pack()
path_entry = Entry(root, textvariable=pathname)
path_entry.pack(side=RIGHT)

upload_btn = Button(root, text="上传图片", command=upload)
upload_btn.pack()

root.mainloop()
