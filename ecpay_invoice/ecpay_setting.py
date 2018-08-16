#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib
import hashlib
import requests


#  執行發票作業項目。
class EcpayInvoiceMethod():
    # 一般開立發票。

    INVOICE = 'INVOICE'

    # 延遲或觸發開立發票。

    INVOICE_DELAY = 'INVOICE_DELAY'

    # 開立折讓。

    ALLOWANCE = 'ALLOWANCE'
    # 發票作廢。

    INVOICE_VOID = 'INVOICE_VOID'

    # 折讓作廢。

    ALLOWANCE_VOID = 'ALLOWANCE_VOID'

    # 查詢發票。

    INVOICE_SEARCH = 'INVOICE_SEARCH'

    # 查詢作廢發票。

    INVOICE_VOID_SEARCH = 'INVOICE_VOID_SEARCH'

    # 查詢折讓明細。

    ALLOWANCE_SEARCH = 'ALLOWANCE_SEARCH'

    # 查詢折讓作廢明細。

    ALLOWANCE_VOID_SEARCH = 'ALLOWANCE_VOID_SEARCH'

    # 發送通知。

    INVOICE_NOTIFY = 'INVOICE_NOTIFY'

    # 付款完成觸發或延遲開立發票。

    INVOICE_TRIGGER = 'INVOICE_TRIGGER'

    # 手機條碼驗證。

    CHECK_MOBILE_BARCODE = 'CHECK_MOBILE_BARCODE'

    # 愛心碼驗證。

    CHECK_LOVE_CODE = 'CHECK_LOVE_CODE'


# 電子發票載具類別
class EcpayCarruerType():
    # 無載具

    No = ''

    # 會員載具

    Member = '1'

    # 買受人自然人憑證

    Citizen = '2'

    # 買受人手機條碼

    Cellphone = '3'


# 電子發票列印註記
class EcpayPrintMark():
    # 不列印

    No = '0'

    # 列印

    Yes = '1'


# 電子發票捐贈註記
class EcpayDonation():
    # 捐贈

    Yes = '1'

    # 不捐贈

    No = '0'


# 通關方式
class EcpayClearanceMark():
    # 經海關出口

    Yes = '1'

    # 非經海關出口

    No = '2'


# 課稅類別
class EcpayTaxType():
    # 應稅

    Dutiable = '1'

    # 零稅率

    Zero = '2'

    # 免稅

    Free = '3'

    # 應稅與免稅混合(限收銀機發票無法分辦時使用，且需通過申請核可)

    Mix = '9'


# 字軌類別
class EcpayInvType():
    # 一般稅額

    General = '07'

    # 特種稅額

    Special = '08'


# 商品單價是否含稅
class EcpayVatType():
    # 商品單價含稅價

    Yes = '1'

    # 商品單價未稅價

    No = '0'


# 延遲註記
class EcpayDelayFlagType():
    # 延遲註記

    Delay = '1'

    # 觸發註記

    Trigger = '2'


# 交易類別
class EcpayPayTypeCategory():
    # ECPAY

    Ecpay = '2'


# 通知類別
class EcpayAllowanceNotifyType():
    # 簡訊通知

    Sms = 'S'

    # 電子郵件通知

    Email = 'E'

    # 皆通知

    All = 'A'

    # 皆不通知

    No = 'N'


# 發送方式
class EcpayNotifyType():
    # 簡訊通知

    Sms = 'S'

    # 電子郵件通知

    Email = 'E'

    # 皆通知

    All = 'A'


# 發送內容類型
class EcpayInvoiceTagType():
    # 發票開立

    Invoice = 'I'

    # 發票作廢

    Invoice_Void = 'II'

    # 折讓開立

    Allowance = 'A'

    # 折讓作廢

    Allowance_Void = 'AI'

    # 發票中獎

    Invoice_Winning = 'AW'


# 發送對象
class EcpayNotifiedType():
    # 通知客戶

    Customer = 'C'

    # 通知廠商

    vendor = 'M'

    # 皆發送

    All = 'A'


# 加密類型
class ECPay_EncryptType():
    # MD5(預設)

    ENC_MD5 = 0

    # SHA256

    ENC_SHA256 = 1


class ECPay_IO():

    @staticmethod
    def ServerPost(parameters, ServiceURL):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        sSend_Info = ''

        # 組合字串
        for key, val in parameters.items():
            if sSend_Info == '':
                sSend_Info += key + '=' + str(val)
            else:
                sSend_Info += '&' + key + '=' + str(val)

        r = requests.post(ServiceURL, data=sSend_Info, headers=headers)
        return r.text


class ECPay_CheckMacValue():
    '''
    *產生檢查碼
    '''

    @staticmethod
    def generate(arParameters=dict, HashKey='', HashIV='', encType=0):
        sMacValue = ''
        if arParameters:
            if 'CheckMacValue' in arParameters:
                del arParameters['CheckMacValue']

            sorted_str = 'HashKey=' + HashKey

            for key in sorted(arParameters.keys(), key=str.lower):
                sorted_str += '&' + key + '=' + str(arParameters[key])

            sorted_str += '&HashIV=' + HashIV

            sMacValue = urllib.parse.quote_plus(sorted_str)

            # 轉成小寫
            sMacValue = sMacValue.lower()

            # 取代為與 dotNet 相符的字元
            sMacValue = ECPay_CheckMacValue.do_str_replace(sMacValue)

            # 編碼
            if encType == ECPay_EncryptType.ENC_SHA256:
                sMacValue = hashlib.sha256(sMacValue.encode('utf-8')).hexdigest()  # SHA256 編碼
            else:
                sMacValue = hashlib.md5(sMacValue.encode('utf-8')).hexdigest()  # MD5 編碼

            # 轉成大寫
            sMacValue = sMacValue.upper()

            return sMacValue

    @staticmethod
    def restore_str_replace(string):
        mapping_dict = {'!': '%21', '*': '%2a', '(': '%28', ')': '%29'}
        for key, val in mapping_dict.items():
            string = string.replace(key, val)

        return string

    @staticmethod
    def do_str_replace(string):
        mapping_dict = {'!': '%21', '*': '%2a', '(': '%28', ')': '%29', '/': '%2F'}
        for key, val in mapping_dict.items():
            string = string.replace(val, key)

        return string
