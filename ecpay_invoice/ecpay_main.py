#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time

from ecpay_invoice.ecpay_setting import *


class EcpayInvoice():
    TimeStamp = ''
    MerchantID = ''
    HashKey = ''
    HashIV = ''
    Send = 'Send'
    Invoice_Method = 'INVOICE'  # 電子發票執行項目
    Invoice_Url = 'Invoice_Url'  # 電子發票執行網址

    def __init__(self):
        self.Send = dict()
        self.Send['RelateNumber'] = ''
        self.Send['CustomerID'] = ''
        self.Send['CustomerIdentifier'] = ''
        self.Send['CustomerName'] = ''
        self.Send['CustomerAddr'] = ''
        self.Send['CustomerPhone'] = ''
        self.Send['CustomerEmail'] = ''
        self.Send['ClearanceMark'] = ''
        self.Send['Print'] = EcpayPrintMark.No
        self.Send['Donation'] = EcpayDonation.No
        self.Send['LoveCode'] = ''
        self.Send['CarruerType'] = ''
        self.Send['CarruerNum'] = ''
        self.Send['TaxType'] = ''
        self.Send['SalesAmount'] = ''
        self.Send['InvoiceRemark'] = ''
        self.Send['Items'] = list()
        self.Send['InvType'] = ''
        self.Send['vat'] = EcpayVatType.Yes
        self.Send['DelayFlag'] = ''
        self.Send['DelayDay'] = 0
        self.Send['Tsr'] = ''
        self.Send['PayType'] = ''
        self.Send['PayAct'] = ''
        self.Send['NotifyURL'] = ''
        self.Send['InvoiceNo'] = ''
        self.Send['AllowanceNotify'] = ''
        self.Send['NotifyMail'] = ''
        self.Send['NotifyPhone'] = ''
        self.Send['AllowanceAmount'] = ''
        self.Send['InvoiceNumber'] = ''
        self.Send['Reason'] = ''
        self.Send['AllowanceNo'] = ''
        self.Send['Phone'] = ''
        self.Send['Notify'] = ''
        self.Send['InvoiceTag'] = ''
        self.Send['Notified'] = ''
        self.Send['BarCode'] = ''
        self.Send['OnLine'] = True
        self.TimeStamp = int(time.time())

    def Check_Out(self):
        arParameters = self.Send.copy()
        arParameters['MerchantID'] = self.MerchantID
        arParameters['TimeStamp'] = self.TimeStamp
        return ECPay_Invoice_Send.CheckOut(arParameters, self.HashKey, self.HashIV, self.Invoice_Method,
                                           self.Invoice_Url)


'''
送出資訊
'''


