import sqlite3
from ocr import *


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
    cmd = '''DROP TABLE IF EXISTS t_invoice_commodity'''
    sql_conn(cmd)
    cmd = '''DROP TABLE IF EXISTS t_invoice'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_transaction(
                id              INTEGER         PRIMARY KEY AUTOINCREMENT,          -- 主键
                name            VARCHAR(100)    NOT NULL DEFAULT '/',               -- 名称
                create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP  -- 创建时间
                )'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_general_basic(
                id              INTEGER         PRIMARY KEY AUTOINCREMENT,      -- 主键
                content         VARCHAR(5000)   NOT NULL DEFAULT '',            -- 内容
                remark          VARCHAR(100)    NOT NULL DEFAULT '',            -- 备注
                transaction_id  INTEGER         NOT NULL,                       -- 外键
                picture         LONGBOLB        NOT NULL DEFAULT ''
                )'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_business_card(
                id              INTEGER         PRIMARY KEY AUTOINCREMENT,  -- 主键
                name            VARCHAR(100)    NOT NULL DEFAULT '',        -- 姓名
                title           VARCHAR(100)    NOT NULL DEFAULT '',        -- 职称
                company         VARCHAR(100)    NOT NULL DEFAULT '',        -- 公司
                addr            VARCHAR(100)    NOT NULL DEFAULT '',        -- 地址
                mobile          VARCHAR(100)    NOT NULL DEFAULT '',        -- 手机
                fax             VARCHAR(100)    NOT NULL DEFAULT '',        -- 传真
                tel             VARCHAR(100)    NOT NULL DEFAULT '',        -- 固话
                email           VARCHAR(100)    NOT NULL DEFAULT '',        -- 电邮
                -- pc              VARCHAR(100)    NOT NULL DEFAULT '',        -- ?
                url             VARCHAR(100)    NOT NULL DEFAULT '',        -- 网址
                transaction_id  INTEGER         NOT NULL,                   -- 外键
                picture         LONGBOLB        NOT NULL DEFAULT ''
                )'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_bankcard(
                id                  INTEGER         PRIMARY KEY AUTOINCREMENT,  -- 主键
                bank_card_number    VARCHAR(100)   NOT NULL DEFAULT '',         -- 银行卡号
                bank_name           VARCHAR(100)    NOT NULL DEFAULT '',        -- 银行名称
                bank_card_type      VARCHAR(100)    NOT NULL DEFAULT '',        -- 类型
                valid_date          VARCHAR(100)    NOT NULL DEFAULT '',        -- 过期日
                transaction_id      INTEGER         NOT NULL,                   -- 外键
                picture             LONGBOLB        NOT NULL DEFAULT ''
                )'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_business_license(
                id                      INTEGER         PRIMARY KEY AUTOINCREMENT,  -- 主键
                company_name            VARCHAR(100)    NOT NULL DEFAULT '',        -- 单位名称
                legal_person            VARCHAR(100)    NOT NULL DEFAULT '',        -- 法人
                license_id              VARCHAR(100)    NOT NULL DEFAULT '',        -- 证件编号
                social_credit_number    VARCHAR(100)    NOT NULL DEFAULT '',        -- 社会信用代码
                establishment_date      VARCHAR(100)    NOT NULL DEFAULT '',        -- 成立日期
                expiration_date         VARCHAR(100)    NOT NULL DEFAULT '',        -- 有效期
                registered_capital      VARCHAR(100)    NOT NULL DEFAULT '',        -- 注册资本
                addr                    VARCHAR(100)    NOT NULL DEFAULT '',        -- 地址
                business_scope          VARCHAR(100)    NOT NULL DEFAULT '',        -- 经营范围
                -- type                    VARCHAR(100)    NOT NULL DEFAULT '',        -- 类型
                -- organization_form       VARCHAR(100)    NOT NULL DEFAULT '',        -- 组成形式
                transaction_id          INTEGER         NOT NULL,                   -- 外键
                picture                 LONGBOLB        NOT NULL DEFAULT ''
                )'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_invoice(
                id                      INTEGER         PRIMARY KEY AUTOINCREMENT,
                invoice_type            VARCHAR(100)    NOT NULL DEFAULT '',
                invoice_code            VARCHAR(100)    NOT NULL DEFAULT '',
                invoice_num             VARCHAR(100)    NOT NULL DEFAULT '',
                invoice_date            VARCHAR(100)    NOT NULL DEFAULT '',
                purchaser_name          VARCHAR(100)    NOT NULL DEFAULT '',
                purchaser_register_num  VARCHAR(100)    NOT NULL DEFAULT '',
                seller_name             VARCHAR(100)    NOT NULL DEFAULT '',
                seller_register_num     VARCHAR(100)    NOT NULL DEFAULT '',
                seller_addr             VARCHAR(100)    NOT NULL DEFAULT '',
                seller_bank             VARCHAR(100)    NOT NULL DEFAULT '',
                amount_in_figures       VARCHAR(100)    NOT NULL DEFAULT '',
                
                -- amount_in_words         VARCHAR(100)    NOT NULL DEFAULT '',           
                -- commodity_price         VARCHAR(100)    NOT NULL DEFAULT '',        
                -- note_drawer             VARCHAR(100)    NOT NULL DEFAULT '',           
                -- commodity_num           VARCHAR(100)    NOT NULL DEFAULT '',         
                -- remarks                 VARCHAR(100)    NOT NULL DEFAULT '',          
                -- commodity_tax_rate      VARCHAR(100)    NOT NULL DEFAULT '',         
                -- total_tax               VARCHAR(100)    NOT NULL DEFAULT '',            
                -- check_code              VARCHAR(100)    NOT NULL DEFAULT '',           
                -- invoice_type_org        VARCHAR(100)    NOT NULL DEFAULT '',
                -- password                VARCHAR(100)    NOT NULL DEFAULT '',
                -- purchaser_bank          VARCHAR(100)    NOT NULL DEFAULT '',
                -- checker                 VARCHAR(100)    NOT NULL DEFAULT '',
                -- totalAmount             VARCHAR(100)    NOT NULL DEFAULT '',
                -- commodity_amount        VARCHAR(100)    NOT NULL DEFAULT '',  
                -- commodity_type          VARCHAR(100)    NOT NULL DEFAULT '',
                -- purchaser_addr          VARCHAR(100)    NOT NULL DEFAULT '',
                -- commodity_tax           VARCHAR(100)    NOT NULL DEFAULT '',
                -- commodity_unit          VARCHAR(100)    NOT NULL DEFAULT '',
                -- payee                   VARCHAR(100)    NOT NULL DEFAULT '',
                -- commodity_name          VARCHAR(100)    NOT NULL DEFAULT '',
                transaction_id          INTEGER         NOT NULL,                       -- 外键
                picture                 LONGBOLB        NOT NULL DEFAULT ''
                )'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_invoice_commodity(
                invoice_id          INTEGER,
                commodity_name      VARCHAR(100)     NOT NULL DEFAULT '',
                commodity_type      VARCHAR(100)     NOT NULL DEFAULT '',
                commodity_num       VARCHAR(100)     NOT NULL DEFAULT '',
                commodity_price     VARCHAR(100)     NOT NULL DEFAULT '',
                commodity_amount    VARCHAR(100)     NOT NULL DEFAULT '',
                commodity_tax_rate  VARCHAR(100)     NOT NULL DEFAULT '',
                commodity_tax       VARCHAR(100)     NOT NULL DEFAULT '',
                FOREIGN KEY (invoice_id) REFERENCES t_invoice(id)
                )'''
    sql_conn(cmd)


