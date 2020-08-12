from sql import *
from ps import *
from tkinter import *
from PIL import Image, ImageTk

# 实用工具函数在此定义
myfont = "宋体 12"


business_card_img = None
bankcard_img = None
business_license_img = None
invoice_img = None
general_basic_img = None


def ps(entry: Entry, btn: Button, ocr_type: OCR):
    name = entry.get()[1:-1]
    myps = PS(name)
    myps.run()

    image = Image.open(name)
    size = 175
    if image.size[0] > image.size[1]:
        size_w = size
        size_h = int(image.size[1] * size / image.size[0])
    else:
        size_w = int(image.size[0] * size / image.size[1])
        size_h = size
    image = image.resize((size_w, size_h))

    if ocr_type == OCR.GENERAL_BASIC:
        global general_basic_img
        general_basic_img = ImageTk.PhotoImage(image)
        btn.config(image=general_basic_img)
    if ocr_type == OCR.INVOICE:
        global invoice_img
        invoice_img = ImageTk.PhotoImage(image)
        btn.config(image=invoice_img)
    if ocr_type == OCR.BUSINESS_LICENSE:
        global business_license_img
        business_license_img = ImageTk.PhotoImage(image)
        btn.config(image=business_license_img)
    if ocr_type == OCR.BUSINESS_CARD:
        global business_card_img
        business_card_img = ImageTk.PhotoImage(image)
        btn.config(image=business_card_img)
    if ocr_type == OCR.BANKCARD:
        global bankcard_img
        bankcard_img = ImageTk.PhotoImage(image)
        btn.config(image=bankcard_img)
