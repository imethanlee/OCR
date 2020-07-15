import requests
import base64
import sqlite3


def sql_conn(sql: str):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    db.commit()
    db.close()
    return result


def ocr():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=M1w2PuNLDG3yngWaVYuyTgmW&client_secret=Doy4yiuRfH9zeOD3g6viwVg6oDyWwqto'
    response = requests.get(host)

    # 通用文字识别
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    f = open('./example.jpg', 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = response.json()['access_token']
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json())
