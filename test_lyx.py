import re
from tkinter import *
from util import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter.filedialog import askopenfilenames
from tkinter import ttk
import math

# TODO: 1.裁剪旋转功能合并（基本完成） 2. 保存图片 3. 修改与删除 4. 上传单项的entry 5. 编辑结果


def path_to_list(input: str):
    flag = False
    lst = []
    path = ""
    for char in input:
        if char == "'" and flag == False:
            flag = True
            continue
        if char == "'" and flag == True:
            flag = False
            lst.append(path)
            path = ""
            continue
        if flag:
            path += char
    return lst


def func(parent, value, tree):
    search(parent, value, tree, '')


def id_match(sid):
    id_format = "(^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$)|(^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}[0-9Xx]$)"
    reg = re.compile(id_format)
    if re.match(reg, sid):
        return re.match(reg, sid)
    return None


def date_match(date):
    date_format = "((((19|20)\d{2})[-.](0?[13578]|1[02])[-.](0?[1-9]|[12]\d|3[01]))|(((19|20)\d{2})[-.](0?[469]|11)[-.](0?[1-9]|[12]\d|30))|(((19|20)\d{2})[-.]0?2[-.](0?[1-9]|1\d|2[0-8])))"
    reg = re.compile(date_format)
    if re.match(reg, date):
        return re.match(reg, date)
    return None


def phone_match(phone):
    phone_format = "(13\d|14[579]|15[^4\D]|17[^49\D]|18\d)\d{8}"
    reg = re.compile(phone_format)
    if re.match(reg, phone):
        return re.match(reg, phone)
    return None


def name_match(name):
    name_format = "^[\u4e00-\u9fa5]+(·[\u4e00-\u9fa5]+)*$"
    reg = re.compile(name_format)
    if re.search(reg, name):
        return re.search(reg, name)
    return None


def handwriting_match(tokens):
    handwriting_result = {'name': None, 'phone': None, 'id': None, 'date': None, 'others': ''}
    for token in tokens:
        if handwriting_result['name'] is None and (not name_match(token) is None):
            handwriting_result['name'] = name_match(token)
            continue
        elif handwriting_result['phone'] is None and not phone_match(token) is None:
            handwriting_result['phone'] = phone_match(token)
            continue
        elif handwriting_result['id'] is None and not id_match(token) is None:
            handwriting_result['id'] = id_match(token)
            continue
        elif handwriting_result['date'] is None and not date_match(token) is None:
            handwriting_result['date'] = date_match(token)
        else:
            handwriting_result['others'] = handwriting_result['others'] + token
    return handwriting_result


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


# TODO: 交易选择路径（已完成未融合到test_zzx.py）
business_card_img = None
bankcard_img = None
business_license_img = None
invoice_img = None
general_basic_img = None
def select_path_for_trade(path_name, btn: Button, ocr_type: OCR):
    path = askopenfilenames(filetypes=[("all", "*.*")])
    path_name.set(path)

    # 处理图片
    name = path_to_list(path_name.get())[0]

    # TODO: 显示图片
    size = 175
    if ocr_type == OCR.BUSINESS_CARD:
        global business_card_img
        business_card_img = put_image(name, size)
        btn.config(state=NORMAL, image=business_card_img, width=size, height=size)
    elif ocr_type == OCR.BANKCARD:
        global bankcard_img
        bankcard_img = put_image(name, size)
        btn.config(state=NORMAL, image=bankcard_img, width=size, height=size)
    elif ocr_type == OCR.BUSINESS_LICENSE:
        global business_license_img
        business_license_img = put_image(name, size)
        btn.config(state=NORMAL, image=business_license_img, width=size, height=size)
    elif ocr_type == OCR.INVOICE:
        global invoice_img
        invoice_img = put_image(name, size)
        btn.config(state=NORMAL, image=invoice_img, width=size, height=size)
    elif ocr_type == OCR.GENERAL_BASIC:
        global general_basic_img
        general_basic_img = put_image(name, size)
        btn.config(state=NORMAL, image=general_basic_img, width=size, height=size)


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


def upload(photo_area, pathname, num_photo, comb_value):
    photo_area.delete(ALL)
    imagelist.clear()
    resultlist.clear()
    small_imagelist.clear()

    # fns = root.tk.splitlist(pathname.get())
    # print(repr(fns))
    num_photo.set(len(path_to_list(pathname.get())))
    namelist = path_to_list(pathname.get())
    if num_photo.get() == 0:
        warning_box = messagebox.showwarning("提示", "图片不为空！")
        return
        # num_photo.set(len(fns))
    # namelist = getName(fns)

    # TODO 先确认再存入
    count = 0
    for name in namelist:
        if comb_value.get() == "普通文本":
            result = ocr_general_basic(name)
        elif comb_value.get() == "名片":
            result = ocr_business_card(name)
        elif comb_value.get() == "营业执照":
            result = ocr_business_license(name)
        elif comb_value.get() == "银行卡":
            result = ocr_bankcard(name)
        elif comb_value.get() == "发票":
            result = ocr_invoice(name)
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
    confirm_window(num_photo, namelist, root)

    for result in resultlist:
        if comb_value.get() == "名片":
            sql_insert(OCR.BUSINESS_CARD, result)
        elif comb_value.get() == "银行卡":
            sql_insert(OCR.BANKCARD, result)
        elif comb_value.get() == "发票":
            sql_insert(OCR.INVOICE, result)
        elif comb_value.get() == "营业执照":
            sql_insert(OCR.BUSINESS_LICENSE, result)
        elif comb_value.get() == "其他信息":
            sql_insert(OCR.GENERAL_BASIC, result)


business_list = []
card_list = []
license_list = []
invoice_list = []
general_list = []

ocr_final_result = {}