class ECPay_Invoice_Send():
    # 發票物件
    InvoiceObj = ''
    InvoiceObj_Return = ''

    '''
    背景送出資料
    '''

    @staticmethod
    def CheckOut(arParameters=dict, HashKey='', HashIV='', Invoice_Method='', ServiceURL=''):
        # 發送資訊處理

        arParameters = ECPay_Invoice_Send.process_send(arParameters, HashKey, HashIV, Invoice_Method, ServiceURL)

        szResult = ECPay_IO.ServerPost(arParameters, ServiceURL)
        # 回傳資訊處理
        arParameters_Return = ECPay_Invoice_Send.process_return(szResult, HashKey, HashIV, Invoice_Method)
        return arParameters_Return

    # 資料檢查與過濾(送出)
    @staticmethod
    def process_send(arParameters=dict, HashKey='', HashIV='', Invoice_Method='', ServiceURL=''):
        # 宣告物件
        InvoiceMethod = 'ECPay_' + Invoice_Method
        class_str = globals()[InvoiceMethod]
        InvoiceObj = class_str()
        # 1寫入參數
        arParameters = InvoiceObj.insert_string(arParameters)
        # 2檢查共用參數
        # ECPay_Invoice_Send.check_string(arParameters['MerchantID'], HashKey, HashIV, Invoice_Method, ServiceURL)
        # 3檢查各別參數
        arParameters = InvoiceObj.check_extend_string(arParameters)
        # 4處理需要轉換為urlencode的參數
        arParameters = ECPay_Invoice_Send.urlencode_process(arParameters, InvoiceObj.urlencode_field)
        # 5欄位例外處理方式(送壓碼前)
        arException = InvoiceObj.check_exception(arParameters)
        # 6產生壓碼
        arParameters['CheckMacValue'] = ECPay_Invoice_Send.generate_checkmacvalue(arException,
                                                                                  InvoiceObj.none_verification, HashKey,
                                                                                  HashIV)
        return arParameters

    '''
    資料檢查與過濾(回傳)
    '''

    @staticmethod
    def process_return(sParameters='', HashKey='', HashIV='', Invoice_Method=''):
        # 宣告物件
        InvoiceMethod = 'ECPay_' + Invoice_Method
        class_str = globals()[InvoiceMethod]
        InvoiceObj_Return = class_str()
        # 7字串轉陣列
        arParameters = ECPay_Invoice_Send.string_to_array(sParameters)
        # 8欄位例外處理方式(送壓碼前)
        arException = InvoiceObj_Return.check_exception(arParameters)
        # 9產生壓碼(壓碼檢查)
        if 'CheckMacValue' in arParameters:
            CheckMacValue = ECPay_Invoice_Send.generate_checkmacvalue(arException, InvoiceObj_Return.none_verification,
                                                                      HashKey, HashIV)
            if CheckMacValue != arParameters['CheckMacValue']:
                print('自己壓的：' + CheckMacValue)
                print('系統回傳的：' + arParameters['CheckMacValue'])
                print('注意：壓碼錯誤')
        # 10處理需要urldecode的參數
        arParameters = ECPay_Invoice_Send.urldecode_process(arParameters, InvoiceObj_Return.urlencode_field)
        return arParameters

    '''
    2檢查共同參數
    2019/07/05 client端不驗證資料
    '''

    # @staticmethod
    # def check_string(MerchantID='', HashKey='', HashIV='', Invoice_Method='INVOICE', ServiceURL=''):
    #     arErrors = list()
    #     # 檢查是否傳入動作方式
    #     if Invoice_Method == '' or Invoice_Method == 'Invoice_Method':
    #         arErrors.append('Invoice_Method is required.')
    #     # 檢查是否有傳入MerchantID
    #     if len(MerchantID) == 0:
    #         arErrors.append('MerchantID is required.')
    #     if len(MerchantID) > 10:
    #         arErrors.append('MerchantID max langth as 10.')
    #     # 檢查是否有傳入HashKey
    #     if len(HashKey) == 0:
    #         arErrors.append('HashKey is required.')
    #     # 檢查是否有傳入HashIV
    #     if len(HashIV) == 0:
    #         arErrors.append('HashIV is required.')
    #     # 檢查是否有傳送網址
    #     if len(ServiceURL) == 0:
    #         arErrors.append('Invoice_Url is required.')
    #
    #     if len(arErrors) > 0:
    #         print(' '.join(arErrors))

    '''
    *4處理需要轉換為urlencode的參數
    '''

    @staticmethod
    def urlencode_process(arParameters=dict, urlencode_field=dict):
        for key, val in arParameters.items():
            if key in urlencode_field:
                arParameters[key] = urllib.parse.quote_plus(val)
                arParameters[key] = ECPay_CheckMacValue.do_str_replace(arParameters[key])
        return arParameters

    '''
    *6, 9產生壓碼
    '''

    @staticmethod
    def generate_checkmacvalue(arParameters=dict, none_verification=dict, HashKey='', HashIV=''):

        sub_parameters = arParameters.copy()
        # 過濾不需要壓碼的參數

        for key, val in none_verification.items():
            if key in sub_parameters:
                del sub_parameters[key]

        sCheck_MacValue = ECPay_CheckMacValue.generate(sub_parameters, HashKey, HashIV, ECPay_EncryptType.ENC_MD5)
        return sCheck_MacValue

    '''
    *7字串轉陣列
    '''

    @staticmethod
    def string_to_array(Parameters=''):
        aParameters = dict()
        aParameters_Tmp = list()

        aParameters_Tmp = Parameters.split('&')

        for part in aParameters_Tmp:
            paramName, paramValue = part.split('=', 1)
            aParameters[paramName] = paramValue

        return aParameters

    '''
    *10處理urldecode的參數
    '''

    @staticmethod
    def urldecode_process(arParameters=dict, urlencode_field=dict):
        for key, val in arParameters.items():
            if key in urlencode_field:
                arParameters[key] = ECPay_CheckMacValue.restore_str_replace(arParameters[key])
                arParameters[key] = urllib.parse.unquote_plus(val)
        return arParameters


