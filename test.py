#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ecpay_invoice.ecpay_main import *

import time
import random

def test_normal_invoice():
    ecpay_invoice = EcpayInvoice()


    # 2.寫入基本介接參數
    ecpay_invoice.Invoice_Method = 'INVOICE'
    ecpay_invoice.Invoice_Url = 'https://einvoice-stage.ecpay.com.tw/Invoice/Issue'
    ecpay_invoice.MerchantID = '2000132'
    ecpay_invoice.HashKey = 'ejCk326UnaZWKisg'
    ecpay_invoice.HashIV = 'q9jcZX8Ib9LM8wYk'

    # 3.寫入發票相關資訊

    # 商品資訊
    ecpay_invoice.Send['Items'].append({
        'ItemName': '商品名稱一',
        'ItemCount': 10,
        'ItemWord': '批',
        'ItemPrice': 0.5,
        'ItemTaxType': '1',
        'ItemAmount': 5,
        'ItemRemark': '商品備註一'
    })
    ecpay_invoice.Send['Items'].append({
        'ItemName': '商品名稱二',
        'ItemCount': 1,
        'ItemWord': '批',
        'ItemPrice': 150,
        'ItemTaxType': '1',
        'ItemAmount': 150,
        'ItemRemark': '商品備註二'
    })
    ecpay_invoice.Send['Items'].append({
        'ItemName': '商品名稱三',
        'ItemCount': 1,
        'ItemWord': '批',
        'ItemPrice': 200,
        'ItemTaxType': '1',
        'ItemAmount': 200,
        'ItemRemark': '商品備註三'
    })

    RelateNumber = 'ECPAY' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + str(
        random.randint(1000000000, 2147483647))  # 產生測試用自訂訂單編號
    ecpay_invoice.Send['RelateNumber'] = RelateNumber
    ecpay_invoice.Send['CustomerID'] = ''
    ecpay_invoice.Send['CustomerIdentifier'] = ''
    ecpay_invoice.Send['CustomerName'] = ''
    ecpay_invoice.Send['CustomerAddr'] = ''
    ecpay_invoice.Send['CustomerPhone'] = ''
    ecpay_invoice.Send['CustomerEmail'] = 'test@local.com'
    ecpay_invoice.Send['ClearanceMark'] = ''
    ecpay_invoice.Send['Print'] = '0'
    ecpay_invoice.Send['Donation'] = '0'
    ecpay_invoice.Send['LoveCode'] = ''
    ecpay_invoice.Send['CarruerType'] = ''
    ecpay_invoice.Send['CarruerNum'] = ''
    ecpay_invoice.Send['TaxType'] = '1'
    ecpay_invoice.Send['SalesAmount'] = 355
    ecpay_invoice.Send['InvoiceRemark'] = 'SDK TEST Python V1.0.5'
    ecpay_invoice.Send['InvType'] = '07'
    ecpay_invoice.Send['vat'] = ''

    # 4. 送出
    aReturn_Info = ecpay_invoice.Check_Out()
    print 'RelateNumber：' + str(RelateNumber)
    print aReturn_Info
    print aReturn_Info['RtnMsg']
    print '發票號碼：' + aReturn_Info['InvoiceNumber']
    assert aReturn_Info['RtnMsg'] == '開立發票成功'