def confirm_single(name, parent, ocr_type: OCR):
    # TODO: show_large_pic 已删除

    fns = root.tk.splitlist(name)
    namelist = path_to_list(name)
    name = namelist[0]

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
    photo_canv.grid(row=0, column=0, columnspan=3, rowspan=40)

    if ocr_type == OCR.BUSINESS_CARD:
        business_list.append(photo_single)
        '''business_image_btn = Button(parent,
                                    command=lambda: show_large_pic(name, parent),
                                    image=business_list[-1])'''
        photo_canv.create_image(5, 5, image=business_list[-1], anchor=NW)
    elif ocr_type == OCR.BANKCARD:
        card_list.append(photo_single)
        '''business_image_btn = Button(parent,
                                    command=lambda: show_large_pic(name, parent),
                                    image=card_list[-1])'''
        photo_canv.create_image(5, 5, image=card_list[-1], anchor=NW)
    elif ocr_type == OCR.BUSINESS_LICENSE:
        license_list.append(photo_single)
        '''business_image_btn = Button(parent,
                                    command=lambda: show_large_pic(name, parent),
                                    image=license_list[-1])'''
        photo_canv.create_image(5, 5, image=license_list[-1], anchor=NW)
    elif ocr_type == OCR.INVOICE:
        invoice_list.append(photo_single)
        '''business_image_btn = Button(parent,
                                    command=lambda: show_large_pic(name, parent),
                                    image=invoice_list[-1])'''
        photo_canv.create_image(5, 5, image=invoice_list[-1], anchor=NW)
    elif ocr_type == OCR.GENERAL_BASIC:
        general_list.append(photo_single)
        '''business_image_btn = Button(parent,
                                    command=lambda: show_large_pic(name, parent),
                                    image=general_list[-1])'''
        photo_canv.create_image(5, 5, image=general_list[-1], anchor=NW)

    if ocr_type == OCR.BUSINESS_CARD:
        offset = 13
        result = ocr_business_card(name)
        v_name = StringVar()
        v_name.set(result['name'])
        v_title = StringVar()
        v_title.set(result['title'])
        v_company = StringVar()
        v_company.set(result['company'])
        v_addr = StringVar()
        v_addr.set(result['addr'])
        v_mobile = StringVar()
        v_mobile.set(result['mobile'])
        v_fax = StringVar()
        v_fax.set(result['fax'])
        v_tel = StringVar()
        v_tel.set(result['tel'])
        v_email = StringVar()
        v_email.set(result['email'])
        v_url = StringVar()
        v_url.set(result['url'])

        text_name = Label(cf_wd, text="姓名:", width=10, font=myfont)
        text_name.grid(row=0 + offset, column=4)
        text_title = Label(cf_wd, text="职位:", width=10, font=myfont)
        text_title.grid(row=0 + offset, column=7)
        text_company = Label(cf_wd, text="公司:", width=10, font=myfont)
        text_company.grid(row=1 + offset, column=4)
        text_addr = Label(cf_wd, text="地址:", width=10, font=myfont)
        text_addr.grid(row=2 + offset, column=4)
        text_mobile = Label(cf_wd, text="手机:", width=10, font=myfont)
        text_mobile.grid(row=3 + offset, column=4)
        text_fax = Label(cf_wd, text="传真:", width=10, font=myfont)
        text_fax.grid(row=3 + offset, column=7)
        text_tel = Label(cf_wd, text="固话:", width=10, font=myfont)
        text_tel.grid(row=4 + offset, column=4)
        text_email = Label(cf_wd, text="E-mail:", width=10, font=myfont)
        text_email.grid(row=4 + offset, column=7)
        text_url = Label(cf_wd, text="网址:", width=10, font=myfont)
        text_url.grid(row=5 + offset, column=4)

        entry_name = Entry(cf_wd, textvariable=v_name, font=myfont)
        entry_name.grid(row=0 + offset, column=5)
        entry_title = Entry(cf_wd, textvariable=v_title, font=myfont)
        entry_title.grid(row=0 + offset, column=8)
        entry_company = Entry(cf_wd, textvariable=v_company, width=52, font=myfont)
        entry_company.grid(row=1 + offset, column=5, columnspan=4)
        entry_addr = Entry(cf_wd, textvariable=v_addr, width=52, font=myfont)
        entry_addr.grid(row=2 + offset, column=5, columnspan=4)
        entry_mobile = Entry(cf_wd, textvariable=v_mobile, font=myfont)
        entry_mobile.grid(row=3 + offset, column=5)
        entry_fax = Entry(cf_wd, textvariable=v_fax, font=myfont)
        entry_fax.grid(row=3 + offset, column=8)
        entry_tel = Entry(cf_wd, textvariable=v_tel, font=myfont)
        entry_tel.grid(row=4 + offset, column=5)
        entry_email = Entry(cf_wd, textvariable=v_email, font=myfont)
        entry_email.grid(row=4 + offset, column=8)
        entry_url = Entry(cf_wd, textvariable=v_url, width=52, font=myfont)
        entry_url.grid(row=5 + offset, column=5, columnspan=4)

        def confirm_business_card():
            item = 'business_card'
            ocr_final_result[item] = {}
            ocr_final_result[item]['name'] = entry_name.get()
            ocr_final_result[item]['title'] = entry_title.get()
            ocr_final_result[item]['company'] = entry_company.get()
            ocr_final_result[item]['addr'] = entry_addr.get()
            ocr_final_result[item]['mobile'] = entry_mobile.get()
            ocr_final_result[item]['fax'] = entry_fax.get()
            ocr_final_result[item]['tel'] = entry_tel.get()
            ocr_final_result[item]['email'] = entry_email.get()
            ocr_final_result[item]['url'] = entry_url.get()
            with open(name, "rb") as f:
                ocr_final_result[item]['picture'] = base64.b64encode(f.read())

            cf_wd.destroy()

        btn_confirm = Button(cf_wd, text="确认信息", command=lambda: confirm_business_card(), relief=GROOVE, font=myfont)
        btn_confirm.grid(row=40, column=5)

    elif ocr_type == OCR.BANKCARD:
        offset = 14
        result = ocr_bankcard(name)
        v_bank_card_number = StringVar()
        v_bank_card_number.set(result['bank_card_number'])
        v_bank_name = StringVar()
        v_bank_name.set(result['bank_name'])
        v_bank_card_type = StringVar()
        v_bank_card_type.set(result['bank_card_type'])
        v_valid_date = StringVar()
        v_valid_date.set(result['valid_date'])

        text_bank_card_number = Label(cf_wd, text="银行卡号:", width=10, font=myfont)
        text_bank_card_number.grid(row=0 + offset, column=4)
        text_bank_name = Label(cf_wd, text="银行名称:", width=10, font=myfont)
        text_bank_name.grid(row=1 + offset, column=4)
        text_bank_card_type = Label(cf_wd, text="卡类型:", width=10, font=myfont)
        text_bank_card_type.grid(row=2 + offset, column=4)
        text_valid_date = Label(cf_wd, text="有效期:", width=10, font=myfont)
        text_valid_date.grid(row=3 + offset, column=4)

        entry_bank_card_number = Entry(cf_wd, textvariable=v_bank_card_number, width=30, font=myfont)
        entry_bank_card_number.grid(row=0 + offset, column=5, columnspan=4)
        entry_bank_name = Entry(cf_wd, textvariable=v_bank_name, width=30, font=myfont)
        entry_bank_name.grid(row=1 + offset, column=5, columnspan=4)
        entry_bank_card_type = Entry(cf_wd, textvariable=v_bank_card_type, width=30, font=myfont)
        entry_bank_card_type.grid(row=2 + offset, column=5, columnspan=4)
        entry_valid_date = Entry(cf_wd, textvariable=v_valid_date, width=30, font=myfont)
        entry_valid_date.grid(row=3 + offset, column=5, columnspan=4)

        def confirm_bankcard():
            item = 'bankcard'
            ocr_final_result[item] = {}
            ocr_final_result[item]['bank_card_number'] = entry_bank_card_number.get()
            ocr_final_result[item]['bank_name'] = entry_bank_name.get()
            ocr_final_result[item]['bank_card_type'] = entry_bank_card_type.get()
            ocr_final_result[item]['valid_date'] = entry_valid_date.get()
            with open(name, "rb") as f:
                ocr_final_result[item]['picture'] = base64.b64encode(f.read())

            cf_wd.destroy()

        btn_confirm = Button(cf_wd, text="确认信息", command=lambda: confirm_bankcard(), relief=GROOVE, font=myfont)
        btn_confirm.grid(row=40, column=5)

    elif ocr_type == OCR.BUSINESS_LICENSE:
        offset = 0
        result = ocr_business_license(name)
        v_company_name = StringVar()
        v_company_name.set(result['company_name'])
        v_legal_person = StringVar()
        v_legal_person.set(result['legal_person'])
        v_license_id = StringVar()
        v_license_id.set(result['license_id'])
        v_social_credit_number = StringVar()
        v_social_credit_number.set(result['social_credit_number'])
        v_establishment_date = StringVar()
        v_establishment_date.set(result['establishment_date'])
        v_expiration_date = StringVar()
        v_expiration_date.set(result['expiration_date'])
        v_registered_capital = StringVar()
        v_registered_capital.set(result['registered_capital'])
        v_addr = StringVar()
        v_addr.set(result['addr'])
        v_business_scope = StringVar()
        v_business_scope.set(result['business_scope'])

        text_company_name = Label(cf_wd, text="公司名称:", width=10, font=myfont)
        text_company_name.grid(row=0 + offset, column=4)
        text_legal_person = Label(cf_wd, text="法人:", width=10, font=myfont)
        text_legal_person.grid(row=1 + offset, column=4)
        text_license_id = Label(cf_wd, text="证书号:", width=10, font=myfont)
        text_license_id.grid(row=1 + offset, column=6)
        text_social_credit_number = Label(cf_wd, text="信用代码:", width=10, font=myfont)
        text_social_credit_number.grid(row=2 + offset, column=4)
        text_establishment_date = Label(cf_wd, text="成立日期:", width=10, font=myfont)
        text_establishment_date.grid(row=3 + offset, column=4)
        text_expiration_date = Label(cf_wd, text="有效期:", width=10, font=myfont)
        text_expiration_date.grid(row=3 + offset, column=6)
        text_registered_capital = Label(cf_wd, text="注册资本:", width=10, font=myfont)
        text_registered_capital.grid(row=4 + offset, column=4)
        text_addr = Label(cf_wd, text="地址:", width=10, font=myfont)
        text_addr.grid(row=5 + offset, column=4)
        text_business_scope = Label(cf_wd, text="经营范围:", width=10, font=myfont)
        text_business_scope.grid(row=6 + offset, column=4)

        entry_company_name = Entry(cf_wd, textvariable=v_company_name, width=52, font=myfont)
        entry_company_name.grid(row=0 + offset, column=5, columnspan=4)
        entry_legal_person = Entry(cf_wd, textvariable=v_legal_person, font=myfont)
        entry_legal_person.grid(row=1 + offset, column=5)
        entry_license_id = Entry(cf_wd, textvariable=v_license_id, font=myfont)
        entry_license_id.grid(row=1 + offset, column=7)
        entry_social_credit_number = Entry(cf_wd, textvariable=v_social_credit_number, width=52, font=myfont)
        entry_social_credit_number.grid(row=2 + offset, column=5, columnspan=4)
        entry_establishment_date = Entry(cf_wd, textvariable=v_establishment_date, font=myfont)
        entry_establishment_date.grid(row=3 + offset, column=5)
        entry_expiration_date = Entry(cf_wd, textvariable=v_expiration_date, font=myfont)
        entry_expiration_date.grid(row=3 + offset, column=7)
        entry_registered_capital = Entry(cf_wd, textvariable=v_registered_capital, width=52, font=myfont)
        entry_registered_capital.grid(row=4 + offset, column=5, columnspan=4)
        entry_addr = Entry(cf_wd, textvariable=v_addr, width=52, font=myfont)
        entry_addr.grid(row=5 + offset, column=5, columnspan=4)
        entry_business_scope = Entry(cf_wd, textvariable=v_business_scope, width=52, font=myfont)
        entry_business_scope.grid(row=6 + offset, column=5, columnspan=4)

        def confirm_business_license():
            item = 'business_license'
            ocr_final_result[item] = {}
            ocr_final_result[item]['company_name'] = entry_company_name.get()
            ocr_final_result[item]['legal_person'] = entry_legal_person.get()
            ocr_final_result[item]['license_id'] = entry_license_id.get()
            ocr_final_result[item]['social_credit_number'] = entry_social_credit_number.get()
            ocr_final_result[item]['establishment_date'] = entry_establishment_date.get()
            ocr_final_result[item]['expiration_date'] = entry_expiration_date.get()
            ocr_final_result[item]['registered_capital'] = entry_registered_capital.get()
            ocr_final_result[item]['addr'] = entry_addr.get()
            ocr_final_result[item]['business_scope'] = entry_business_scope.get()
            with open(name, "rb") as f:
                ocr_final_result[item]['picture'] = base64.b64encode(f.read())

            cf_wd.destroy()

        btn_confirm = Button(cf_wd, text="确认信息", command=lambda: confirm_business_license(), relief=GROOVE, font=myfont)
        btn_confirm.grid(row=40, column=5)

    elif ocr_type == OCR.INVOICE:
        offset = 0
        result = ocr_invoice(name)
        v_invoice_type = StringVar()  # 发票种类
        v_invoice_type.set(result['invoice_type'])
        v_invoice_code = StringVar()  # 发票代码
        v_invoice_code.set(result['invoice_code'])
        v_invoice_num = StringVar()  # 发票号码
        v_invoice_num.set(result['invoice_num'])
        v_invoice_date = StringVar()  # 开票日期
        v_invoice_date.set(result['invoice_date'])
        v_purchaser_name = StringVar()  # 购买方名称
        v_purchaser_name.set(result['purchaser_name'])
        v_purchaser_register_num = StringVar()  # 购买方纳税人识别号
        v_purchaser_register_num.set(result['purchaser_register_num'])
        v_seller_name = StringVar()  # 销售方名称
        v_seller_name.set(result['seller_name'])
        v_seller_register_num = StringVar()  # 销售方纳税人识别号
        v_seller_register_num.set(result['seller_register_num'])
        v_seller_addr = StringVar()  # 销售方地址电话
        v_seller_addr.set(result['seller_addr'])
        v_seller_bank = StringVar()  # 销售方开户行及账号
        v_seller_bank.set(result['seller_bank'])
        '''
        v_commodity_name = StringVar()          # 货物名称 多行
        v_commodity_type = StringVar()          # 规格型号 多行
        v_commodity_num = StringVar()           # 数量 多行
        v_commodity_price = StringVar()         # 单价 多行
        v_commodity_amount = StringVar()        # 金额 多行
        v_commodity_tax_rate = StringVar()      # 税率 多行
        v_commodity_tax = StringVar()           # 税额 多行
        '''
        v_amount_in_figures = StringVar()  # 价格合计
        v_amount_in_figures.set(result['amount_in_figures'])

        text_invoice_type = Label(cf_wd, text="发票种类:", font=myfont)
        text_invoice_type.grid(row=0 + offset, column=4)
        text_invoice_code = Label(cf_wd, text="发票代码:", font=myfont)
        text_invoice_code.grid(row=0 + offset, column=6)
        text_invoice_num = Label(cf_wd, text="发票号码:", font=myfont)
        text_invoice_num.grid(row=1 + offset, column=4)
        text_invoice_date = Label(cf_wd, text="开票日期:", font=myfont)
        text_invoice_date.grid(row=1 + offset, column=6)
        text_purchaser = Label(cf_wd, text="购买方信息:", font=myfont)
        text_purchaser.grid(row=2 + offset, column=4)
        text_purchaser_name = Label(cf_wd, text="名称:", font=myfont)
        text_purchaser_name.grid(row=3 + offset, column=4)
        text_purchaser_register_num = Label(cf_wd, text="纳税人\n识别号:", font=myfont)
        text_purchaser_register_num.grid(row=3 + offset, column=6)
        text_seller = Label(cf_wd, text="销售方信息:", font=myfont)
        text_seller.grid(row=4 + offset, column=4)
        text_seller_name = Label(cf_wd, text="名称:", width=10, font=myfont)
        text_seller_name.grid(row=5 + offset, column=4)
        text_seller_register_num = Label(cf_wd, text="纳税人\n识别号:", width=10, font=myfont)
        text_seller_register_num.grid(row=5 + offset, column=6)
        text_seller_addr = Label(cf_wd, text="地址:", width=10, font=myfont)
        text_seller_addr.grid(row=6 + offset, column=4)
        text_seller_bank = Label(cf_wd, text="银行:", width=10, font=myfont)
        text_seller_bank.grid(row=6 + offset, column=6)
        text_amount_in_figures = Label(cf_wd, text="价格合计(元):", font=myfont)
        text_amount_in_figures.grid(row=10 + offset, column=4)

        entry_invoice_type = Entry(cf_wd, textvariable=v_invoice_type, font=myfont)
        entry_invoice_type.grid(row=0 + offset, column=5)
        entry_invoice_code = Entry(cf_wd, textvariable=v_invoice_code, font=myfont)
        entry_invoice_code.grid(row=0 + offset, column=7)
        entry_invoice_num = Entry(cf_wd, textvariable=v_invoice_num, font=myfont)
        entry_invoice_num.grid(row=1 + offset, column=5)
        entry_invoice_date = Entry(cf_wd, textvariable=v_invoice_date, font=myfont)
        entry_invoice_date.grid(row=1 + offset, column=7)
        entry_purchaser_name = Entry(cf_wd, textvariable=v_purchaser_name, font=myfont)
        entry_purchaser_name.grid(row=3 + offset, column=5)
        entry_purchaser_register_num = Entry(cf_wd, textvariable=v_purchaser_register_num, font=myfont)
        entry_purchaser_register_num.grid(row=3 + offset, column=7)
        entry_seller_name = Entry(cf_wd, textvariable=v_seller_name, font=myfont)
        entry_seller_name.grid(row=5 + offset, column=5)
        entry_seller_register_num = Entry(cf_wd, textvariable=v_seller_register_num, font=myfont)
        entry_seller_register_num.grid(row=5 + offset, column=7)
        entry_seller_addr = Entry(cf_wd, textvariable=v_seller_addr, font=myfont)
        entry_seller_addr.grid(row=6 + offset, column=5)
        entry_seller_bank = Entry(cf_wd, textvariable=v_seller_bank, font=myfont)
        entry_seller_bank.grid(row=6 + offset, column=7)

        tree = ttk.Treeview(cf_wd,
                            show="headings",
                            columns=('commodity_name',
                                     'commodity_type',
                                     'commodity_num',
                                     'commodity_price',
                                     'commodity_amount',
                                     'commodity_tax_rate',
                                     'commodity_tax')
                            , selectmode=BROWSE, height=5)
        tree.heading("commodity_name", text="货物名称")
        tree.column("commodity_name", minwidth=0, width=100, stretch=NO)
        tree.heading("commodity_type", text="规格型号")
        tree.column("commodity_type", minwidth=0, width=100, stretch=NO)
        tree.heading("commodity_num", text="数量")
        tree.column("commodity_num", minwidth=0, width=50, stretch=NO)
        tree.heading("commodity_price", text="单价")
        tree.column("commodity_price", minwidth=0, width=100, stretch=NO)
        tree.heading("commodity_amount", text="金额")
        tree.column("commodity_amount", minwidth=0, width=100, stretch=NO)
        tree.heading("commodity_tax_rate", text="税率")
        tree.column("commodity_tax_rate", minwidth=0, width=50, stretch=NO)
        tree.heading("commodity_tax", text="税额")
        tree.column("commodity_tax", minwidth=0, width=100, stretch=NO)

        for i in range(len(result['commodity_name'])):
            tree.insert('', i, values=(result['commodity_name'][i]['word'],
                                       result['commodity_type'][i]['word'],
                                       result['commodity_num'][i]['word'],
                                       result['commodity_price'][i]['word'],
                                       result['commodity_amount'][i]['word'],
                                       result['commodity_tax_rate'][i]['word'],
                                       result['commodity_tax'][i]['word'],))
        tree.grid(row=7 + offset, column=4, columnspan=4)

        entry_amount_in_figures = Entry(cf_wd, textvariable=v_amount_in_figures, font=myfont)
        entry_amount_in_figures.grid(row=10 + offset, column=5)

        def confirm_invoice():
            item = 'invoice'
            ocr_final_result[item] = {}
            ocr_final_result[item]['invoice_type'] = entry_invoice_type.get()
            ocr_final_result[item]['invoice_code'] = entry_invoice_code.get()
            ocr_final_result[item]['invoice_num'] = entry_invoice_num.get()
            ocr_final_result[item]['invoice_date'] = entry_invoice_date.get()
            ocr_final_result[item]['purchaser_name'] = entry_purchaser_name.get()
            ocr_final_result[item]['purchaser_register_num'] = entry_purchaser_register_num.get()
            ocr_final_result[item]['seller_name'] = entry_seller_name.get()
            ocr_final_result[item]['seller_register_num'] = entry_seller_register_num.get()
            ocr_final_result[item]['seller_addr'] = entry_seller_addr.get()
            ocr_final_result[item]['seller_bank'] = entry_seller_bank.get()
            ocr_final_result[item]['amount_in_figures'] = entry_amount_in_figures.get()
            with open(name, "rb") as f:
                ocr_final_result[item]['picture'] = base64.b64encode(f.read())

            ocr_final_result[item]['commodity'] = {}
            ocr_final_result[item]['commodity']['name'] = []
            ocr_final_result[item]['commodity']['type'] = []
            ocr_final_result[item]['commodity']['num'] = []
            ocr_final_result[item]['commodity']['price'] = []
            ocr_final_result[item]['commodity']['amount'] = []
            ocr_final_result[item]['commodity']['tax_rate'] = []
            ocr_final_result[item]['commodity']['tax'] = []

            for children in tree.get_children():
                info = tree.item(children, 'values')
                ocr_final_result[item]['commodity']['name'].append(info[0])
                ocr_final_result[item]['commodity']['type'].append(info[1])
                ocr_final_result[item]['commodity']['num'].append(info[2])
                ocr_final_result[item]['commodity']['price'].append(info[3])
                ocr_final_result[item]['commodity']['amount'].append(info[4])
                ocr_final_result[item]['commodity']['tax_rate'].append(info[5])
                ocr_final_result[item]['commodity']['tax'].append(info[6])

            cf_wd.destroy()

        btn_confirm = Button(cf_wd, text="确认信息", command=lambda: confirm_invoice(), relief=GROOVE, font=myfont)
        btn_confirm.grid(row=40, column=5)

    elif ocr_type == OCR.GENERAL_BASIC:
        offset = 0
        result = ocr_general_basic(name)
        v_remark = StringVar()
        content = result['content']
        text_remark = Label(cf_wd, text="备注:", width=10, font=myfont)
        text_remark.grid(row=0 + offset, column=4)
        text_content = Label(cf_wd, text="内容:", width=10, font=myfont)
        text_content.grid(row=1 + offset, column=4)

        entry_remark = Entry(cf_wd, textvariable=v_remark, width=40, font=myfont)
        entry_remark.grid(row=0 + offset, column=5, columnspan=4)
        entry_content = Text(cf_wd, width=40, height=17, font=myfont)
        entry_content.insert('end', content)
        entry_content.grid(row=1 + offset, column=5, columnspan=4)

        def confirm_general_basic():
            item = 'general_basic'
            ocr_final_result[item] = {}
            ocr_final_result[item]['remark'] = entry_remark.get()
            ocr_final_result[item]['content'] = entry_content.get('0.0', 'end')
            with open(name, "rb") as f:
                ocr_final_result[item]['picture'] = base64.b64encode(f.read())

            cf_wd.destroy()

        btn_confirm = Button(cf_wd, text="确认信息", command=lambda: confirm_general_basic(), relief=GROOVE, font=myfont)
        btn_confirm.grid(row=40, column=5)

    # TODO: 此函数下方的所有内容均已删除