'''
*  A一般開立 
'''


class ECPay_INVOICE():
    # 所需參數
    parameters = dict({
        'TimeStamp': '',
        'MerchantID': '',
        'RelateNumber': '',
        'CustomerID': '',
        'CustomerIdentifier': '',
        'CustomerName': '',
        'CustomerAddr': '',
        'CustomerPhone': '',
        'CustomerEmail': '',
        'ClearanceMark': '',
        'Print': '',
        'Donation': '',
        'LoveCode': '',
        'CarruerType': '',
        'CarruerNum': '',
        'TaxType': '',
        'SalesAmount': '',
        'InvoiceRemark': '',
        'Items': list(),
        'ItemName': '',
        'ItemCount': '',
        'ItemWord': '',
        'ItemPrice': '',
        'ItemTaxType': '',
        'ItemAmount': '',
        'ItemRemark': '',
        'CheckMacValue': '',
        'InvType': '',
        'vat': '',
        'OnLine': True
    })
    # 需要做urlencode的參數
    urlencode_field = dict({
        'CustomerName': '',
        'CustomerAddr': '',
        'CustomerEmail': '',
        'InvoiceRemark': '',
        'ItemName': '',
        'ItemWord': '',
        'ItemRemark': ''
    })

    # 不需要送壓碼的欄位
    none_verification = dict({
        'InvoiceRemark': '',
        'ItemName': '',
        'ItemWord': '',
        'ItemRemark': '',
        'CheckMacValue': ''
    })

    '''
    *1寫入參數
    '''

    def insert_string(self, arParameters=dict):
        nItems_Count_Total = 0
        nItems_Foreach_Count = 1
        sItemName = ''
        sItemCount = ''
        sItemWord = ''
        sItemPrice = ''
        sItemTaxType = ''
        sItemAmount = ''
        sItemRemark = ''

        # Python特性，需要複製一個字典，不然回修改到原先宣告的字典的key與value
        parameters = self.parameters.copy()

        for key, val in parameters.items():
            if key in arParameters:
                parameters[key] = arParameters[key]
        # 商品資訊組合
        nItems_Count_Total = len(arParameters['Items'])  # 商品總筆數
        if nItems_Count_Total != 0:
            for val2 in arParameters['Items']:
                sItemName += val2['ItemName'] if 'ItemName' in val2 else ''
                sItemCount += str(val2['ItemCount'])
                sItemWord += val2['ItemWord'] if 'ItemWord' in val2 else ''
                sItemPrice += str(val2['ItemPrice'])
                sItemTaxType += str(val2['ItemTaxType']) if 'ItemTaxType' in val2 else ''
                sItemAmount += str(val2['ItemAmount'])
                sItemRemark += val2['ItemRemark'] if 'ItemRemark' in val2 else ''

                if nItems_Foreach_Count < nItems_Count_Total:
                    sItemName += '|'
                    sItemCount += '|'
                    sItemWord += '|'
                    sItemPrice += '|'
                    sItemTaxType += '|'
                    sItemAmount += '|'
                    sItemRemark += '|'
                nItems_Foreach_Count += 1
        parameters['ItemName'] = sItemName  # 商品名稱
        parameters['ItemCount'] = sItemCount
        parameters['ItemWord'] = sItemWord  # 商品單位
        parameters['ItemPrice'] = sItemPrice
        parameters['ItemTaxType'] = sItemTaxType
        parameters['ItemAmount'] = sItemAmount
        parameters['ItemRemark'] = sItemRemark  # 商品備註
        return parameters

    '''
    *2 - 2驗證參數格式
    '''

    def check_extend_string(self, arParameters=dict):

        # 刪除items
        del arParameters['Items']
        # 刪除SDK自訂義參數
        del arParameters['OnLine']

        return arParameters

    '''
    *4欄位例外處理方式(送壓碼前)
    '''

    def check_exception(self, arParameters=dict):
        if 'CarruerNum' in arParameters:
            # 載具編號內包含 + 號則改為空白
            arParameters['CarruerNum'] = arParameters['CarruerNum'].replace('+', ' ')
        return arParameters


