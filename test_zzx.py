from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilenames


def read_file(image_path):
    f = None
    try:
        f = open(image_path, 'rb')
        return f.read()
    except:
        print('read image file fail')
        return None
    finally:
        if f:
            f.close()


def upload_callback():
    messagebox.showinfo("Hello Python", "Hello Runoob")
    # selectPath()


def selectPath():
    path = askopenfilenames(initialdir='C:\\Windows',filetypes=[("all","*.*")])
    pathname.set(path)
    print(path)
    return path

#TODO 调用read_file函数读入图片 完成upload
file_content = read_file("D:/Desktop/pic.jpeg")

root = Tk()  # 创建窗口对象的背景色

upload_btn = Button(root, text="上传图片", command=selectPath)
upload_btn.pack()
pathname = StringVar()

path_entry = Entry(root, textvariable=pathname)
path_entry.pack(side=RIGHT)

root.mainloop()