def confirm_window(num_photo, namelist, parent):
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
    trade_wd = Toplevel(root, bg='#f8ffff', )
    size = 200
    results = StringVar()
    button_list = []
    upload_image = Image.open("上传.jpg")
    upload_photo = ImageTk.PhotoImage(upload_image)
    button_list.append(upload_photo)

    edit_image = Image.open("编辑.jpg")
    edit_photo = ImageTk.PhotoImage(edit_image)
    button_list.append(edit_photo)

    license_image = Image.open("执照.jpg")  # 2
    license_photo = ImageTk.PhotoImage(license_image)
    button_list.append(license_photo)

    business_card_image = Image.open("名片.jpg")  # 3
    business_card_photo = ImageTk.PhotoImage(business_card_image)
    button_list.append(business_card_photo)

    card_image = Image.open("银行卡.jpg")  # 4
    card_photo = ImageTk.PhotoImage(card_image)
    button_list.append(card_photo)

    invoice_image = Image.open("发票.jpg")  # 5
    invoice_photo = ImageTk.PhotoImage(invoice_image)
    button_list.append(invoice_photo)

    other_image = Image.open("其他.jpg")  # 6
    other_photo = ImageTk.PhotoImage(other_image)
    button_list.append(other_photo)

    confirm_image = Image.open("确认.jpg")  # 7
    confirm_photo = ImageTk.PhotoImage(confirm_image)
    button_list.append(confirm_photo)

    business_path = StringVar()

    frame_businesscard = Frame(trade_wd, bg='#f8ffff', height=208, width=635, bd=1, relief='groove')
    frame_businesscard.grid(row=0, column=0, columnspan=5)

    businesscard_edit = Button(frame_businesscard, bg='white', image=button_list[1], command=lambda: select_path(),
                               relief=FLAT)
    businesscard_edit.place(relx=0.34, rely=0.65)

    businesscard_upload = Button(frame_businesscard, bg='#f8ffff', image=button_list[0],
                                 command=lambda: confirm_single(business_path.get(), frame_businesscard,
                                                                OCR.BUSINESS_CARD),
                                 relief=FLAT)
    businesscard_upload.place(relx=0.58, rely=0.65)

    business_entry = Entry(frame_businesscard, textvariable=business_path, width=25)
    business_entry.place(relx=0.41, rely=0.35)

    business_canv = Canvas(frame_businesscard, bg='#f8ffff', bd=1, width=200, height=200)
    business_canv.place(relx=0, rely=0)

    businesscard_btn = Button(frame_businesscard, bg='#f8ffff', image=button_list[3],
                              command=lambda: select_path_for_trade(path_name=business_path,
                                                                    btn=btn_business_card_image,
                                                                    ocr_type=OCR.BUSINESS_CARD),
                              relief=FLAT, font="宋体 12")
    businesscard_btn.place(relx=0.74, rely=0.3)

    # -----------营业执照
    license_path = StringVar()

    frame_license = Frame(trade_wd, bg='#f8ffff', height=208, width=635, bd=1, relief='groove')
    frame_license.grid(row=1, column=0, columnspan=5)

    license_edit = Button(frame_license, bg='#f8ffff', image=button_list[1], command=lambda: select_path(), relief=FLAT)
    license_edit.place(relx=0.34, rely=0.65)

    license_upload = Button(frame_license, image=button_list[0], bg='#f8ffff',
                            command=lambda: confirm_single(license_path.get(), frame_license, OCR.BUSINESS_LICENSE),
                            relief=FLAT)
    license_upload.place(relx=0.58, rely=0.65)

    license_entry = Entry(frame_license, textvariable=license_path, width=25)
    license_entry.place(relx=0.41, rely=0.35)

    license_canv = Canvas(frame_license, bg='#f8ffff', bd=1, width=200, height=200)
    license_canv.place(relx=0, rely=0)

    license_btn = Button(frame_license, image=button_list[2], bg='#f8ffff',
                         command=lambda: select_path_for_trade(path_name=license_path,
                                                               btn=btn_business_license_image,
                                                               ocr_type=OCR.BUSINESS_LICENSE),
                         relief=FLAT)
    license_btn.place(relx=0.74, rely=0.3)
    # -----------通用文本
    general_path = StringVar()

    frame_general = Frame(trade_wd, bg='#f8ffff', height=208, width=635, bd=1, relief='groove')
    frame_general.grid(row=2, column=0, columnspan=5)

    general_edit = Button(frame_general, bg='#f8ffff', image=button_list[1], command=lambda: select_path(), relief=FLAT)
    general_edit.place(relx=0.34, rely=0.65)

    general_upload = Button(frame_general, bg='#f8ffff', image=button_list[0],
                            command=lambda: confirm_single(general_path.get(), frame_general, OCR.GENERAL_BASIC),
                            relief=FLAT)
    general_upload.place(relx=0.58, rely=0.65)

    general_entry = Entry(frame_general, textvariable=general_path, width=25)
    general_entry.place(relx=0.41, rely=0.35)

    general_canv = Canvas(frame_general, bg='#f8ffff', bd=1, width=200, height=200)
    general_canv.place(relx=0, rely=0)

    general_btn = Button(frame_general, bg='#f8ffff', image=button_list[6],
                         command=lambda: select_path_for_trade(path_name=general_path,
                                                               btn=btn_general_basic_image,
                                                               ocr_type=OCR.GENERAL_BASIC),
                         relief=FLAT)
    general_btn.place(relx=0.74, rely=0.3)

    # -----------银行卡
    card_path = StringVar()

    frame_card = Frame(trade_wd, bg='#f8ffff', height=208, width=635, bd=1, relief='groove')
    frame_card.grid(row=0, column=5, columnspan=5)

    card_edit = Button(frame_card, bg='#f8ffff', image=button_list[1], command=lambda: select_path(), relief=FLAT)
    card_edit.place(relx=0.34, rely=0.65)

    card_upload = Button(frame_card, bg='#f8ffff', image=button_list[0],
                         command=lambda: confirm_single(card_path.get(), frame_card, OCR.BANKCARD),
                         relief=FLAT)
    card_upload.place(relx=0.58, rely=0.65)

    card_entry = Entry(frame_card, textvariable=card_path, width=25)
    card_entry.place(relx=0.41, rely=0.35)

    card_canv = Canvas(frame_card, bg='#f8ffff', bd=1, width=200, height=200)
    card_canv.place(relx=0, rely=0)

    card_btn = Button(frame_card, image=button_list[4], bg='#f8ffff',
                      command=lambda: select_path_for_trade(path_name=card_path,
                                                            btn=btn_bankcard_image,
                                                            ocr_type=OCR.BANKCARD),
                      relief=FLAT)
    card_btn.place(relx=0.74, rely=0.3)

    # -----------发票
    invoice_path = StringVar()

    frame_invoice = Frame(trade_wd, bg='#f8ffff', height=208, width=635, bd=1, relief='groove')
    frame_invoice.grid(row=1, column=5, columnspan=5)

    invoice_edit = Button(frame_invoice, bg='#f8ffff', image=button_list[1], command=lambda: select_path(), relief=FLAT)
    invoice_edit.place(relx=0.34, rely=0.65)

    invoice_upload = Button(frame_invoice, bg='#f8ffff', image=button_list[0],
                            command=lambda: confirm_single(invoice_path.get(), frame_invoice, OCR.INVOICE),
                            relief=FLAT)
    invoice_upload.place(relx=0.58, rely=0.65)

    invoice_entry = Entry(frame_invoice, textvariable=invoice_path, width=25)
    invoice_entry.place(relx=0.41, rely=0.35)

    invoice_canv = Canvas(frame_invoice, bg='#f8ffff', bd=1, width=200, height=200)
    invoice_canv.place(relx=0, rely=0)

    invoice_btn = Button(frame_invoice, bg='#f8ffff', image=button_list[5],
                         command=lambda: select_path_for_trade(path_name=invoice_path,
                                                               btn=btn_invoice_image,
                                                               ocr_type=OCR.INVOICE),
                         relief=FLAT)
    invoice_btn.place(relx=0.74, rely=0.3)

    # TODO: 统一管理小图按钮（已完成，未融合至test_zzx）
    btn_business_card_image = Button(frame_businesscard, width=24, height=10,
                                     command=lambda: ps(business_entry),
                                     state=DISABLED, relief=GROOVE)
    btn_business_card_image.place(relx=0.02, rely=0.05)

    btn_bankcard_image = Button(frame_card, width=24, height=10,
                                command=lambda: ps(card_entry),
                                image=None, state=DISABLED, relief=GROOVE)
    btn_bankcard_image.place(relx=0.02, rely=0.05)

    btn_business_license_image = Button(frame_license, width=24, height=10,
                                        command=lambda: ps(license_entry),
                                        image=None, state=DISABLED, relief=GROOVE)
    btn_business_license_image.place(relx=0.02, rely=0.05)

    btn_invoice_image = Button(frame_invoice, width=24, height=10,
                               command=lambda: ps(invoice_entry),
                               image=None, state=DISABLED, relief=GROOVE)
    btn_invoice_image.place(relx=0.02, rely=0.05)

    btn_general_basic_image = Button(frame_general, width=24, height=10,
                                     command=lambda: ps(general_entry),
                                     image=None, state=DISABLED, relief=GROOVE)
    btn_general_basic_image.place(relx=0.02, rely=0.05)



    v_transaction_name = StringVar()

    frame_confirm = Frame(trade_wd, bg='#f8ffff', bd=1, height=200, width=5000, relief=FLAT)
    frame_confirm.grid(row=2, column=5, columnspan=5, rowspan=5)

    label_transaction_name = Label(frame_confirm, text="交易名称:", font="宋体 12", bg='#f8ffff')
    label_transaction_name.grid(row=3, column=2)

    entry_transaction_name = Entry(frame_confirm, width=25, textvariable=v_transaction_name)
    entry_transaction_name.grid(row=3, column=3)

    def store_confirm():
        if entry_transaction_name.get() != "":
            # 交易
            trans_content = {'name': entry_transaction_name.get()}
            sql_insert(OCR.TRANSACTION, trans_content)
            transaction_id = sql_conn('''SELECT max(id) FROM t_transaction''')[0][0]
            print(transaction_id)
            # 五项信息
            if ocr_final_result.__contains__('business_card'):
                ocr_final_result['business_card']['transaction_id'] = transaction_id
                sql_insert(OCR.BUSINESS_CARD, ocr_final_result['business_card'])
            if ocr_final_result.__contains__('bankcard'):
                ocr_final_result['bankcard']['transaction_id'] = transaction_id
                sql_insert(OCR.BANKCARD, ocr_final_result['bankcard'])
            if ocr_final_result.__contains__('business_license'):
                ocr_final_result['business_license']['transaction_id'] = transaction_id
                sql_insert(OCR.BUSINESS_LICENSE, ocr_final_result['business_license'])
            if ocr_final_result.__contains__('invoice'):
                ocr_final_result['invoice']['transaction_id'] = transaction_id
                sql_insert(OCR.INVOICE, ocr_final_result['invoice'])
            if ocr_final_result.__contains__('general_basic'):
                ocr_final_result['general_basic']['transaction_id'] = transaction_id
                sql_insert(OCR.GENERAL_BASIC, ocr_final_result['general_basic'])
            ocr_final_result.clear()

            trade_wd.destroy()
        else:
            print("Transaction name CANNOT be empty")

    btn_confirm = Button(frame_confirm, bg='#f8ffff', image=button_list[7],
                         command=lambda: store_confirm(), relief=FLAT)
    btn_confirm.grid(row=4, column=3)

    trade_wd.mainloop()