'''
*  B延遲開立
'''


class ECPay_INVOICE_DELAY():
    # 所需參數
    parameters = dict({
        'TimeStamp': '',
        'MerchantID': '',
        'RelateNumber': '',
        'CustomerID': '',
        'CustomerIdentifier': '',
        'CustomerName': '',
        'CustomerAddr': '',
        'CustomerPhone': '',
        'CustomerEmail': '',
        'ClearanceMark': '',
        'Print': '',
        'Donation': '',
        'LoveCode': '',
        'CarruerType': '',
        'CarruerNum': '',
        'TaxType': '',
        'SalesAmount': '',
        'InvoiceRemark': '',
        'Items': list(),
        'ItemName': '',
        'ItemCount': '',
        'ItemWord': '',
        'ItemPrice': '',
        'ItemTaxType': '',
        'ItemAmount': '',
        'CheckMacValue': '',
        'InvType': '',
        'DelayFlag': '',
        'DelayDay': '',
        'Tsr': '',
        'PayType': '2',
        'PayAct': 'ECPAY',
        'NotifyURL': ''
    })
    # 需要做urlencode的參數
    urlencode_field = dict({
        'CustomerName': '',
        'CustomerAddr': '',
        'CustomerEmail': '',
        'InvoiceRemark': '',
        'ItemName': '',
        'ItemWord': '',
        'ItemRemark': ''
    })

    # 不需要送壓碼的欄位
    none_verification = dict({
        'InvoiceRemark': '',
        'ItemName': '',
        'ItemWord': '',
        'CheckMacValue': ''
    })

    '''
    *1寫入參數
    '''

    def insert_string(self, arParameters=dict):
        nItems_Count_Total = 0
        nItems_Foreach_Count = 1
        sItemName = ''
        sItemCount = ''
        sItemWord = ''
        sItemPrice = ''
        sItemTaxType = ''
        sItemAmount = ''

        # Python特性，需要複製一個字典，不然回修改到原先宣告的字典的key與value
        parameters = self.parameters.copy()

        for key, val in parameters.items():
            if key in arParameters:
                parameters[key] = arParameters[key]
        # 商品資訊組合
        nItems_Count_Total = len(arParameters['Items'])  # 商品總筆數
        if nItems_Count_Total != 0:
            for val2 in arParameters['Items']:
                sItemName += val2['ItemName'] if 'ItemName' in val2 else ''
                sItemCount += str(val2['ItemCount'])
                sItemWord += val2['ItemWord'] if 'ItemWord' in val2 else ''
                sItemPrice += str(val2['ItemPrice'])
                sItemTaxType += str(val2['ItemTaxType']) if 'ItemTaxType' in val2 else ''
                sItemAmount += str(val2['ItemAmount'])

                if nItems_Foreach_Count < nItems_Count_Total:
                    sItemName += '|'
                    sItemCount += '|'
                    sItemWord += '|'
                    sItemPrice += '|'
                    sItemTaxType += '|'
                    sItemAmount += '|'

                nItems_Foreach_Count += 1
        parameters['ItemName'] = sItemName  # 商品名稱
        parameters['ItemCount'] = sItemCount
        parameters['ItemWord'] = sItemWord  # 商品單位
        parameters['ItemPrice'] = sItemPrice
        parameters['ItemTaxType'] = sItemTaxType
        parameters['ItemAmount'] = sItemAmount
        return parameters

    '''
    *2 - 2驗證參數格式
    '''

    def check_extend_string(self, arParameters=dict):

        # 刪除items
        del arParameters['Items']

        return arParameters

    '''
    *4欄位例外處理方式(送壓碼前)
    '''

    def check_exception(self, arParameters=dict):
        if 'CarruerNum' in arParameters:
            # 載具編號內包含 + 號則改為空白
            arParameters['CarruerNum'] = arParameters['CarruerNum'].replace('+', ' ')
        return arParameters