# 增
def sql_insert(ocr_type: OCR, content: dict):
    if ocr_type == OCR.TRANSACTION:
        cmd = '''INSERT INTO t_transaction 
                (name)
            VALUES ("{}")
        '''.format(content['name'])
        sql_conn(cmd)

    elif ocr_type == OCR.GENERAL_BASIC:
        cmd = '''INSERT INTO t_general_basic 
                (content, remark, transaction_id) 
            VALUES ("{}","{}",{}) 
        '''.format(content['content'], content['remark'], content['transaction_id'])
        sql_conn(cmd)

    elif ocr_type == OCR.INVOICE:
        cmd = '''INSERT INTO t_invoice 
                (invoice_type, invoice_code, invoice_num, invoice_date,
                 purchaser_name, purchaser_register_num, 
                 seller_name, seller_register_num, seller_addr,seller_bank,
                 amount_in_figures, 
                 transaction_id) 
            VALUES ("{}","{}","{}","{}",
                    "{}","{}",
                    "{}","{}","{}","{}",
                    "{}",
                     {}) 
                '''.format(content['invoice_type'], content['invoice_code'], content['invoice_num'], content['invoice_date'],
                           content['purchaser_name'], content['purchaser_register_num'],
                           content['seller_name'], content['seller_register_num'], content['seller_addr'], content['seller_bank'],
                           content['amount_in_figures'],
                           content['transaction_id'])
        sql_conn(cmd)
        invoice_id = sql_conn('''SELECT max(id) FROM t_invoice''')[0][0]
        for i in range(len(content['commodity']['name'])):
            cmd = '''INSERT INTO t_invoice_commodity
                    (invoice_id, commodity_name, 
                    commodity_type, commodity_num,
                    commodity_price, commodity_amount,
                    commodity_tax_rate, commodity_tax
                    )
            VALUES ("{}","{}",
                    "{}","{}",
                    "{}","{}",
                    "{}","{}") 
                '''.format(invoice_id, content['commodity']['name'][i],
                           content['commodity']['type'][i], content['commodity']['name'][i],
                           content['commodity']['price'][i], content['commodity']['amount'][i],
                           content['commodity']['tax_rate'][i], content['commodity']['tax'][i])
            sql_conn(cmd)

    elif ocr_type == OCR.BANKCARD:
        cmd = '''INSERT INTO t_bankcard
                (bank_card_number, valid_date, bank_card_type, bank_name,
                 transaction_id) 
            VALUES ("{}","{}","{}","{}",
                    "{}")
            '''.format(content['bank_card_number'], content['valid_date'], content['bank_card_type'],content['bank_name'],
                       content['transaction_id'])
        sql_conn(cmd)

    elif ocr_type == OCR.BUSINESS_CARD:
        cmd = '''INSERT INTO t_business_card 
                (addr, fax, mobile, name,
                url, tel,
                company, title, email, transaction_id)
            VALUES ("{}","{}","{}","{}",
                    "{}","{}",
                    "{}","{}","{}",{})
            '''.format(content['addr'], content['fax'], content['mobile'], content['name'],
                       content['url'], content['tel'],
                       content['company'], content['title'], content['email'], content['transaction_id'])
        sql_conn(cmd)

    elif ocr_type == OCR.BUSINESS_LICENSE:
        cmd = '''INSERT INTO t_business_license
                (registered_capital, social_credit_number, company_name, legal_person,
                license_id, establishment_date, addr, 
                business_scope, expiration_date, transaction_id)
            VALUES ("{}","{}","{}","{}",
                    "{}","{}","{}",
                    "{}","{}",{})
            '''.format(content['registered_capital'],content['social_credit_number'],content['company_name'],content['legal_person'],
                       content['license_id'],content['establishment_date'],content['addr'],
                       content['business_scope'],content['expiration_date'],content['transaction_id'])
        sql_conn(cmd)

    else:
        print("Type Error")