def delButton(tree):
    x = tree.get_children()
    for item in x:
        tree.delete(item)
    tree.heading('1', text='')
    tree.heading('2', text='')
    tree.heading('3', text='')
    tree.heading('4', text='')
    tree.heading('5', text='')
    tree.heading('6', text='')
    tree.heading('7', text='')
    tree.heading('8', text='')
    tree.heading('9', text='')


def search(parent, manage_comb_value, result_tree, str):
    delButton(result_tree)
    # delButton(result_tree)
    if manage_comb_value.get() == "交易":
        result_tree.column('1', width=200, anchor='center')

        result_tree.heading('1', text='交易名称')
        result_tree.heading('2', text='交易时间')
        result_dict = sql_query(OCR.TRANSACTION, str)

    elif manage_comb_value.get() == "普通文本":
        result_tree.column('1', width=200, anchor='center')
        result_tree.heading('1', text='内容')
        result_dict = sql_query(OCR.GENERAL_BASIC, str)

    elif manage_comb_value.get() == "执照":
        width = 100
        result_tree.column('1', width=width, anchor='center')
        result_tree.column('2', width=width, anchor='center')
        result_tree.column('3', width=width, anchor='center')
        result_tree.column('4', width=width, anchor='center')
        result_tree.column('5', width=width, anchor='center')
        result_tree.column('6', width=width, anchor='center')
        result_tree.column('7', width=width, anchor='center')
        result_tree.column('8', width=width, anchor='center')
        result_tree.column('9', width=width, anchor='center')

        result_tree.heading('1', text='公司名称')
        result_tree.heading('2', text='法人')
        result_tree.heading('3', text='证书号')
        result_tree.heading('4', text='信用代码')
        result_tree.heading('5', text='成立日期')
        result_tree.heading('6', text='有效期')
        result_tree.heading('7', text='注册资本')
        result_tree.heading('8', text='地址')
        result_tree.heading('9', text='经营范围')
        result_dict = sql_query(OCR.BUSINESS_LICENSE, str)

    elif manage_comb_value.get() == "名片":
        width = 100
        result_tree.column('1', width=width, anchor='center')
        result_tree.column('2', width=width, anchor='center')
        result_tree.column('3', width=width, anchor='center')
        result_tree.column('4', width=width, anchor='center')
        result_tree.column('5', width=width, anchor='center')
        result_tree.column('6', width=width, anchor='center')
        result_tree.column('7', width=width, anchor='center')
        result_tree.column('8', width=width, anchor='center')
        result_tree.column('9', width=width, anchor='center')

        result_tree.heading('1', text='姓名')
        result_tree.heading('2', text='职位')
        result_tree.heading('3', text='公司')
        result_tree.heading('4', text='地址')
        result_tree.heading('5', text='手机')
        result_tree.heading('6', text='固话')
        result_tree.heading('7', text='传真')
        result_tree.heading('8', text='Email')
        result_tree.heading('9', text='网址')
        result_dict = sql_query(OCR.BUSINESS_CARD, str)

        # for result_values in result_dict.values():

        # sql_conn()
    count = 0
    result_list = []
    for id in result_dict['id']:
        temp_list = []
        for value in result_dict.values():
            temp_list.append(value[count])
        count = count + 1
        result_list.append(temp_list[1:])
        # result_list.append(result_values[2:])
        # print(result_list)
        result_tree.insert('', 'end', values=temp_list[1:])
    result_tree.grid(row=1, rowspan=10, column=1, columnspan=6)