'''
*  C開立折讓
'''


class ECPay_ALLOWANCE():
    # 所需參數
    parameters = dict({
        'TimeStamp': '',
        'MerchantID': '',
        'CustomerName': '',
        'Items': list(),
        'ItemName': '',
        'ItemCount': '',
        'ItemWord': '',
        'ItemPrice': '',
        'ItemTaxType': '',
        'ItemAmount': '',
        'CheckMacValue': '',
        'InvoiceNo': '',
        'AllowanceNotify': '',
        'NotifyMail': '',
        'NotifyPhone': '',
        'AllowanceAmount': ''
    })
    # 需要做urlencode的參數
    urlencode_field = dict({
        'CustomerName': '',
        'NotifyMail': '',
        'ItemName': '',
        'ItemWord': ''
    })

    # 不需要送壓碼的欄位
    none_verification = dict({
        'ItemName': '',
        'ItemWord': '',
        'CheckMacValue': ''
    })

    '''
    *1寫入參數
    '''

    def insert_string(self, arParameters=dict):
        nItems_Count_Total = 0
        nItems_Foreach_Count = 1
        sItemName = ''
        sItemCount = ''
        sItemWord = ''
        sItemPrice = ''
        sItemTaxType = ''
        sItemAmount = ''

        # Python特性，需要複製一個字典，不然回修改到原先宣告的字典的key與value
        parameters = self.parameters.copy()

        for key, val in parameters.items():
            if key in arParameters:
                parameters[key] = arParameters[key]
        # 商品資訊組合
        nItems_Count_Total = len(arParameters['Items'])  # 商品總筆數
        if nItems_Count_Total != 0:
            for val2 in arParameters['Items']:
                sItemName += val2['ItemName'] if 'ItemName' in val2 else ''
                sItemCount += str(val2['ItemCount'])
                sItemWord += val2['ItemWord'] if 'ItemWord' in val2 else ''
                sItemPrice += str(val2['ItemPrice'])
                sItemTaxType += str(val2['ItemTaxType']) if 'ItemTaxType' in val2 else ''
                sItemAmount += str(val2['ItemAmount'])

                if nItems_Foreach_Count < nItems_Count_Total:
                    sItemName += '|'
                    sItemCount += '|'
                    sItemWord += '|'
                    sItemPrice += '|'
                    sItemTaxType += '|'
                    sItemAmount += '|'

                nItems_Foreach_Count += 1
        parameters['ItemName'] = sItemName  # 商品名稱
        parameters['ItemCount'] = sItemCount
        parameters['ItemWord'] = sItemWord  # 商品單位
        parameters['ItemPrice'] = sItemPrice
        parameters['ItemTaxType'] = sItemTaxType
        parameters['ItemAmount'] = sItemAmount
        return parameters

    '''
    * 2-2 驗證參數格式
    '''

    def check_extend_string(self, arParameters=dict):

        # 刪除items
        del arParameters['Items']

        return arParameters

    '''
    *4欄位例外處理方式(送壓碼前)
    '''

    def check_exception(self, arParameters=dict):
        return arParameters


