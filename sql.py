import sqlite3
from ocr import *


# 数据库指令运行
def sql_conn(sql: str):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    # desc = cursor.description # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
    # data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来
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
                transaction_id  INTEGER         NOT NULL                        -- 外键
                )'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_business_card(
                id              INTEGER         PRIMARY KEY AUTOINCREMENT,  -- 主键
                addr            VARCHAR(100)    NOT NULL DEFAULT '',        -- 地址
                fax             VARCHAR(100)    NOT NULL DEFAULT '',        -- 传真
                mobile          VARCHAR(100)    NOT NULL DEFAULT '',        -- 手机
                name            VARCHAR(100)    NOT NULL DEFAULT '',        -- 姓名
                pc              VARCHAR(100)    NOT NULL DEFAULT '',        -- ?
                url             VARCHAR(100)    NOT NULL DEFAULT '',        -- 网址
                tel             VARCHAR(100)    NOT NULL DEFAULT '',        -- 固话
                company         VARCHAR(100)    NOT NULL DEFAULT '',        -- 公司
                title           VARCHAR(100)    NOT NULL DEFAULT '',        -- 职称
                email           VARCHAR(100)    NOT NULL DEFAULT '',        -- 电邮
                transaction_id  INTEGER         NOT NULL                    -- 外键
                )'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_bankcard(
                id                  INTEGER         PRIMARY KEY AUTOINCREMENT,  -- 主键
                bank_card_number    VARCHAR(100)   NOT NULL DEFAULT '',         -- 银行卡号
                valid_date          VARCHAR(100)    NOT NULL DEFAULT '',        -- 过期日
                bank_card_type      VARCHAR(100)    NOT NULL DEFAULT '',        -- 类型
                bank_name           VARCHAR(100)    NOT NULL DEFAULT '',        -- 银行名称
                transaction_id      INTEGER         NOT NULL                    -- 外键
                )'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_business_license(
                id                      INTEGER         PRIMARY KEY AUTOINCREMENT,  -- 主键
                registered_capital      VARCHAR(100)    NOT NULL DEFAULT '',        -- 注册资本
                social_credit_number    VARCHAR(100)    NOT NULL DEFAULT '',        -- 社会信用代码
                company_name            VARCHAR(100)    NOT NULL DEFAULT '',        -- 单位名称
                legal_person            VARCHAR(100)    NOT NULL DEFAULT '',        -- 法人
                license_id              VARCHAR(100)    NOT NULL DEFAULT '',        -- 证件编号
                organization_form       VARCHAR(100)    NOT NULL DEFAULT '',        -- 组成形式
                establishment_date      VARCHAR(100)    NOT NULL DEFAULT '',        --成立日期
                addr                    VARCHAR(100)    NOT NULL DEFAULT '',        -- 地址
                business_scope          VARCHAR(100)    NOT NULL DEFAULT '',        -- 经营范围
                type                    VARCHAR(100)    NOT NULL DEFAULT '',        -- 类型
                expiration_date         VARCHAR(100)    NOT NULL DEFAULT '',        -- 有效期
                transaction_id          INTEGER         NOT NULL                    -- 外键
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
                
                transaction_id          INTEGER         NOT NULL                        -- 外键
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
                pc, url, tel,
                company, title, email, transaction_id)
            VALUES ("{}","{}","{}","{}",
                    "{}","{}","{}",
                    "{}","{}","{}",{})
            '''.format(content['addr'], content['fax'], content['mobile'], content['name'],
                       content['pc'], content['url'], content['tel'],
                       content['company'], content['title'], content['email'], content['transaction_id'])
        sql_conn(cmd)

    elif ocr_type == OCR.BUSINESS_LICENSE:
        cmd = '''INSERT INTO t_business_license
                (registered_capital, social_credit_number, company_name, legal_person,
                license_id, organization_form, establishment_date, addr, 
                business_scope, type, expiration_date, transaction_id)
            VALUES ("{}","{}","{}","{}",
                    "{}","{}","{}","{}",
                    "{}","{}","{}",{})
            '''.format(content['registered_capital'],content['social_credit_number'],content['company_name'],content['legal_person'],
                       content['license_id'],content['organization_form'],content['establishment_date'],content['addr'],
                       content['business_scope'],content['type'],content['expiration_date'],content['transaction_id'])
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
def sql_query():
    pass


# 改
def sql_modify(ocr_type: OCR, id: int, content: dict):
    if ocr_type == OCR.TRANSACTION:
        cmd = '''UPDATE t_transaction SET
        '''.format()
        sql_conn(cmd)
    elif ocr_type == OCR.GENERAL_BASIC:
        cmd = '''UPDATE t_general_basic SET
                content = "{}", remark = "{}", transaction_id = {}
            WHERE id = {}
        '''.format(content['content'], content['remark'], content['transaction_id'], id)
        sql_conn(cmd)
    elif ocr_type == OCR.INVOICE:
        cmd = '''UPDATE t_invoice SET
                amount_in_words = "{}", note_drawer = "{}", seller_addr = "{}",
                seller_register_num = "{}", remarks = "{}", seller_bank = "{}",
                total_tax = "{}", check_code = "{}", invoice_code = "{}", 
                invoice_date = "{}", purchaser_register_num = "{}", invoice_type_org = "{}", password = "{}",
                amount_in_figuers = "{}", purchaser_bank = "{}", checker = "{}", totalAmount = "{}", 
                purchaser_name = "{}", invoice_type = "{}"
                purchaser_addr = "{}", payee = "{}",
                seller_name = "{}", invoice_num = "{}", transaction_id = {}
            WHERE id = {}}
                '''.format(content['amount_in_words'], content['note_drawer'], content['seller_addr'],
                           content['seller_register_num'], content['remarks'], content['seller_bank'],
                           content['total_tax'], content['check_code'], content['invoice_code'],
                           content['invoice_date'], content['purchaser_register_num'], content['invoice_type_org'], content['password'],
                           content['amount_in_figuers'], content['purchaser_bank'], content['checker'], content['totalAmount'],
                           content['purchaser_name'], content['invoice_type'],
                           content['purchaser_addr'], content['payee'],
                           content['seller_name'], content['invoice_num'], content['transaction_id'],
                           id)
        sql_conn(cmd)
    elif ocr_type == OCR.BANKCARD:
        cmd = '''UPDATE t_bankcard SET
                bank_card_number = "{}", valid_date = "{}", bank_card_type = "{}", bank_name = "{}",
                 transaction_id = {}
            WHERE id = {}
            '''.format(content['bank_card_number'], content['valid_date'], content['bank_card_type'], content['bank_name'],
                       content['transaction_id'], id)
        sql_conn(cmd)
    elif ocr_type == OCR.BUSINESS_CARD:
        cmd = '''UPDATE t_business_card SET
                addr = "{}", fax = "{}", mobile = "{}", name = "{}", 
                pc = "{}", url = "{}", tel = "{}", tel = "{}",
                company = "{}", title = "{}", email = "{}", transaction_id = {}
            WHERE id = {}
            '''.format(content['addr'], content['fax'], content['mobile'], content['name'],
                       content['pc'], content['url'], content['tel'], content['tel'],
                       content['company'], content['title'], content['email'], content['transaction_id'],
                       id)
        sql_conn(cmd)
    elif ocr_type == OCR.BUSINESS_LICENSE:
        cmd = '''UPDATE t_business_license SET
                registered_capital = "{}", social_credit_number = "{}", company_name = "{}", legal_person = "{}",
                license_id = "{}", organization_form = "{}", establishment_date = "{}", addr = "{}", 
                business_scope = "{}", type = "{}", expiration_date = "{}", transaction_id = {}
            WHERE id = {}
            '''.format(content['registered_capital'], content['social_credit_number'], content['company_name'], content['legal_person'],
                       content['license_id'], content['organization_form'], content['establishment_date'], content['addr'],
                       content['business_scope'], content['type'], content['expiration_date'], content['transaction_id'],
                       id)
        sql_conn(cmd)
    else:
        print("Type Error")

