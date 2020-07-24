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
    cmd = '''DROP TABLE IF EXISTS t_invoice'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_transaction(
                id          INTEGER         PRIMARY KEY AUTOINCREMENT        -- 主键
                name        varchar(100)    NOT NULL DEFAULT '/'
                )'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_general_basic(
                id              INTEGER         PRIMARY KEY AUTOINCREMENT,        -- 主键
                content         varchar(1000)   NOT NULL DEFAULT '', -- 内容
                remark          varchar(100)    NOT NULL DEFAULT '',   -- 备注
                transaction_id  INTEGER         NOT NULL           -- 外键
                )'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_business_card(
                id              INTEGER         PRIMARY KEY AUTOINCREMENT,         -- 主键
                addr            varchar(100)    NOT NULL DEFAULT '',      -- 地址
                fax             varchar(100)    NOT NULL DEFAULT '',       -- 传真
                mobile          varchar(100)    NOT NULL DEFAULT '',    -- 手机
                name            varchar(100)    NOT NULL DEFAULT '',      -- 姓名
                pc              varchar(100)    NOT NULL DEFAULT '',        -- ?
                url             varchar(100)    NOT NULL DEFAULT '',       -- 网址
                tel             varchar(100)    NOT NULL DEFAULT '',       -- 固话
                company         varchar(100)    NOT NULL DEFAULT '',   -- 公司
                title           varchar(100)    NOT NULL DEFAULT '',     -- 职称
                email           varchar(100)    NOT NULL DEFAULT '',     -- 电邮
                transaction_id  INTEGER         NOT NULL            -- 外键
                )'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_bankcard(
                id                  INTEGER         PRIMARY KEY AUTOINCREMENT,                     -- 主键
                bank_card_number    varchar(100)   NOT NULL DEFAULT '',     -- 银行卡号
                valid_date          varchar(100)    NOT NULL DEFAULT '',            -- 过期日
                bank_card_type      varchar(100)    NOT NULL DEFAULT '',        -- 类型
                bank_name           varchar(100)    NOT NULL DEFAULT '',             -- 银行名称
                transaction_id      INTEGER         NOT NULL                        -- 外键
                )'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_business_license(
                id                      INTEGER         PRIMARY KEY AUTOINCREMENT,                     -- 主键
                registered_capital      varchar(100)    NOT NULL DEFAULT '',   -- 注册资本
                social_credit_number    varchar(100)    NOT NULL DEFAULT '', -- 社会信用代码
                company_name            varchar(100)    NOT NULL DEFAULT '',          -- 单位名称
                legal_person            varchar(100)    NOT NULL DEFAULT '',          -- 法人
                license_id              varchar(100)    NOT NULL DEFAULT '',            -- 证件编号
                organization_form       varchar(100)    NOT NULL DEFAULT '',        -- 组成形式
                establishment_date      varchar(100)    NOT NULL DEFAULT '',       --成立日期
                addr                    varchar(100)    NOT NULL DEFAULT '',                     -- 地址
                business_scope          varchar(100)    NOT NULL DEFAULT '',           -- 经营范围
                type                    varchar(100)    NOT NULL DEFAULT '',                     -- 类型
                expiration_date         varchar(100)    NOT NULL DEFAULT '',          -- 有效期
                transaction_id          INTEGER         NOT NULL                        -- 外键
                )'''
    sql_conn(cmd)

    cmd = '''CREATE TABLE t_invoice(
                id                      INTEGER         PRIMARY KEY AUTOINCREMENT,                          -- 主键
                amount_in_words         varchar(100)    NOT NULL DEFAULT '',           -- 注册资本
                commodity_price         varchar(100)    NOT NULL DEFAULT '',           -- 社会信用代码
                note_drawer             varchar(100)    NOT NULL DEFAULT '',               -- 单位名称
                seller_addr             varchar(100)    NOT NULL DEFAULT '',               -- 法人
                commodity_num           varchar(100)    NOT NULL DEFAULT '',             -- 证件编号
                seller_register_num     varchar(100)    NOT NULL DEFAULT '',       -- 组成形式
                remarks                 varchar(100)    NOT NULL DEFAULT '',                    --成立日期
                seller_bank             varchar(100)    NOT NULL DEFAULT '',                -- 地址
                commodity_tax_rate      varchar(100)    NOT NULL DEFAULT '',         -- 经营范围
                total_tax               varchar(100)    NOT NULL DEFAULT '',                   -- 类型
                check_code              varchar(100)    NOT NULL DEFAULT '',                  -- 有效期
                invoice_code            varchar(100)    NOT NULL DEFAULT '',
                invoice_date            varchar(100)    NOT NULL DEFAULT '',
                purchaser_register_num  varchar(100)    NOT NULL DEFAULT '',
                invoice_type_org        varchar(100)    NOT NULL DEFAULT '',
                password                varchar(100)    NOT NULL DEFAULT '',
                amount_in_figuers       varchar(100)    NOT NULL DEFAULT '',
                purchaser_bank          varchar(100)    NOT NULL DEFAULT '',
                checker                 varchar(100)    NOT NULL DEFAULT '',
                totalAmount             varchar(100)    NOT NULL DEFAULT '',
                commodity_amount        varchar(100)    NOT NULL DEFAULT '',
                purchaser_name          varchar(100)    NOT NULL DEFAULT '',
                commodity_type          varchar(100)    NOT NULL DEFAULT '',
                invoice_type            varchar(100)    NOT NULL DEFAULT '',
                purchaser_addr          varchar(100)    NOT NULL DEFAULT '',
                commodity_tax           varchar(100)    NOT NULL DEFAULT '',
                commodity_unit          varchar(100)    NOT NULL DEFAULT '',
                payee                   varchar(100)    NOT NULL DEFAULT '',
                commodity_name          varchar(100)    NOT NULL DEFAULT '',
                seller_name             varchar(100)    NOT NULL DEFAULT '',
                invoice_num             varchar(100)    NOT NULL DEFAULT '',
                transaction_id          INTEGER         NOT NULL                        -- 外键
                )'''
    sql_conn(cmd)