'''
*  D發票作廢
'''


class ECPay_INVOICE_VOID():
    # 所需參數
    parameters = dict({
        'TimeStamp': '',
        'MerchantID': '',
        'CheckMacValue': '',
        'InvoiceNumber': '',
        'Reason': ''
    })
    # 需要做urlencode的參數
    urlencode_field = dict({
        'Reason': '',
    })

    # 不需要送壓碼的欄位
    none_verification = dict({
        'Reason': '',
        'CheckMacValue': ''
    })

    '''
    *1寫入參數
    '''

    def insert_string(self, arParameters=dict):

        # Python特性，需要複製一個字典，不然回修改到原先宣告的字典的key與value
        parameters = self.parameters.copy()

        for key, val in parameters.items():
            if key in arParameters:
                parameters[key] = arParameters[key]

        return parameters

    '''
    * 2-2 驗證參數格式
    '''

    def check_extend_string(self, arParameters=dict):

        return arParameters

    '''
    * 4欄位例外處理方式(送壓碼前)
    '''

    def check_exception(self, arParameters=dict):
        return arParameters


'''
*  E折讓作廢
'''


class ECPay_ALLOWANCE_VOID():
    # 所需參數
    parameters = dict({
        'TimeStamp': '',
        'MerchantID': '',
        'CheckMacValue': '',
        'InvoiceNo': '',
        'Reason': '',
        'AllowanceNo': ''
    })
    # 需要做urlencode的參數
    urlencode_field = dict({
        'Reason': '',
    })

    # 不需要送壓碼的欄位
    none_verification = dict({
        'Reason': '',
        'CheckMacValue': ''
    })

    '''
    *1寫入參數
    '''

    def insert_string(self, arParameters=dict):

        # Python特性，需要複製一個字典，不然回修改到原先宣告的字典的key與value
        parameters = self.parameters.copy()

        for key, val in parameters.items():
            if key in arParameters:
                parameters[key] = arParameters[key]

        return parameters

    '''
    * 2-2 驗證參數格式
    '''

    def check_extend_string(self, arParameters=dict):

        return arParameters

    '''
    * 4欄位例外處理方式(送壓碼前)
    '''

    def check_exception(self, arParameters=dict):
        return arParameters


'''
*  F查詢發票
'''


class ECPay_INVOICE_SEARCH():
    # 所需參數
    parameters = dict({
        'TimeStamp': '',
        'MerchantID': '',
        'RelateNumber': '',
        'CheckMacValue': '',
    })
    # 需要做urlencode的參數
    urlencode_field = dict({
        'IIS_Customer_Name': '',
        'IIS_Customer_Addr': '',
        'ItemName': '',
        'ItemWord': '',
        'ItemRemark': '',
        'InvoiceRemark': ''
    })

    # 不需要送壓碼的欄位
    none_verification = dict({
        'ItemName': '',
        'ItemWord': '',
        'ItemRemark': '',
        'InvoiceRemark': '',
        'PosBarCode': '',
        'QRCode_Left': '',
        'QRCode_Right': '',
        'CheckMacValue': ''
    })

    '''
    *1寫入參數
    '''

    def insert_string(self, arParameters=dict):

        # Python特性，需要複製一個字典，不然回修改到原先宣告的字典的key與value
        parameters = self.parameters.copy()

        for key, val in parameters.items():
            if key in arParameters:
                parameters[key] = arParameters[key]

        return parameters

    '''
    * 2-2 驗證參數格式
    '''

    def check_extend_string(self, arParameters=dict):
        return arParameters

    '''
    * 4欄位例外處理方式(送壓碼前)
    '''

    def check_exception(self, arParameters=dict):

        if 'IIS_Customer_Email' in arParameters:
            arParameters['IIS_Customer_Email'] = arParameters['IIS_Customer_Email'].replace('+', ' ')
        return arParameters


'''
*  G查詢作廢發票
'''


