#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
* 一般開立發票，範例程式
* 除了*SalesAmount與*TimeStamp 為int，其他參數皆為字串
'''

# 1.載入SDK程式與建立物件
import random
from ecpay_invoice.ecpay_main import *

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
    'ItemPrice': 50,
    'ItemTaxType': '',
    'ItemAmount': 50,
    'ItemRemark': '商品備註一'
})
ecpay_invoice.Send['Items'].append({
    'ItemName': '商品名稱二',
    'ItemCount': 1,
    'ItemWord': '批',
    'ItemPrice': 150,
    'ItemTaxType': '',
    'ItemAmount': 150,
    'ItemRemark': '商品備註二'
})
ecpay_invoice.Send['Items'].append({
    'ItemName': '商品名稱三',
    'ItemCount': 1,
    'ItemWord': '批',
    'ItemPrice': 200,
    'ItemTaxType': '',
    'ItemAmount': 200,
    'ItemRemark': '商品備註三'
})

RelateNumber = 'ECPAY' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + str(
random.randint(1000000000, 2147483647))  # 產生測試用自訂訂單編號
ecpay_invoice.Send['RelateNumber'] = RelateNumber
ecpay_invoice.Send['CustomerID'] = ''
ecpay_invoice.Send['CustomerIdentifier'] = ''
ecpay_invoice.Send['CustomerName'] = '測試名稱'
ecpay_invoice.Send['CustomerAddr'] = '測試地址'
ecpay_invoice.Send['CustomerPhone'] = ''
ecpay_invoice.Send['CustomerEmail'] = 'test@local.com'
ecpay_invoice.Send['ClearanceMark'] = ''
ecpay_invoice.Send['Print'] = '0'
ecpay_invoice.Send['Donation'] = '0'
ecpay_invoice.Send['LoveCode'] = ''
ecpay_invoice.Send['CarruerType'] = '3'
ecpay_invoice.Send['CarruerNum'] = '/00-1688'
ecpay_invoice.Send['TaxType'] = '1'
ecpay_invoice.Send['SalesAmount'] = 400
ecpay_invoice.Send['InvoiceRemark'] = 'SDK TEST Python V1.0.5'
ecpay_invoice.Send['InvType'] = '07'
ecpay_invoice.Send['vat'] = ''

# 4. 送出
aReturn_Info = ecpay_invoice.Check_Out()

# 5. 返回
print 'RelateNumber：' + str(RelateNumber)
print aReturn_Info
print aReturn_Info['RtnMsg']
print '發票號碼：' + aReturn_Info['InvoiceNumber']

