import requests
import base64
import sqlite3
import tkinter


# 数据库指令运行
def sql_conn(sql: str):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    db.commit()
    db.close()
    return result


# 数据库初始化
def sql_init():
    # 删表
    cmd = '''DROP TABLE IF EXISTS t_transaction'''
    sql_conn(cmd)
    cmd = '''DROP TABLE IF EXISTS t_general_basic'''
    sql_conn(cmd)
    cmd = '''DROP TABLE IF EXISTS t_business_card'''
    sql_conn(cmd)
    cmd = '''DROP TABLE IF EXISTS t_bankcard'''
    sql_conn(cmd)
    cmd = '''DROP TABLE IF EXISTS t_business_license'''
    sql_conn(cmd)
    cmd = '''DROP TABLE IF EXISTS t_invoice'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_transaction(
                id INTEGER AUTO_INCREMENT NOT NULL ,        -- 主键
                PRIMARY KEY (id))'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_general_basic(
                id INTEGER AUTO_INCREMENT NOT NULL ,        -- 主键
                content varchar(1000) NOT NULL DEFAULT '', -- 内容
                remark varchar(100) NOT NULL DEFAULT '',   -- 备注
                transaction_id INTEGER NOT NULL,           -- 外键
                PRIMARY KEY (id))'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_business_card(
                id INTEGER AUTO_INCREMENT NOT NULL,         -- 主键
                addr varchar(100) NOT NULL DEFAULT '',      -- 地址
                fax varchar(100) NOT NULL DEFAULT '',       -- 传真
                mobile varchar(100) NOT NULL DEFAULT '',    -- 手机
                name varchar(100) NOT NULL DEFAULT '',      -- 姓名
                pc varchar(100) NOT NULL DEFAULT '',        -- ?
                url varchar(100) NOT NULL DEFAULT '',       -- 网址
                tel varchar(100) NOT NULL DEFAULT '',       -- 固话
                company varchar(100) NOT NULL DEFAULT '',   -- 公司
                title varchar(100) NOT NULL DEFAULT '',     -- 职称
                email varchar(100) NOT NULL DEFAULT '',     -- 电邮
                transaction_id INTEGER NOT NULL,            -- 外键
                PRIMARY KEY (id))'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_bankcard(
                id INTEGER AUTO_INCREMENT NOT NULL,                     -- 主键
                bank_card_number varchar(100) NOT NULL DEFAULT '',     -- 银行卡号
                valid_date varchar(100) NOT NULL DEFAULT '',            -- 过期日
                bank_card_type varchar(100) NOT NULL DEFAULT '',        -- 类型
                bank_name varchar(100) NOT NULL DEFAULT '',             -- 银行名称
                transaction_id INTEGER NOT NULL,                        -- 外键
                PRIMARY KEY (id))'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_business_license(
                id INTEGER AUTO_INCREMENT NOT NULL,                     -- 主键
                registered_capital varchar(100) NOT NULL DEFAULT '',   -- 注册资本
                social_credit_number varchar(100) NOT NULL DEFAULT '', -- 社会信用代码
                company_name varchar(100) NOT NULL DEFAULT '',          -- 单位名称
                legal_person varchar(100) NOT NULL DEFAULT '',          -- 法人
                license_id varchar(100) NOT NULL DEFAULT '',            -- 证件编号
                organization_form varchar(100) NOT NULL DEFAULT '',        -- 组成形式
                establishment_date varchar(100) NOT NULL DEFAULT '',       --成立日期
                addr varchar(100) NOT NULL DEFAULT '',                     -- 地址
                business_scope varchar(100) NOT NULL DEFAULT '',           -- 经营范围
                type varchar(100) NOT NULL DEFAULT '',                     -- 类型
                expiration_date varchar(100) NOT NULL DEFAULT '',          -- 有效期
                transaction_id INTEGER NOT NULL,                        -- 外键
                PRIMARY KEY (id))'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_invoice(
                id INTEGER AUTO_INCREMENT NOT NULL,                     -- 主键
                amount_in_words varchar(100) NOT NULL DEFAULT '',   -- 注册资本
                commodity_price varchar(100) NOT NULL DEFAULT '', -- 社会信用代码
                note_drawer varchar(100) NOT NULL DEFAULT '',          -- 单位名称
                seller_addr varchar(100) NOT NULL DEFAULT '',          -- 法人
                commodity_num varchar(100) NOT NULL DEFAULT '',            -- 证件编号
                seller_register_num varchar(100) NOT NULL DEFAULT '',        -- 组成形式
                remarks varchar(100) NOT NULL DEFAULT '',       --成立日期
                seller_bank varchar(100) NOT NULL DEFAULT '',                     -- 地址
                commodity_tax_rate varchar(100) NOT NULL DEFAULT '',           -- 经营范围
                total_tax varchar(100) NOT NULL DEFAULT '',                     -- 类型
                check_code varchar(100) NOT NULL DEFAULT '',          -- 有效期
                invoice_code varchar(100) NOT NULL DEFAULT '',
                invoice_date varchar(100) NOT NULL DEFAULT '',
                purchaser_register_num varchar(100) NOT NULL DEFAULT '',
                invoice_type_org varchar(100) NOT NULL DEFAULT '',
                password varchar(100) NOT NULL DEFAULT '',
                amount_in_figuers varchar(100) NOT NULL DEFAULT '',
                purchaser_bank varchar(100) NOT NULL DEFAULT '',
                checker varchar(100) NOT NULL DEFAULT '',
                totalAmount varchar(100) NOT NULL DEFAULT '',
                commodity_amount varchar(100) NOT NULL DEFAULT '',
                purchaser_name varchar(100) NOT NULL DEFAULT '',
                commodity_type varchar(100) NOT NULL DEFAULT '',
                invoice_type varchar(100) NOT NULL DEFAULT '',
                purchaser_addr varchar(100) NOT NULL DEFAULT '',
                commodity_tax varchar(100) NOT NULL DEFAULT '',
                commodity_unit varchar(100) NOT NULL DEFAULT '',
                payee varchar(100) NOT NULL DEFAULT '',
                commodity_name varchar(100) NOT NULL DEFAULT '',
                seller_name varchar(100) NOT NULL DEFAULT '',
                invoice_num varchar(100) NOT NULL DEFAULT '',
                transaction_id INTEGER NOT NULL,                        -- 外键
                PRIMARY KEY (id))'''
    sql_conn(cmd)