class ECPay_INVOICE_VOID_SEARCH():
    # 所需參數
    parameters = dict({
        'TimeStamp': '',
        'MerchantID': '',
        'RelateNumber': '',
        'CheckMacValue': ''
    })
    # 需要做urlencode的參數
    urlencode_field = dict({
        'Reason': '',
    })

    # 不需要送壓碼的欄位
    none_verification = dict({
        'Reason': '',
        'CheckMacValue': ''
    })

    '''
    *1寫入參數
    '''

    def insert_string(self, arParameters=dict):

        # Python特性，需要複製一個字典，不然回修改到原先宣告的字典的key與value
        parameters = self.parameters.copy()

        for key, val in parameters.items():
            if key in arParameters:
                parameters[key] = arParameters[key]

        return parameters

    '''
    * 2-2 驗證參數格式
    '''

    def check_extend_string(self, arParameters=dict):

        return arParameters

    '''
    * 4欄位例外處理方式(送壓碼前)
    '''

    def check_exception(self, arParameters=dict):
        return arParameters


'''
*  H查詢折讓明細
'''


class ECPay_ALLOWANCE_SEARCH():
    # 所需參數
    parameters = dict({
        'TimeStamp': '',
        'MerchantID': '',
        'CheckMacValue': '',
        'InvoiceNo': '',
        'AllowanceNo': ''
    })
    # 需要做urlencode的參數
    urlencode_field = dict({
        'ItemName': '',
        'ItemWord': '',
        'IIS_Customer_Name': ''
    })

    # 不需要送壓碼的欄位
    none_verification = dict({
        'ItemName': '',
        'ItemWord': '',
        'CheckMacValue': ''
    })

    '''
    *1寫入參數
    '''

    def insert_string(self, arParameters=dict):

        # Python特性，需要複製一個字典，不然回修改到原先宣告的字典的key與value
        parameters = self.parameters.copy()

        for key, val in parameters.items():
            if key in arParameters:
                parameters[key] = arParameters[key]

        return parameters

    '''
    * 2-2 驗證參數格式
    '''

    def check_extend_string(self, arParameters=dict):
        return arParameters

    '''
    * 4欄位例外處理方式(送壓碼前)
    '''

    def check_exception(self, arParameters=dict):
        return arParameters


'''
*  I查詢折讓作廢明細
'''


class ECPay_ALLOWANCE_VOID_SEARCH():
    # 所需參數
    parameters = dict({
        'TimeStamp': '',
        'MerchantID': '',
        'CheckMacValue': '',
        'InvoiceNo': '',
        'AllowanceNo': ''
    })
    # 需要做urlencode的參數
    urlencode_field = dict({
        'Reason': ''
    })

    # 不需要送壓碼的欄位
    none_verification = dict({
        'Reason': '',
        'CheckMacValue': ''
    })

    '''
    *1寫入參數
    '''

    def insert_string(self, arParameters=dict):

        # Python特性，需要複製一個字典，不然回修改到原先宣告的字典的key與value
        parameters = self.parameters.copy()

        for key, val in parameters.items():
            if key in arParameters:
                parameters[key] = arParameters[key]

        return parameters

    '''
    * 2-2 驗證參數格式
    '''

    def check_extend_string(self, arParameters=dict):
        return arParameters

    '''
    * 4欄位例外處理方式(送壓碼前)
    '''

    def check_exception(self, arParameters=dict):
        return arParameters


'''
*  J發送通知
'''