# 增
def sql_insert(ocr_type: OCR, content: dict):
    if ocr_type == OCR.TRANSACTION:
        cmd = '''INSERT INTO t_transaction ()
        '''
    elif ocr_type == OCR.GENERAL_BASIC:
        cmd = '''INSERT INTO t_general_basic 
                (content, remark, transaction_id) 
            VALUES ("{}","{}",{}) 
        '''.format(content['content'], content['remark'], content['transaction_id'])
        sql_conn(cmd)
    elif ocr_type == OCR.INVOICE:
        cmd = '''INSERT INTO t_invoice 
                (amount_in_words, commodity_price, note_drawer, seller_addr,
                commodity_num, seller_register_num, remarks, seller_bank,
                commodity_tax_rate, total_tax, check_code, invoice_code, 
                invoice_date, purchaser_register_num, invoice_type_org, password,
                amount_in_figuers, purchaser_bank, checker, totalAmount, 
                commodity_amount, purchaser_name, commodity_type, invoice_type
                purchaser_addr, commodity_tax, commodity_unit, payee,
                commodity_name, seller_name, invoice_num, transaction_id) 
            VALUES ("{}","{}","{}","{}",
                    "{}","{}","{}","{}",
                    "{}","{}","{}","{}",
                    "{}","{}","{}","{}",
                    "{}","{}","{}","{}",
                    "{}","{}","{}","{}",
                    "{}","{}","{}","{}",
                    "{}","{}","{}",{},) 
                '''.format(content['amount_in_words'], content['commodity_price'], content['note_drawer'], content['seller_addr'],
                           content['commodity_num'], content['seller_register_num'], content['remarks'], content['seller_bank'],
                           content['commodity_tax_rate'], content['total_tax'], content['check_code'], content['invoice_code'],
                           content['invoice_date'], content['purchaser_register_num'], content['invoice_type_org'], content['password'],
                           content['amount_in_figuers'], content['purchaser_bank'], content['checker'], content['totalAmount'],
                           content['commodity_amount'], content['purchaser_name'], content['commodity_type'], content['invoice_type'],
                           content['purchaser_addr'], content['commodity_tax'], content['commodity_unit'], content['payee'],
                           content['commodity_name'], content['seller_name'], content['invoice_num'], content['transaction_id'],)
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
                pc, url, tel, tel,
                company, title, email, transaction_id)
            VALUES ("{}","{}","{}","{}",
                    "{}","{}","{}","{}",
                    "{}","{}","{}",{})
            '''.format(content['addr'],content['fax'],content['mobile'],content['name'],
                       content['pc'],content['url'],content['tel'],content['tel'],
                       content['company'],content['title'],content['email'],content['transaction_id'])
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
    elif ocr_type == OCR.BANKCARD:
        cmd = '''DELETE FROM t_bankcard
            WHERE id = {}
        '''.format(id)
    elif ocr_type == OCR.BUSINESS_CARD:
        cmd = '''DELETE FROM t_business_card
            WHERE id = {}
        '''.format(id)
    elif ocr_type == OCR.BUSINESS_LICENSE:
        cmd = '''DELETE FROM t_business_license
            WHERE id = {}
        '''.format(id)
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
                amount_in_words = "{}", commodity_price = "{}", note_drawer = "{}", seller_addr = "{}",
                commodity_num = "{}", seller_register_num = "{}", remarks = "{}", seller_bank = "{}",
                commodity_tax_rate = "{}", total_tax = "{}", check_code = "{}", invoice_code = "{}", 
                invoice_date = "{}", purchaser_register_num = "{}", invoice_type_org = "{}", password = "{}",
                amount_in_figuers = "{}", purchaser_bank = "{}", checker = "{}", totalAmount = "{}", 
                commodity_amount = "{}", purchaser_name = "{}", commodity_type = "{}", invoice_type = "{}"
                purchaser_addr = "{}", commodity_tax = "{}", commodity_unit = "{}", payee = "{}",
                commodity_name = "{}", seller_name = "{}", invoice_num = "{}", transaction_id = {}
            WHERE id = {}}
                '''.format(content['amount_in_words'], content['commodity_price'], content['note_drawer'], content['seller_addr'],
                           content['commodity_num'], content['seller_register_num'], content['remarks'], content['seller_bank'],
                           content['commodity_tax_rate'], content['total_tax'], content['check_code'], content['invoice_code'],
                           content['invoice_date'], content['purchaser_register_num'], content['invoice_type_org'], content['password'],
                           content['amount_in_figuers'], content['purchaser_bank'], content['checker'], content['totalAmount'],
                           content['commodity_amount'], content['purchaser_name'], content['commodity_type'], content['invoice_type'],
                           content['purchaser_addr'], content['commodity_tax'], content['commodity_unit'], content['payee'],
                           content['commodity_name'], content['seller_name'], content['invoice_num'], content['transaction_id'],
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