# TODO: 增
def sql_add(type: str, content: dict):
    pass


# TODO: 删
def sql_delete(type: str, id: int):
    pass


# TODO: 查
def sql_search():
    pass


# TODO: 改
def sql_modify(type: str, content: dict):
    pass


# 获取OCR接口Token
def get_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?' \
           'grant_type=client_credentials&client_' \
           'id=M1w2PuNLDG3yngWaVYuyTgmW&' \
           'client_secret=Doy4yiuRfH9zeOD3g6viwVg6oDyWwqto'
    response = requests.get(host)
    return response.json()['access_token']


# 通用文字识别
def ocr_general_basic(img_path: str = './test_case/example.jpg'):
    '''
    :param img_path: 图片路径
    :return: 识别结果
    '''

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = get_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        # 返回完整字符串
        num = response.json()['words_result_num']
        words = response.json()['words_result']
        result = ""
        for i in range(num):
            result += words[i]['words']
        return result
    else:
        print("OCR Connection Error!")


# 名片识别
def ocr_business_card(img_path: str = './test_case/card.jpg'):
    '''
    :param img_path: 图片路径
    :return: 识别结果
    '''

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/business_card"
    # 二进制方式打开图片文件
    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = get_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()['words_result']
    else:
        print("OCR Connection Error!")


# 银行卡识别
def ocr_bankcard(img_path: str = './test_case/bankcard.jpg'):
    '''
    :param img_path: 图片路径
    :return: 识别结果
    '''

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/bankcard"
    # 二进制方式打开图片文件
    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = get_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()['result']
    else:
        print("OCR Connection Error!")


# 营业执照识别
def ocr_business_license(img_path: str = './test_case/business_license.jpg'):
    '''
    :param img_path: 图片路径
    :return: 识别结果
    '''

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/business_license"
    # 二进制方式打开图片文件
    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = get_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()['words_result']
    else:
        print("OCR Connection Error!")


# 发票识别
def ocr_invoice(img_path: str = './test_case/invoice.png'):
    '''
    :param img_path:
    :return:
    '''

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/vat_invoice"
    # 二进制方式打开图片文件
    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = get_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()['words_result']
    else:
        print("OCR Connection Error!")