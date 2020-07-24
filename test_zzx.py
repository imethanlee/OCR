from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter.filedialog import askopenfilenames
from tkinter import ttk
import math
from util import *

# TODO 文件名有空格 备忘 核对功能 如果录入结果不对就手动录入
''''''


def func(event):
    print(comb.get())


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


def select_path(path_name):
    path = askopenfilenames(filetypes=[("all", "*.*")])
    path_name.set(path)
    return path


def getName(fns):
    count = 0
    namelist = []
    for picName in fns:
        if count == 0:
            picName = picName[1:]
            # print("start",picName)
        if count == len(fns) - 1:
            picName = picName[:-1]
            # print("end",picName)
        if count == len(fns) - 1 and len(fns) != 1:
            namelist.append(picName[1:-1])
        else:
            namelist.append(picName[1:-2])
        count = count + 1
    return namelist


imagelist = []
small_imagelist = []
resultlist = []


def upload():
    photo_area.delete(ALL)
    imagelist.clear()
    resultlist.clear()
    small_imagelist.clear()

    fns = root.tk.splitlist(pathname.get())
    # print(repr(fns))
    num_photo.set(len(fns))
    namelist = getName(fns)
    count = 0

    for name in namelist:

        if comb_value.get() == "普通文本":
            result = ocr_general_basic(name)
        elif comb_value.get() == "名片":
            result = ocr_business_card(name)
        elif comb_value.get() == "执照":
            result = ocr_business_license(name)
        ''''''
        resultlist.append(result)

        size = 200
        img = Image.open(name)

        if img.size[0] > img.size[1]:
            size_w = size
            size_h = int(img.size[1] * size / img.size[0])
            # img = img.resize((size, int(img.size[1] * size / img.size[0])))
        else:
            size_w = int(img.size[0] * size / img.size[1])
            size_h = size
            # img = img.resize((int(img.size[0] * size / img.size[1]), size))

        img = img.resize((size_w, size_h))
        photo = ImageTk.PhotoImage(img)
        small_imagelist.append(photo)

        # print(count % 2)
        # print(math.floor(count / 2))
        # x y
        photo_area.create_image(count % 2 * size, size * math.floor(count / 2), image=photo, anchor=NW)
        ''''''
        # imageLabel = Label(photo_area, image=photo)
        # imageLabel.grid(row=int(count/2), column=count+1)  # 自动对齐
        # imageLabel.pack()
        count = count + 1
    confirm_window(namelist, root)
    for result in resultlist:
        if comb_value.get() == "名片":
            sql_insert(OCR.BUSINESS_CARD, result)


def confirm_single(name, parent):
    def show_large_pic(name, parent):
        pic_wd = Toplevel(parent)
        image = Image.open(name)
        pic_size = 700

        if image.size[0] > image.size[1]:
            size_w = pic_size
            size_h = int(image.size[1] * pic_size / image.size[0])
            # img = img.resize((pic_size, int(img.size[1] * size / img.size[0])))
        else:
            size_w = int(image.size[0] * pic_size / image.size[1])
            size_h = pic_size
            # img = img.resize((int(img.size[0] * size / img.size[1]), size))

        image = image.resize((size_w, size_h))
        temp_photo = ImageTk.PhotoImage(image)
        imageLabel = Label(pic_wd, image=temp_photo)
        imageLabel.pack()
        pic_wd.mainloop()
    fns = root.tk.splitlist(name)
    namelist = getName(fns)
    name=namelist[0]

    cf_wd = Toplevel(parent)
    size = 650

    img_single = Image.open(name)
    if img_single.size[0] > img_single.size[1]:
        size_w = size
        size_h = int(img_single.size[1] * size / img_single.size[0])

    else:
        size_w = int(img_single.size[0] * size / img_single.size[1])
        size_h = size

    img_single = img_single.resize((size_w, size_h))
    photo_single = ImageTk.PhotoImage(img_single)

    photo_canv = Canvas(cf_wd, bd=1, width=660, height=550, relief=GROOVE, scrollregion=(0, 0, 500, 500))
    photo_canv.grid(row=1, column=0, columnspan=3)
    photo_canv.create_image(5, 5, image=photo_single, anchor=NW)
    result = ocr_business_card(name)
    addr = StringVar()
    addr.set(result['addr'])
    fax = StringVar()
    fax.set(result['fax'])

    business_image = put_image(name, 200)
    business_image_btn = Button(parent,
                                command=lambda: show_large_pic(name, parent),
                                image=business_image)
    business_image_btn.grid(row=0, column=0, rowspan=2)


