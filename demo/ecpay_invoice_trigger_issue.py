#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
* 付款完成觸發或延遲開立發票，範例程式
'''

# 1.載入SDK程式與建立物件
from ecpay_invoice.ecpay_main import *

ecpay_invoice = EcpayInvoice()

# 2.寫入基本介接參數
ecpay_invoice.Invoice_Method = 'INVOICE_TRIGGER'
ecpay_invoice.Invoice_Url = 'https://einvoice-stage.ecpay.com.tw/Invoice/TriggerIssue'
ecpay_invoice.MerchantID = '2000132'
ecpay_invoice.HashKey = 'ejCk326UnaZWKisg'
ecpay_invoice.HashIV = 'q9jcZX8Ib9LM8wYk'

# 3.寫入發票相關資訊
ecpay_invoice.Send['Tsr'] = 'ECPAY201807161533501566047166' # 交易單號
ecpay_invoice.Send['PayType'] = '2'        # 交易類別

# 4. 送出
aReturn_Info = ecpay_invoice.Check_Out()
print aReturn_Info
print aReturn_Info['RtnMsg']