def test_offline_normal_invoice():
    ecpay_invoice = EcpayInvoice()

    # 2.寫入基本介接參數
    ecpay_invoice.Invoice_Method = 'INVOICE'
    ecpay_invoice.Invoice_Url = 'https://einvoice-stage.ecpay.com.tw/Invoice/Issue'
    ecpay_invoice.MerchantID = '2000132'
    ecpay_invoice.HashKey = 'ejCk326UnaZWKisg'
    ecpay_invoice.HashIV = 'q9jcZX8Ib9LM8wYk'

    # 3.寫入發票相關資訊

    # 商品資訊
    ecpay_invoice.Send['Items'].append({
        'ItemName': '商品名稱一',
        'ItemCount': 1,
        'ItemWord': '批',
        'ItemPrice': 100,
        'ItemTaxType': '1',
        'ItemAmount': 100,
        'ItemRemark': '商品備註一'
    })
    ecpay_invoice.Send['Items'].append({
        'ItemName': '商品名稱二',
        'ItemCount': 1,
        'ItemWord': '批',
        'ItemPrice': 150,
        'ItemTaxType': '1',
        'ItemAmount': 150,
        'ItemRemark': '商品備註二'
    })
    ecpay_invoice.Send['Items'].append({
        'ItemName': '商品名稱三',
        'ItemCount': 1,
        'ItemWord': '批',
        'ItemPrice': 250,
        'ItemTaxType': '1',
        'ItemAmount': 250,
        'ItemRemark': '商品備註三'
    })

    RelateNumber = 'ECPAY' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + str(random.randint(1000000000, 2147483647))  # 產生測試用自訂訂單編號
    ecpay_invoice.Send['RelateNumber'] = RelateNumber
    ecpay_invoice.Send['CustomerID'] = ''
    ecpay_invoice.Send['CustomerIdentifier'] = ''
    ecpay_invoice.Send['CustomerName'] = 'test'
    ecpay_invoice.Send['CustomerAddr'] = 'test'
    ecpay_invoice.Send['CustomerPhone'] = ''
    ecpay_invoice.Send['CustomerEmail'] = 'test@abc.com'
    ecpay_invoice.Send['ClearanceMark'] = ''
    ecpay_invoice.Send['Print'] = '0'
    ecpay_invoice.Send['Donation'] = '0'
    ecpay_invoice.Send['LoveCode'] = ''
    ecpay_invoice.Send['CarruerType'] = ''
    ecpay_invoice.Send['CarruerNum'] = ''
    ecpay_invoice.Send['TaxType'] = '1'
    ecpay_invoice.Send['SalesAmount'] = 500
    ecpay_invoice.Send['InvoiceRemark'] = 'SDK TEST Python V1.0.5'
    ecpay_invoice.Send['InvType'] = '07'
    ecpay_invoice.Send['vat'] = ''
    ecpay_invoice.Send['OnLine'] = False

    # 4. 送出
    aReturn_Info = ecpay_invoice.Check_Out()
    print 'RelateNumber：' + str(RelateNumber)
    print aReturn_Info

    print aReturn_Info['RtnMsg']
    print '發票號碼' + aReturn_Info['InvoiceNumber']
    assert aReturn_Info['RtnMsg'] == '開立發票成功'


def test_delay_invoice():
    ecpay_invoice = EcpayInvoice()

    # 2.寫入基本介接參數
    ecpay_invoice.Invoice_Method = 'INVOICE_DELAY'
    ecpay_invoice.Invoice_Url = 'https://einvoice-stage.ecpay.com.tw/Invoice/DelayIssue'
    ecpay_invoice.MerchantID = '2000132'
    ecpay_invoice.HashKey = 'ejCk326UnaZWKisg'
    ecpay_invoice.HashIV = 'q9jcZX8Ib9LM8wYk'

    # 3.寫入發票相關資訊

    # 商品資訊
    ecpay_invoice.Send['Items'].append({
        'ItemName': '商品名稱一',
        'ItemCount': 1,
        'ItemWord': '批',
        'ItemPrice': 100,
        'ItemTaxType': '1',
        'ItemAmount': 100,
        'ItemRemark': '商品備註一'
    })
    ecpay_invoice.Send['Items'].append({
        'ItemName': '商品名稱二',
        'ItemCount': 2,
        'ItemWord': '件',
        'ItemPrice': 200,
        'ItemTaxType': '1',
        'ItemAmount': 400,
        'ItemRemark': '商品備註二'
    })

    RelateNumber = 'ECPAY' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + str(random.randint(1000000000, 2147483647))  # 產生測試用自訂訂單編號
    ecpay_invoice.Send['RelateNumber'] = RelateNumber
    ecpay_invoice.Send['CustomerID'] = ''
    ecpay_invoice.Send['CustomerIdentifier'] = ''
    ecpay_invoice.Send['CustomerName'] = ''
    ecpay_invoice.Send['CustomerAddr'] = ''
    ecpay_invoice.Send['CustomerPhone'] = ''
    ecpay_invoice.Send['CustomerEmail'] = 'test@localhost.com'
    ecpay_invoice.Send['ClearanceMark'] = ''
    ecpay_invoice.Send['Print'] = '0'
    ecpay_invoice.Send['Donation'] = '0'
    ecpay_invoice.Send['LoveCode'] = ''
    ecpay_invoice.Send['CarruerType'] = ''
    ecpay_invoice.Send['CarruerNum'] = ''
    ecpay_invoice.Send['TaxType'] = '1'
    ecpay_invoice.Send['SalesAmount'] = 500
    ecpay_invoice.Send['InvoiceRemark'] = 'SDK TEST Python V1.0.5'
    ecpay_invoice.Send['InvType'] = '07'
    ecpay_invoice.Send['DelayFlag'] = '1'
    ecpay_invoice.Send['DelayDay'] = '1'
    ecpay_invoice.Send['ECBankID'] = ''
    ecpay_invoice.Send['Tsr'] = RelateNumber
    ecpay_invoice.Send['PayType'] = '2'
    ecpay_invoice.Send['PayAct'] = 'ALLPAY'
    ecpay_invoice.Send['NotifyURL'] = ''

    # 4. 送出
    aReturn_Info = ecpay_invoice.Check_Out()
    print aReturn_Info['OrderNumber']
    print 'RelateNumber：' + str(RelateNumber)
    print aReturn_Info['RtnMsg']
    assert aReturn_Info['RtnMsg'] == '開立延遲發票成功'