# TODO 上传空图片
def tree_click(tree):
    detail_wd = Toplevel()
    for item in tree.selection():
        item_text = tree.item(item, "values")


def manage():
    manage_wd = Toplevel(root)
    search_str = StringVar()
    manage_comb_value = StringVar()  # 窗体自带的文本，新建一个值
    manage_comb = ttk.Combobox(manage_wd, textvariable=manage_comb_value, state='readonly')  # 初始化
    result_tree = ttk.Treeview(manage_wd, columns=['1', '2', '3', '4', '5', '6', '7', '8', '9'], show='headings')
    result_tree.bind('<Double-1>', lambda event: tree_click(result_tree))

    search_btn = Button(manage_wd, text="搜索", width=11,
                        command=lambda: search(manage_wd, manage_comb_value, result_tree, search_str.get()),
                        relief=GROOVE)
    search_btn.grid(row=0, column=5)

    type_lable = Label(manage_wd, text="类型", width=8)
    type_lable.grid(row=0, column=1)

    manage_comb["values"] = ("普通文本", "名片", "执照", '交易')
    manage_comb.current(0)

    manage_comb.bind("<<ComboboxSelected>>", lambda event: func(manage_wd, value=manage_comb_value, tree=result_tree))

    manage_comb.grid(row=0, column=2),

    manage_entry = Entry(manage_wd, textvariable=search_str, width=25)
    manage_entry.grid(row=0, column=4)

    manage_wd.mainloop()


