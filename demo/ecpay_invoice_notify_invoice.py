#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
* 發送通知，範例程式
'''

# 1.載入SDK程式與建立物件
from ecpay_invoice.ecpay_main import *

ecpay_invoice = EcpayInvoice()

# 2.寫入基本介接參數
ecpay_invoice.Invoice_Method = 'INVOICE_NOTIFY'
ecpay_invoice.Invoice_Url = 'https://einvoice-stage.ecpay.com.tw/Notify/InvoiceNotify'
ecpay_invoice.MerchantID = '2000132'
ecpay_invoice.HashKey = 'ejCk326UnaZWKisg'
ecpay_invoice.HashIV = 'q9jcZX8Ib9LM8wYk'

# 3.寫入發票相關資訊
ecpay_invoice.Send['InvoiceNo'] = 'FY10004004' # 發票號碼
ecpay_invoice.Send['NotifyMail'] = 'demo@local.com' # 發送電子信箱
ecpay_invoice.Send['Notify'] = 'E' # 發送方式
ecpay_invoice.Send['InvoiceTag'] = 'I' # 發送內容類型
ecpay_invoice.Send['Notified'] = 'C'

# 4. 送出
aReturn_Info = ecpay_invoice.Check_Out()
# 5. 返回
print aReturn_Info
print aReturn_Info['RtnMsg']