def test_allowance():
    ecpay_invoice = EcpayInvoice()

    # 2.寫入基本介接參數
    ecpay_invoice.Invoice_Method = 'ALLOWANCE'
    ecpay_invoice.Invoice_Url = 'https://einvoice-stage.ecpay.com.tw/Invoice/Allowance'
    ecpay_invoice.MerchantID = '2000132'
    ecpay_invoice.HashKey = 'ejCk326UnaZWKisg'
    ecpay_invoice.HashIV = 'q9jcZX8Ib9LM8wYk'

    # 3.寫入發票相關資訊

    # 商品資訊
    ecpay_invoice.Send['Items'].append({
        'ItemName': '商品名稱一',
        'ItemCount': 1,
        'ItemWord': '批',
        'ItemPrice': 100,
        'ItemTaxType': 1,
        'ItemAmount': 100,
        'ItemRemark': '商品備註一'
    })

    RelateNumber = 'ECPAY' + time.strftime("%Y%m%d%H%M%S", time.localtime()) +\
                   str(random.randint(1000000000, 2147483647))  # 產生測試用自訂訂單編號
    ecpay_invoice.Send['CustomerName'] = ''
    ecpay_invoice.Send['InvoiceNo'] = 'FY10004005'
    ecpay_invoice.Send['AllowanceNotify'] = 'E'
    ecpay_invoice.Send['NotifyMail'] = 'test@localhost.com'
    ecpay_invoice.Send['NotifyPhone'] = ''
    ecpay_invoice.Send['AllowanceAmount'] = 100

    # 4. 送出
    aReturn_Info = ecpay_invoice.Check_Out()
    print 'RelateNumber：' + str(RelateNumber)
    print aReturn_Info

    print aReturn_Info['RtnMsg']
    print '折讓編號：'+ aReturn_Info['IA_Allow_No']
    assert aReturn_Info['RtnMsg'] == '成功.'


def test_invoice_void():
    ecpay_invoice = EcpayInvoice()

    # 2.寫入基本介接參數
    ecpay_invoice.Invoice_Method = 'INVOICE_VOID'
    ecpay_invoice.Invoice_Url = 'https://einvoice-stage.ecpay.com.tw/Invoice/IssueInvalid'
    ecpay_invoice.MerchantID = '2000132'
    ecpay_invoice.HashKey = 'ejCk326UnaZWKisg'
    ecpay_invoice.HashIV = 'q9jcZX8Ib9LM8wYk'

    # 3.寫入發票相關資訊
    ecpay_invoice.Send['InvoiceNumber'] = 'FY10004205'
    ecpay_invoice.Send['Reason'] = 'ISSUE INVALID TEST'

    # 4. 送出
    aReturn_Info = ecpay_invoice.Check_Out()
    print aReturn_Info
    print aReturn_Info['RtnMsg']
    assert aReturn_Info['RtnMsg'] == '作廢發票成功'