def confirm_window(namelist, parent):
    cf_wd = Toplevel(parent)
    size = 650
    result = StringVar()
    ''''''
    for name in namelist:
        img = Image.open(name)
        if img.size[0] > img.size[1]:
            size_w = size
            size_h = int(img.size[1] * size / img.size[0])

        else:
            size_w = int(img.size[0] * size / img.size[1])
            size_h = size

        img = img.resize((size_w, size_h))
        photo = ImageTk.PhotoImage(img)
        imagelist.append(photo)
    photo_canv = Canvas(cf_wd, bd=1, width=660, height=550, relief=GROOVE, scrollregion=(0, 0, 500, 500))
    photo_canv.grid(row=1, column=0, columnspan=3)
    photo_canv.create_image(5, 5, image=imagelist[0], anchor=NW)
    curr = IntVar()
    result.set(resultlist[0])

    def next_photo():
        if len(namelist) == 1:
            return
        if curr.get() == 0:
            last_btn['state'] = NORMAL
        curr.set(curr.get() + 1)
        photo_canv.delete(ALL)
        photo_canv.create_image(5, 5, image=imagelist[curr.get()], anchor=NW)
        result.set(resultlist[curr.get()])
        if curr.get() == len(namelist) - 1:
            next_btn['state'] = DISABLED

    def last_photo():
        if len(namelist) == 1:
            return
        if curr.get() == len(namelist) - 1:
            next_btn['state'] = NORMAL
        curr.set(curr.get() - 1)
        photo_canv.delete(ALL)
        photo_canv.create_image(5, 5, image=imagelist[curr.get()], anchor=NW)
        result.set(resultlist[curr.get()])
        if curr.get() == 0:
            last_btn['state'] = DISABLED

    def confirm():
        pass

    def cancel():
        if len(namelist) == 1:
            cf_wd.destroy()
            return
        temp = curr.get()
        if curr.get() == len(namelist) - 1:  # last one
            last_photo()
        else:  # default:next photo
            next_photo()
        imagelist.remove(imagelist[temp])
        resultlist.remove(resultlist[temp])
        namelist.remove(namelist[temp])
        num_photo.set(temp - 1)

    last_btn = Button(cf_wd, text="上一张", width=11, command=last_photo, relief=GROOVE)
    last_btn.grid(row=0, column=0)

    next_btn = Button(cf_wd, text="下一张", width=11, command=next_photo, relief=GROOVE)
    next_btn.grid(row=0, column=1)

    confirm_btn = Button(cf_wd, text="确认", width=11, command=confirm, relief=GROOVE)
    confirm_btn.grid(row=3, column=0)

    cancel_btn = Button(cf_wd, text="取消", width=11, command=cancel, relief=GROOVE)
    cancel_btn.grid(row=3, column=1)

    result_entry = Entry(cf_wd, textvariable=result, width=100)
    result_entry.grid(row=1, column=4)

    cf_wd.mainloop()


'''
    count = 0
    for picName in fns:
        if count == 0:
            picName = picName[1:]
            # print("start",picName)
        if count == len(fns) - 1:
            picName = picName[:-1]
            # print("end",picName)
        if count == len(fns) - 1 and len(fns) != 1:
            if comb_value.get() == "普通文本":
                result = util.ocr_general_basic(picName[1:-1])
            elif comb_value.get() == "名片":
                result = util.ocr_business_card(picName[1:-1])
            elif comb_value.get() == "执照":
                result = util.ocr_business_license(picName[1:-1])
            print(result)
            # TODO store result into system
        else:
            if comb_value.get() == "普通文本":
                result = util.ocr_general_basic(picName[1:-2])
            elif comb_value.get() == "名片":
                result = util.ocr_business_card(picName[1:-2])
            elif comb_value.get() == "执照":
                result = util.ocr_business_license(picName[1:-2])
            print(result)
        count = count + 1
    '''

''''''