# 删
def sql_delete(ocr_type: OCR, id: int):
    if ocr_type == OCR.TRANSACTION:
        cmd = '''DELETE FROM t_transaction 
            WHERE id = {}
        '''.format(id)
        sql_conn(cmd)
    elif ocr_type == OCR.GENERAL_BASIC:
        cmd = '''DELETE FROM t_general_basic
            WHERE id = {}
        '''.format(id)
        sql_conn(cmd)
    elif ocr_type == OCR.INVOICE:
        cmd = '''DELETE FROM t_invoice
            WHERE id = {}
        '''.format(id)
        sql_conn(cmd)
        cmd = '''DELETE FROM t_invoice_commodity
                WHERE invoice_id = {}
                '''.format(id)
        sql_conn(cmd)
    elif ocr_type == OCR.BANKCARD:
        cmd = '''DELETE FROM t_bankcard
            WHERE id = {}
        '''.format(id)
        sql_conn(cmd)
    elif ocr_type == OCR.BUSINESS_CARD:
        cmd = '''DELETE FROM t_business_card
            WHERE id = {}
        '''.format(id)
        sql_conn(cmd)
    elif ocr_type == OCR.BUSINESS_LICENSE:
        cmd = '''DELETE FROM t_business_license
            WHERE id = {}
        '''.format(id)
        sql_conn(cmd)
    else:
        print("Type Error")


