#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
* 開立折讓，範例程式
'''

# 1.載入SDK程式與建立物件
from ecpay_invoice.ecpay_main import *
import time
import random

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
    'ItemTaxType': '1',
    'ItemAmount': 100,
    'ItemRemark': '商品備註一'
})

RelateNumber = 'ECPAY' + time.strftime("%Y%m%d%H%M%S", time.localtime()) +\
   str(random.randint(1000000000, 2147483647))  # 產生測試用自訂訂單編號
ecpay_invoice.Send['CustomerName'] = '測試名稱'
ecpay_invoice.Send['InvoiceNo'] = 'FY10004005'
ecpay_invoice.Send['AllowanceNotify'] = 'E'
ecpay_invoice.Send['NotifyMail'] = 'test@localhost.com'
ecpay_invoice.Send['NotifyPhone'] = '097897'
ecpay_invoice.Send['AllowanceAmount'] = 100

# 4. 送出
aReturn_Info = ecpay_invoice.Check_Out()
# 5. 返回
print 'RelateNumber：' + str(RelateNumber)
print aReturn_Info
print aReturn_Info['RtnMsg']
print '折讓編號：'+ aReturn_Info['IA_Allow_No']