def test_allowancs_void():
    ecpay_invoice = EcpayInvoice()

    # 2.寫入基本介接參數
    ecpay_invoice.Invoice_Method = 'ALLOWANCE_VOID'
    ecpay_invoice.Invoice_Url = 'https://einvoice-stage.ecpay.com.tw/Invoice/AllowanceInvalid'
    ecpay_invoice.MerchantID = '2000132'
    ecpay_invoice.HashKey = 'ejCk326UnaZWKisg'
    ecpay_invoice.HashIV = 'q9jcZX8Ib9LM8wYk'

    # 3.寫入發票相關資訊
    ecpay_invoice.Send['InvoiceNo'] = 'FY10004005'
    ecpay_invoice.Send['Reason'] = '錯開'
    ecpay_invoice.Send['AllowanceNo'] = '2018071615286810'

    # 4. 送出
    aReturn_Info = ecpay_invoice.Check_Out()
    print aReturn_Info
    print aReturn_Info['RtnMsg']
    assert aReturn_Info['RtnMsg'] == '成功.'


def test_qissue_invoice():
    ecpay_invoice = EcpayInvoice()

    # 2.寫入基本介接參數
    ecpay_invoice.Invoice_Method = 'INVOICE_SEARCH'
    ecpay_invoice.Invoice_Url = 'https://einvoice-stage.ecpay.com.tw/Query/Issue'
    ecpay_invoice.MerchantID = '2000132'
    ecpay_invoice.HashKey = 'ejCk326UnaZWKisg'
    ecpay_invoice.HashIV = 'q9jcZX8Ib9LM8wYk'

    # 3.寫入發票相關資訊
    ecpay_invoice.Send['RelateNumber'] = 'SocialOrder320180716015434'

    # 4. 送出
    aReturn_Info = ecpay_invoice.Check_Out()
    print aReturn_Info
    print aReturn_Info['RtnMsg']
    assert aReturn_Info['RtnMsg'] == '查詢發票成功'


def test_qissue_void():
    ecpay_invoice = EcpayInvoice()

    # 2.寫入基本介接參數
    ecpay_invoice.Invoice_Method = 'INVOICE_VOID_SEARCH'
    ecpay_invoice.Invoice_Url = 'https://einvoice-stage.ecpay.com.tw/Query/IssueInvalid'
    ecpay_invoice.MerchantID = '2000132'
    ecpay_invoice.HashKey = 'ejCk326UnaZWKisg'
    ecpay_invoice.HashIV = 'q9jcZX8Ib9LM8wYk'

    # 3.寫入發票相關資訊
    ecpay_invoice.Send['RelateNumber'] = 'ECPAY201807161524431519428107'

    # 4. 送出
    aReturn_Info = ecpay_invoice.Check_Out()
    print aReturn_Info
    print aReturn_Info['RtnMsg']
    assert aReturn_Info['RtnMsg'] == '查詢作廢發票成功'


def test_qallowance():

    ecpay_invoice = EcpayInvoice()

    # 2.寫入基本介接參數
    ecpay_invoice.Invoice_Method = 'ALLOWANCE_SEARCH'
    ecpay_invoice.Invoice_Url = 'https://einvoice-stage.ecpay.com.tw/Query/Allowance'
    ecpay_invoice.MerchantID = '2000132'
    ecpay_invoice.HashKey = 'ejCk326UnaZWKisg'
    ecpay_invoice.HashIV = 'q9jcZX8Ib9LM8wYk'

    # 3.寫入發票相關資訊
    ecpay_invoice.Send['InvoiceNo'] = 'FY10004005'
    ecpay_invoice.Send['AllowanceNo'] = '2018071615286810'

    # 4. 送出
    aReturn_Info = ecpay_invoice.Check_Out()
    print aReturn_Info
    print aReturn_Info['RtnMsg']
    assert aReturn_Info['RtnMsg'] == '成功.'


def test_qallowance_void():
    ecpay_invoice = EcpayInvoice()

    # 2.寫入基本介接參數
    ecpay_invoice.Invoice_Method = 'ALLOWANCE_VOID_SEARCH'
    ecpay_invoice.Invoice_Url = 'https://einvoice-stage.ecpay.com.tw/Query/AllowanceInvalid'
    ecpay_invoice.MerchantID = '2000132'
    ecpay_invoice.HashKey = 'ejCk326UnaZWKisg'
    ecpay_invoice.HashIV = 'q9jcZX8Ib9LM8wYk'

    # 3.寫入發票相關資訊
    ecpay_invoice.Send['InvoiceNo'] = 'FY10004005'
    ecpay_invoice.Send['AllowanceNo'] = '2018071615286810'

    # 4. 送出
    aReturn_Info = ecpay_invoice.Check_Out()
    print aReturn_Info
    print aReturn_Info['RtnMsg']
    assert aReturn_Info['RtnMsg'] == '成功.'


