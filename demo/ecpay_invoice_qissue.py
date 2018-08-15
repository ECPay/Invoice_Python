#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
* 查詢一般發票，範例程式
'''

# 1.載入SDK程式與建立物件
from ecpay_invoice.ecpay_main import *

ecpay_invoice = EcpayInvoice()

# 2.寫入基本介接參數
ecpay_invoice.Invoice_Method = 'INVOICE_SEARCH'  # 請見16.1操作發票功能類別
ecpay_invoice.Invoice_Url = 'https://einvoice-stage.ecpay.com.tw/Query/Issue'
ecpay_invoice.MerchantID = '2000132'
ecpay_invoice.HashKey = 'ejCk326UnaZWKisg'
ecpay_invoice.HashIV = 'q9jcZX8Ib9LM8wYk'

# 3.寫入發票相關資訊
ecpay_invoice.Send['RelateNumber'] = 'SocialOrder320180716015434'#  廠商自訂編號

# 4. 送出
aReturn_Info = ecpay_invoice.Check_Out()
# 5. 返回
print aReturn_Info
print aReturn_Info['RtnMsg']
