import requests
import base64
import sqlite3
import tkinter


def sql_conn(sql: str):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    db.commit()
    db.close()
    return result


def sql_init():
    # 建表
    cmd = '''DROP TABLE IF EXISTS ocr'''
    sql_conn(cmd)
    cmd = '''CREATE TABLE ocr(
            id INTEGER AUTO_INCREMENT NOT NULL , -- 主键
            name varchar(100) NOT NULL DEFAULT '', -- 名字
            PRIMARY KEY (id))'''
    sql_conn(cmd)


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