class ECPay_INVOICE_NOTIFY():
    # 所需參數
    parameters = dict({
        'TimeStamp': '',
        'MerchantID': '',
        'CheckMacValue': '',
        'InvoiceNo': '',
        'AllowanceNo': '',
        'NotifyMail': '',
        'Phone': '',
        'Notify': '',
        'InvoiceTag': '',
        'Notified': ''
    })
    # 需要做urlencode的參數
    urlencode_field = dict({
        'NotifyMail': ''
    })

    # 不需要送壓碼的欄位
    none_verification = dict({
        'CheckMacValue': ''
    })

    '''
    *1寫入參數
    '''

    def insert_string(self, arParameters=dict):

        # Python特性，需要複製一個字典，不然回修改到原先宣告的字典的key與value
        parameters = self.parameters.copy()

        for key, val in parameters.items():
            if key in arParameters:
                parameters[key] = arParameters[key]

        return parameters

    '''
    * 2-2 驗證參數格式
    '''

    def check_extend_string(self, arParameters=dict):
        return arParameters

    '''
    * 4欄位例外處理方式(送壓碼前)
    '''

    def check_exception(self, arParameters=dict):
        return arParameters


'''
*  K付款完成觸發或延遲開立發票
'''


class ECPay_INVOICE_TRIGGER():
    # 所需參數
    parameters = dict({
        'TimeStamp': '',
        'MerchantID': '',
        'CheckMacValue': '',
        'Tsr': '',
        'PayType': '2'
    })
    # 需要做urlencode的參數
    urlencode_field = dict({

    })

    # 不需要送壓碼的欄位
    none_verification = dict({
        'CheckMacValue': ''
    })

    '''
    *1寫入參數
    '''

    def insert_string(self, arParameters=dict):

        # Python特性，需要複製一個字典，不然回修改到原先宣告的字典的key與value
        parameters = self.parameters.copy()

        for key, val in parameters.items():
            if key in arParameters:
                parameters[key] = arParameters[key]

        return parameters

    '''
    * 2-2 驗證參數格式
    '''

    def check_extend_string(self, arParameters=dict):
        return arParameters

    '''
    * 4欄位例外處理方式(送壓碼前)
    '''

    def check_exception(self, arParameters=dict):
        return arParameters


'''
*  L手機條碼驗證
'''


class ECPay_CHECK_MOBILE_BARCODE():
    # 所需參數
    parameters = dict({
        'TimeStamp': '',
        'MerchantID': '',
        'CheckMacValue': '',
        'BarCode': ''
    })
    # 需要做urlencode的參數
    urlencode_field = dict({

    })

    # 不需要送壓碼的欄位
    none_verification = dict({
        'CheckMacValue': ''
    })

    '''
    *1寫入參數
    '''

    def insert_string(self, arParameters=dict):

        # Python特性，需要複製一個字典，不然回修改到原先宣告的字典的key與value
        parameters = self.parameters.copy()

        for key, val in parameters.items():
            if key in arParameters:
                parameters[key] = arParameters[key]

        return parameters

    '''
    * 2-2 驗證參數格式
    '''

    def check_extend_string(self, arParameters=dict):
        return arParameters

    '''
    * 4欄位例外處理方式(送壓碼前)
    '''

    def check_exception(self, arParameters=dict):
        if 'BarCode' in arParameters:
            arParameters['BarCode'] = arParameters['BarCode'].replace('+', ' ')
        return arParameters


'''
*  M愛心碼驗證
'''


class ECPay_CHECK_LOVE_CODE():
    # 所需參數
    parameters = dict({
        'TimeStamp': '',
        'MerchantID': '',
        'LoveCode': '',
        'CheckMacValue': ''
    })
    # 需要做urlencode的參數
    urlencode_field = dict({

    })

    # 不需要送壓碼的欄位
    none_verification = dict({
        'CheckMacValue': ''
    })

    '''
    *1寫入參數
    '''

    def insert_string(self, arParameters=dict):

        # Python特性，需要複製一個字典，不然回修改到原先宣告的字典的key與value
        parameters = self.parameters.copy()

        for key, val in parameters.items():
            if key in arParameters:
                parameters[key] = arParameters[key]

        return parameters

    '''
    * 2-2 驗證參數格式
    '''

    def check_extend_string(self, arParameters=dict):
        return arParameters

    '''
    * 4欄位例外處理方式(送壓碼前)
    '''

    def check_exception(self, arParameters=dict):
        return arParameters