def test_invoice_notify():
    ecpay_invoice = EcpayInvoice()

    # 2.寫入基本介接參數
    ecpay_invoice.Invoice_Method = 'INVOICE_NOTIFY'
    ecpay_invoice.Invoice_Url = 'https://einvoice-stage.ecpay.com.tw/Notify/InvoiceNotify'
    ecpay_invoice.MerchantID = '2000132'
    ecpay_invoice.HashKey = 'ejCk326UnaZWKisg'
    ecpay_invoice.HashIV = 'q9jcZX8Ib9LM8wYk'

    # 3.寫入發票相關資訊
    ecpay_invoice.Send['InvoiceNo'] = 'FY10004004' # 發票號碼
    ecpay_invoice.Send['NotifyMail'] = 'skypc785308@gmal.com' # 發送電子信箱
    ecpay_invoice.Send['Notify'] = 'E' # 發送方式
    ecpay_invoice.Send['InvoiceTag'] = 'I' # 發送內容類型
    ecpay_invoice.Send['Notified'] = 'C'

    # 4. 送出
    aReturn_Info = ecpay_invoice.Check_Out()
    print aReturn_Info
    print aReturn_Info['RtnMsg']
    assert aReturn_Info['RtnMsg'] == '成功.'


def test_invoice_trigger_issue():
    ecpay_invoice = EcpayInvoice()

    # 2.寫入基本介接參數
    ecpay_invoice.Invoice_Method = 'INVOICE_TRIGGER'
    ecpay_invoice.Invoice_Url = 'https://einvoice-stage.ecpay.com.tw/Invoice/TriggerIssue'
    ecpay_invoice.MerchantID = '2000132'
    ecpay_invoice.HashKey = 'ejCk326UnaZWKisg'
    ecpay_invoice.HashIV = 'q9jcZX8Ib9LM8wYk'

    # 3.寫入發票相關資訊
    ecpay_invoice.Send['Tsr'] = 'ECPAY201807161533501566047166'
    ecpay_invoice.Send['PayType'] = '2'

    # 4. 送出
    aReturn_Info = ecpay_invoice.Check_Out()
    print aReturn_Info
    print aReturn_Info['RtnMsg']
    assert aReturn_Info['RtnMsg'] == '延後開立成功'


def test_check_mobile_barcode():
    ecpay_invoice = EcpayInvoice()

    # 2.寫入基本介接參數
    ecpay_invoice.Invoice_Method = 'CHECK_MOBILE_BARCODE'
    ecpay_invoice.Invoice_Url = 'https://einvoice-stage.ecpay.com.tw/Query/CheckMobileBarCode'
    ecpay_invoice.MerchantID = '2000132'
    ecpay_invoice.HashKey = 'ejCk326UnaZWKisg'
    ecpay_invoice.HashIV = 'q9jcZX8Ib9LM8wYk'

    # 3.寫入發票相關資訊
    ecpay_invoice.Send['BarCode'] = '/RXNOFER'

    # 4. 送出
    aReturn_Info = ecpay_invoice.Check_Out()
    print aReturn_Info
    print aReturn_Info['RtnMsg']
    assert aReturn_Info['RtnMsg'] == '執行成功'


def test_check_love_code():
    ecpay_invoice = EcpayInvoice()

    # 2.寫入基本介接參數
    ecpay_invoice.Invoice_Method = 'CHECK_LOVE_CODE'
    ecpay_invoice.Invoice_Url = 'https://einvoice-stage.ecpay.com.tw/Query/CheckLoveCode'
    ecpay_invoice.MerchantID = '2000132'
    ecpay_invoice.HashKey = 'ejCk326UnaZWKisg'
    ecpay_invoice.HashIV = 'q9jcZX8Ib9LM8wYk'

    # 3.寫入發票相關資訊
    ecpay_invoice.Send['LoveCode'] = '51919'

    # 4. 送出
    aReturn_Info = ecpay_invoice.Check_Out()
    print aReturn_Info
    print aReturn_Info['RtnMsg']
    assert aReturn_Info['RtnMsg'] == '執行成功'