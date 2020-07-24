import requests
import base64
from enum import Enum


class OCR(Enum):
    TRANSACTION = 0
    GENERAL_BASIC = 1
    BUSINESS_CARD = 2
    BANKCARD = 3
    BUSINESS_LICENSE = 4
    INVOICE = 5


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
        res = ocr_result_transform(OCR.BUSINESS_CARD, response.json()['words_result'])
        return res
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


# TODO: 通用文本字典定义未完成
def ocr_result_transform(ocr_type: OCR, origin: dict):
    new = {}
    if ocr_type == OCR.BUSINESS_CARD:
        new['addr'] = origin['ADDR']
        new['fax'] = origin['FAX']
        new['mobile'] = origin['MOBILE']
        new['name'] = origin['NAME']
        new['pc'] = origin['PC']
        new['url'] = origin['URL']
        new['tel'] = origin['TEL']
        new['company'] = origin['COMPANY']
        new['title'] = origin['TITLE']
        new['email'] = origin['EMAIL']
    elif ocr_type == OCR.INVOICE:
        new['amount_in_words'] = origin['AmountInWords']
        new['commodity_price'] = origin['CommodityPrice']
        new['note_drawer'] = origin['NoteDrawer']
        new['seller_addr'] = origin['SellerAddress']
        new['commodity_num'] = origin['CommodityNum']
        new['seller_register_num'] = origin['SellerRegisterNum']
        new['remarks'] = origin['Remarks']
        new['seller_bank'] = origin['SellerBank']
        new['commodity_tax_rate'] = origin['CommodityTaxRate']
        new['total_tax'] = origin['TotalTax']
        new['check_code'] = origin['CheckCode']
        new['invoice_code'] = origin['InvoiceCode']
        new['invoice_date'] = origin['InvoiceDate']
        new['purchaser_register_num'] = origin['PurchaserRegisterNum']
        new['invoice_type_org'] = origin['InvoiceTypeOrg']
        new['password'] = origin['Password']
        new['amount_in_figuers'] = origin['AmountInFiguers']
        new['purchaser_bank'] = origin['PurchaserBank']
        new['checker'] = origin['Checker']
        new['totalAmount'] = origin['TotalAmount']
        new['commodity_amount'] = origin['CommodityAmount']
        new['purchaser_name'] = origin['PurchaserName']
        new['commodity_type'] = origin['CommodityType']
        new['invoice_type'] = origin['InvoiceType']
        new['purchaser_addr'] = origin['PurchaserAddress']
        new['commodity_tax'] = origin['CommodityTax']
        new['commodity_unit'] = origin['CommodityUnit']
        new['payee'] = origin['Payee']
        new['commodity_name'] = origin['CommodityName']
        new['seller_name'] = origin['SellerName']
        new['invoice_num'] = origin['InvoiceNum']
    elif ocr_type == OCR.BANKCARD:
        new = origin
    elif ocr_type == OCR.BUSINESS_LICENSE:
        new['registered_capital'] = origin['注册资本']
        new['social_credit_number'] = origin['社会信用代码']
        new['company_name'] = origin['单位名称']
        new['legal_person'] = origin['法人']
        new['license_id'] = origin['证件编号']
        new['organization_form'] = origin['组成形式']
        new['establishment_date'] = origin['成立日期']
        new['addr'] = origin['地址']
        new['business_scope'] = origin['经营范围']
        new['type'] = origin['类型']
        new['expiration_date'] = origin['有效期']
    elif ocr_type == OCR.GENERAL_BASIC:
        new['content'] = origin
        new['remark '] ='???'
    else:
        print("Type Error")
        return
    new['transaction_id'] = 0
    return new