# 查
def sql_query(ocr_type: OCR, content: str):
    if ocr_type == OCR.TRANSACTION:
        cmd = '''SELECT * FROM t_transaction WHERE 
                id LIKE '%{}%' OR 
                name LIKE '%{}%' OR 
                create_time LIKE '%{}%'
                '''.format(content, content, content)
        data = sql_conn(cmd)
        res = {
            'id': [],
            'name': [],
            'create_time': []}
        for row in data:
            res['id'].append(row[0])
            res['name'].append(row[1])
            res['create_time'].append(row[2])
        return res
    elif ocr_type == OCR.GENERAL_BASIC:
        cmd = '''SELECT * FROM t_general_basic WHERE 
                        id LIKE '%{}%' OR 
                        content LIKE '%{}%' OR 
                        remark LIKE '%{}%' OR
                        transaction_id LIKE '%{}%'
                        '''.format(content, content, content, content)
        data = sql_conn(cmd)
        res = {
            'id': [],
            'content': [],
            'remark': [],
            'transaction_id': [],
            'picture': [],
        }
        for row in data:
            res['id'].append(row[0])
            res['content'].append(row[1])
            res['remark'].append(row[2])
            res['transaction_id'].append(row[3])
        return res
    elif ocr_type == OCR.BUSINESS_CARD:
        cmd = '''SELECT * FROM t_business_card WHERE 
                                id LIKE '%{}%' OR 
                                name LIKE '%{}%' OR 
                                title LIKE '%{}%' OR
                                company LIKE '%{}%' OR 
                                addr LIKE '%{}%' OR 
                                mobile LIKE '%{}%' OR 
                                fax LIKE '%{}%' OR 
                                tel LIKE '%{}%' OR 
                                email LIKE '%{}%' OR 
                                url LIKE '%{}%' OR 
                                transaction_id LIKE '%{}%'
                                '''.format(content, content, content, content,
                                           content, content, content, content,
                                           content, content, content)
        data = sql_conn(cmd)
        res = {
            'id': [],
            'name': [],
            'title': [],
            'company': [],
            'addr': [],
            'mobile': [],
            'fax': [],
            'tel': [],
            'email': [],
            'url': [],
            'transaction_id': [],
            'picture': [],
        }
        for row in data:
            res['id'].append(row[0])
            res['name'].append(row[1])
            res['title'].append(row[2])
            res['company'].append(row[3])
            res['addr'].append(row[4])
            res['mobile'].append(row[5])
            res['fax'].append(row[6])
            res['tel'].append(row[7])
            res['email'].append(row[8])
            res['url'].append(row[9])
            res['transaction_id'].append(row[10])
            res['picture'].append(row[11])
        return res
    elif ocr_type == OCR.BANKCARD:
        cmd = '''SELECT * FROM t_bankcard WHERE 
                                id LIKE '%{}%' OR 
                                bank_card_number LIKE '%{}%' OR 
                                bank_name LIKE '%{}%' OR
                                bank_card_type LIKE '%{}%' OR 
                                valid_date LIKE '%{}%' OR 
                                transaction_id LIKE '%{}%'
                                '''.format(content, content, content, content,
                                           content, content)
        data = sql_conn(cmd)
        res = {
            'id': [],
            'bank_card_number': [],
            'bank_name': [],
            'bank_card_type': [],
            'valid_date': [],
            'transaction_id': [],
            'picture': [],
        }
        for row in data:
            res['id'].append(row[0])
            res['bank_card_number'].append(row[1])
            res['bank_name'].append(row[2])
            res['transaction_id'].append(row[3])
            res['bank_card_type'].append(row[4])
            res['valid_date'].append(row[5])
            res['transaction_id'].append(row[6])
            res['id'].append(row[7])
        return res
    elif ocr_type == OCR.BUSINESS_LICENSE:
        cmd = '''SELECT * FROM t_business_license WHERE 
                                id LIKE '%{}%' OR 
                                company_name LIKE '%{}%' OR 
                                legal_person LIKE '%{}%' OR 
                                license_id LIKE '%{}%' OR 
                                social_credit_number LIKE '%{}%' OR 
                                establishment_date LIKE '%{}%' OR 
                                expiration_date LIKE '%{}%' OR 
                                registered_capital LIKE '%{}%' OR 
                                addr LIKE '%{}%' OR 
                                business_scope LIKE '%{}%' OR 
                                transaction_id LIKE '%{}%'
                                '''.format(content, content, content, content,
                                           content, content, content, content,
                                           content, content, content)
        data = sql_conn(cmd)
        res = {
            'id': [],
            'company_name': [],
            'legal_person': [],
            'license_id': [],
            'social_credit_number': [],
            'establishment_date': [],
            'expiration_date': [],
            'registered_capital': [],
            'addr': [],
            'business_scope': [],
            'transaction_id': [],
            'picture': [],
        }
        for row in data:
            res['id'].append(row[0])
            res['company_name'].append(row[1])
            res['legal_person'].append(row[2])
            res['license_id'].append(row[3])
            res['social_credit_number'].append(row[4])
            res['establishment_date'].append(row[5])
            res['expiration_date'].append(row[6])
            res['registered_capital'].append(row[7])
            res['addr'].append(row[8])
            res['business_scope'].append(row[9])
            res['transaction_id'].append(row[10])
            res['picture'].append(row[11])
        return res
    elif ocr_type == OCR.INVOICE:
        cmd = '''SELECT * FROM t_invoice WHERE 
                id LIKE '%{}%' OR 
                invoice_type LIKE '%{}%' OR 
                invoice_code LIKE '%{}%' OR 
                invoice_num LIKE '%{}%' OR 
                invoice_date LIKE '%{}%' OR 
                purchaser_name LIKE '%{}%' OR 
                purchaser_register_num LIKE '%{}%' OR 
                seller_name LIKE '%{}%' OR 
                seller_register_num LIKE '%{}%' OR 
                seller_addr LIKE '%{}%' OR 
                seller_bank LIKE '%{}%' OR 
                amount_in_figures LIKE '%{}%' OR
                transaction_id LIKE '%{}%' OR
                '''.format(content, content, content, content,
                           content, content, content, content,
                           content, content, content, content,
                           content)
        data = sql_conn(cmd)
        res = {
            'id': [],
            'invoice_type': [],
            'invoice_code': [],
            'invoice_num': [],
            'invoice_date': [],
            'purchaser_name': [],
            'purchaser_register_num': [],
            'seller_name': [],
            'seller_register_num': [],
            'seller_addr': [],
            'seller_bank': [],
            'amount_in_figures': [],
            'transaction_id': [],
            'picture': [],
        }
        for row in data:
            res['id'].append(row[0])
            res['invoice_type'].append(row[1])
            res['invoice_code'].append(row[2])
            res['invoice_date'].append(row[3])
            res['purchaser_name'].append(row[4])
            res['purchaser_register_num'].append(row[5])
            res['purchaser_register_num'].append(row[6])
            res['seller_name'].append(row[7])
            res['seller_register_num'].append(row[8])
            res['seller_addr'].append(row[9])
            res['seller_bank'].append(row[10])
            res['picture'].append(row[11])
            res['amount_in_figures'].append(row[12])
            res['transaction_id'].append(row[13])
            res['picture'].append(row[14])
        return res