def upload_single():
    single_wd = Toplevel(root,bg='#f8ffff',)
    pathname = StringVar()

    single_canv = Canvas(single_wd, bd=1, width=1000, height=640)
    single_canv.pack()

    single_canv.create_image(0, 0, image=single_bg, anchor=NW)

    comb_value = StringVar()  # 窗体自带的文本，新建一个值
    comb = ttk.Combobox(single_wd, textvariable=comb_value, state='readonly',font="宋体 12")  # 初始化
    comb["values"] = ("普通文本", "名片", "营业执照", "银行卡", "发票")
    comb.current(0)

    upload_single_btn = Button(single_wd, bg='#e0f1ed',image=icon_list[0], command=lambda: select_path(pathname), relief=FLAT)
    upload_single_btn.place(relx=0.615,rely=0.162)
    # comb.bind("<<ComboboxSelected>>", func(manage_comb_value, result_tree))
    comb.place(relx=0.4,rely=0.18)

    scrollbar = Scrollbar(single_wd)
    num_photo = IntVar()
    photo_area = Canvas(single_wd, bd=1, width=500, height=300, relief=GROOVE, yscrollcommand=scrollbar.set,
                        scrollregion=(0, 0, 500, math.ceil(num_photo.get() / 2) * 200 + 500),bg='#f0fffe')
    photo_area.place(relx=0.25,rely=0.35)
    # photo_area.config(width=300, height=200)
    # photo_area.configure(scrollregion=photo_area.bbox('all'))

    scrollbar.config(command=photo_area.yview)
    scrollbar.place(relx=0.6,rely=0.4)

    path_entry = Entry(single_wd, textvariable=pathname, width=25,bg='#e0f1ed',font="宋体 13",relief=FLAT)
    path_entry.place(relx=0.38,rely=0.25)
    upload_btn = Button(single_wd, image=icon_list[1], command=lambda: upload(photo_area, pathname, num_photo, comb_value),
                        relief=FLAT,bg='#f8ffff')
    upload_btn.place(relx=0.44,rely=0.85)
    ''''''