def put_image(name, size):
    image = Image.open(name)

    if image.size[0] > image.size[1]:
        size_w = size
        size_h = int(image.size[1] * size / image.size[0])
        # img = img.resize((size, int(img.size[1] * size / img.size[0])))
    else:
        size_w = int(image.size[0] * size / image.size[1])
        size_h = size
        # img = img.resize((int(img.size[0] * size / img.size[1]), size))

    image = image.resize((size_w, size_h))
    temp_photo = ImageTk.PhotoImage(image)

    return temp_photo


def upload_trade():
    trade_wd = Toplevel(root)
    size = 200
    results = StringVar()

    business_path = StringVar()

    frame_businesscard = Frame(trade_wd, height=200, width=500, bd=1, relief='groove')
    frame_businesscard.grid(row=0, column=0, columnspan=5)

    businesscard_edit = Button(frame_businesscard, text="编辑结果", width=11, command=lambda: select_path(), relief=GROOVE)
    businesscard_edit.grid(row=1, column=1)

    businesscard_upload = Button(frame_businesscard, text="上传图片", width=11,
                                 command=lambda: confirm_single(business_path.get(), frame_businesscard),
                                 relief=GROOVE)
    businesscard_upload.grid(row=1, column=2)
    # ------------------photo---------------

    business_entry = Entry(frame_businesscard, textvariable=business_path, width=25)
    business_entry.grid(row=0, column=1)

    businesscard_btn = Button(frame_businesscard, text="选择名片图片", width=11,
                              command=lambda: select_path(business_path), relief=GROOVE)
    businesscard_btn.grid(row=0, column=3)
    trade_wd.mainloop()


root = Tk()

pathname = StringVar()

comb_value = StringVar()  # 窗体自带的文本，新建一个值
comb = ttk.Combobox(root, textvariable=comb_value, state='readonly')  # 初始化
comb["values"] = ("普通文本", "名片", "执照")
comb.current(0)

comb.bind("<<ComboboxSelected>>", func)
comb.grid(row=0, column=2)

scrollbar = Scrollbar(root)
num_photo = IntVar()
photo_area = Canvas(root, bd=1, width=500, height=200, relief=GROOVE, yscrollcommand=scrollbar.set,
                    scrollregion=(0, 0, 500, math.ceil(num_photo.get() / 2) * 200 + 500))
photo_area.grid(row=2, column=1, columnspan=3)
# photo_area.config(width=300, height=200)
# photo_area.configure(scrollregion=photo_area.bbox('all'))
'''
frame1 = Frame(root, height=200, width=500, bd=1, highlightbackground="black", relief='groove',
               yscrollbarcommand=scrollbar)
frame1.grid(row=2, column=1, columnspan=5)'''
scrollbar.config(command=photo_area.yview)
scrollbar.grid(row=2, column=5, sticky=S + W + E + N)

single_btn = Button(root, text="上传单项", width=11, command=lambda: select_path(pathname), relief=GROOVE)
single_btn.grid(row=0, column=0)

trade_btn = Button(root, text="上传交易", width=11, command=upload_trade, relief=GROOVE)
trade_btn.grid(row=1, column=0)

path_entry = Entry(root, textvariable=pathname, width=25)
path_entry.grid(row=0, column=1)

upload_btn = Button(root, text="上传图片", command=upload, relief=GROOVE)
upload_btn.grid(row=4, column=1)

root.mainloop()

'''

ButtonList = IntVar()  # IntVar 是tkinter的一个类，可以管理单选按钮
r1 = Radiobutton(root, variable=ButtonList, value=0, text="普通文本")
r2 = Radiobutton(root, variable=ButtonList, value=1, text="名片")
r3 = Radiobutton(root, variable=ButtonList, value=2, text="执照")
# variable=从属的“管理类” value=索引/ID
ButtonList.set(0)
r1.grid(row=2, column=0)
r2.grid(row=2, column=1)
r3.grid(row=2, column=2)
'''

'''


def test():
    messagebox.showinfo('提示', 'test')


f_btn = Button(root, width=7,height=3,text="选择图片", command=test).grid(row=0,column=0,columnspan=2)
s_btn = Button(root, width=7,height=3,text="选择图片", command=test).grid(row=1,column=0,columnspan=1)
t_btn = Button(root, width=7,height=1,text="选择图片", command=test).grid(row=1,column=1,columnspan=1)
'''