# 提取具体信息
def sql_extract(ocr_type: OCR, id: int):
    if ocr_type == OCR.TRANSACTION:
        cmd = '''SELECT * FROM t_transaction WHERE 
                id = {}
                '''.format(id)
        data = sql_conn(cmd)
        if len(data[0]) == 0:
            print("Extract Error!")
            return None
        else:
            row = data[0]
            res = {
                'id': row[0],
                'name': row[1],
                'create_time': row[2]
            }
            return res
    elif ocr_type == OCR.GENERAL_BASIC:
        cmd = '''SELECT * FROM t_general_basic WHERE 
                        id = {}
                        '''.format(id)
        data = sql_conn(cmd)
        if len(data[0]) == 0:
            print("Extract Error!")
            return None
        else:
            row = data[0]
            res = {
                'id': row[0],
                'content': row[1],
                'remark': row[2],
                'transaction_id': row[3],
                'picture': row[4],
            }
            return res
    elif ocr_type == OCR.BUSINESS_CARD:
        cmd = '''SELECT * FROM t_business_card WHERE 
                        id = {}
                        '''.format(id)
        data = sql_conn(cmd)
        if len(data[0]) == 0:
            print("Extract Error!")
            return None
        else:
            row = data[0]
            res = {
                'id': row[0],
                'name': row[1],
                'title': row[2],
                'company': row[3],
                'addr': row[4],
                'mobile': row[5],
                'fax': row[6],
                'tel': row[7],
                'email': row[8],
                'url': row[9],
                'transaction_id': row[10],
                'picture': row[11],
            }
            return res
    elif ocr_type == OCR.BANKCARD:
        cmd = '''SELECT * FROM t_bankcard WHERE 
                        id = {}
                        '''.format(id)
        data = sql_conn(cmd)
        if len(data[0]) == 0:
            print("Extract Error!")
            return None
        else:
            row = data[0]
            res = {
                'id': row[0],
                'bank_card_number': row[1],
                'bank_name': row[2],
                'bank_card_type': row[3],
                'valid_date': row[4],
                'transaction_id': row[5],
                'picture': row[6],
            }
            return res
    elif ocr_type == OCR.BUSINESS_LICENSE:
        cmd = '''SELECT * FROM t_business_license WHERE 
                        id = {}
                        '''.format(id)
        data = sql_conn(cmd)
        if len(data[0]) == 0:
            print("Extract Error!")
            return None
        else:
            row = data[0]
            res = {
                'id': row[0],
                'company_name': row[1],
                'legal_person': row[2],
                'license_id': row[3],
                'social_credit_number': row[4],
                'establishment_date': row[5],
                'expiration_date': row[6],
                'registered_capital': row[7],
                'addr': row[8],
                'business_scope': row[9],
                'transaction_id': row[10],
                'picture': row[11],
            }
            return res
    elif ocr_type == OCR.INVOICE:
        cmd = '''SELECT * FROM t_invoice WHERE 
                id = {}
                '''.format(id)
        data = sql_conn(cmd)
        if len(data[0]) == 0:
            print("Extract Error!")
            return None
        else:
            row = data[0]
            res = {
                'id': row[0],
                'invoice_type': row[1],
                'invoice_code': row[2],
                'invoice_num': row[3],
                'invoice_date': row[4],
                'purchaser_name': row[5],
                'purchaser_register_num': row[6],
                'seller_name': row[7],
                'seller_register_num': row[8],
                'seller_addr': row[9],
                'seller_bank': row[10],
                'amount_in_figures': row[11],
                'transaction_id': row[12],
                'picture': row[13],
            }
            invoice_id = id
            cmd = '''SELECT * FROM t_invoice WHERE 
                            invoice_id = {}
                            '''.format(invoice_id)
            data = sql_conn(cmd)
            if len(data[0]) != 0:
                res['commodity']['name'] = []
                res['commodity']['type'] = []
                res['commodity']['num'] = []
                res['commodity']['price'] = []
                res['commodity']['amount'] = []
                res['commodity']['tax_rate'] = []
                res['commodity']['tax'] = []
                for item in data:
                    res['commodity']['name'].append(item[0])
                    res['commodity']['type'].append(item[1])
                    res['commodity']['num'].append(item[2])
                    res['commodity']['price'].append(item[3])
                    res['commodity']['amount'].append(item[4])
                    res['commodity']['tax_rate'].append(item[5])
                    res['commodity']['tax'].append(item[6])
            return res