root = Tk()
# root.overrideredirect(True)

icon_list = []
select_image = Image.open("选择单项2.jpg")
select_photo = ImageTk.PhotoImage(select_image) #0
icon_list.append(select_photo)

upload_image = Image.open("上传.jpg") #1
upload_photo = ImageTk.PhotoImage(upload_image)
icon_list.append(upload_photo)

ui_list = []
test_string = "周子昕 15902348495 500109199804060423 2020.08.07 这是地址"
split_list = test_string.split(' ')
print(handwriting_match(split_list))



main_canv = Canvas(root, bd=1, width=1000, height=640)
main_canv.pack()
bg_image = Image.open("bg.jpg")
bg = ImageTk.PhotoImage(bg_image)
main_canv.create_image(0, 0, image=bg, anchor=NW)

# 下右
button_image = Image.open("管理长.jpg")
button_image = button_image.resize((240, 200))
button_photo = ImageTk.PhotoImage(button_image)
ui_list.append(button_photo)
manage_btn = Button(main_canv, image=ui_list[0], command=manage, relief=FLAT)
manage_btn.place(relx=0.5, rely=0.55)

# 下左
button_image = Image.open("交易长.jpg")
button_image = button_image.resize((240, 200))
button_photo = ImageTk.PhotoImage(button_image)
ui_list.append(button_photo)
trade_btn = Button(main_canv, image=ui_list[1], command=upload_trade, relief=FLAT)
trade_btn.place(relx=0.245, rely=0.55)

# 上左
button_image = Image.open("单项长2.jpg")
button_image = button_image.resize((240, 200))
button_photo = ImageTk.PhotoImage(button_image)
ui_list.append(button_photo)
single_btn = Button(main_canv, image=ui_list[2], command=upload_single, relief=FLAT)
single_btn.place(relx=0.245, rely=0.218)

single_image = Image.open("bg3.jpg")
single_bg = ImageTk.PhotoImage(single_image)
ui_list.append(single_bg)#3

'''
size_w = 300
size_h = 260
main_canv.grid_columnconfigure(0, minsize=size_w)
main_canv.grid_rowconfigure(0, minsize=size_h)
main_canv.grid_columnconfigure(1, minsize=size_w)
main_canv.grid_rowconfigure(1, minsize=size_h)
#main_canv["background"] = '#c06f98'
'''
root.mainloop()