# 改
def sql_modify(ocr_type: OCR, id: int, content: dict):
    if ocr_type == OCR.TRANSACTION:
        cmd = '''UPDATE t_transaction SET
            name = "{}",
            create_time = "{}"
        '''.format(content['name'],
                   content['create_time'])
        sql_conn(cmd)
    elif ocr_type == OCR.GENERAL_BASIC:
        cmd = '''UPDATE t_general_basic SET
                content = "{}", 
                remark = "{}", 
                transaction_id = {}
            WHERE id = {}
        '''.format(content['content'],
                   content['remark'],
                   content['transaction_id'], id)
        sql_conn(cmd)
    elif ocr_type == OCR.INVOICE:
        cmd = '''UPDATE t_invoice SET                     
                invoice_type = "{}",         
                invoice_code = "{}",         
                invoice_num = "{}",       
                invoice_date = "{}",    
                purchaser_name = "{}",     
                purchaser_register_num = "{}",  
                seller_name = "{}",        
                seller_register_num = "{}",   
                seller_addr = "{}",           
                seller_bank = "{}",      
                amount_in_figures = "{}",    
                transaction_id = {},              
            WHERE id = {}
                '''.format(content['invoice_type'],
                           content['invoice_code'],
                           content['invoice_num'],
                           content['invoice_date'],
                           content['purchaser_name'],
                           content['purchaser_register_num'],
                           content['seller_name'],
                           content['seller_register_num'],
                           content['seller_addr'],
                           content['seller_bank'],
                           content['amount_in_figures'],
                           content['transaction_id'],
                           id)
        sql_conn(cmd)
        invoice_id = id
        cmd = '''DELETE FROM t_invoice_commodity WHERE invoice_id = {}'''.format(invoice_id)
        sql_conn(cmd)
        for i in range(len(content['commodity']['name'])):
            cmd = '''INSERT INTO t_invoice_commodity
                    (invoice_id, commodity_name, 
                    commodity_type, commodity_num,
                    commodity_price, commodity_amount,
                    commodity_tax_rate, commodity_tax
                    )
            VALUES ("{}","{}",
                    "{}","{}",
                    "{}","{}",
                    "{}","{}") 
                '''.format(invoice_id, content['commodity']['name'][i],
                           content['commodity']['type'][i], content['commodity']['name'][i],
                           content['commodity']['price'][i], content['commodity']['amount'][i],
                           content['commodity']['tax_rate'][i], content['commodity']['tax'][i])
            sql_conn(cmd)
    elif ocr_type == OCR.BANKCARD:
        cmd = '''UPDATE t_bankcard SET
                bank_card_number = "{}", 
                valid_date = "{}", 
                bank_card_type = "{}", 
                bank_name = "{}",
                transaction_id = {}
            WHERE id = {}
            '''.format(content['bank_card_number'],
                       content['valid_date'],
                       content['bank_card_type'],
                       content['bank_name'],
                       content['transaction_id'],
                       id)
        sql_conn(cmd)
    elif ocr_type == OCR.BUSINESS_CARD:
        cmd = '''UPDATE t_business_card SET
                addr = "{}",
                fax = "{}",
                mobile = "{}",
                name = "{}",
                pc = "{}",
                url = "{}",
                tel = "{}",
                tel = "{}",
                company = "{}", 
                title = "{}", 
                email = "{}", 
                transaction_id = {}
            WHERE id = {}
            '''.format(content['addr'],
                       content['fax'],
                       content['mobile'],
                       content['name'],
                       content['pc'],
                       content['url'],
                       content['tel'],
                       content['tel'],
                       content['company'],
                       content['title'],
                       content['email'],
                       content['transaction_id'],
                       id)
        sql_conn(cmd)
    elif ocr_type == OCR.BUSINESS_LICENSE:
        cmd = '''UPDATE t_business_license SET
                registered_capital = "{}", 
                social_credit_number = "{}", 
                company_name = "{}", 
                legal_person = "{}",
                license_id = "{}", 
                organization_form = "{}", 
                establishment_date = "{}", 
                addr = "{}", 
                business_scope = "{}", 
                type = "{}", 
                expiration_date = "{}", 
                transaction_id = {}
            WHERE id = {}
            '''.format(content['registered_capital'],
                       content['social_credit_number'],
                       content['company_name'],
                       content['legal_person'],
                       content['license_id'],
                       content['organization_form'],
                       content['establishment_date'],
                       content['addr'],
                       content['business_scope'],
                       content['type'],
                       content['expiration_date'],
                       content['transaction_id'],
                       id)
        sql_conn(cmd)
    else:
        print("Type Error")

