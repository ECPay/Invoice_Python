#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time
import sys
import re
from ecpay_setting import *


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
        return ECPay_Invoice_Send.CheckOut(arParameters, self.HashKey, self.HashIV, self.Invoice_Method, self.Invoice_Url)

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
    def CheckOut(arParameters = dict, HashKey = '', HashIV = '', Invoice_Method = '', ServiceURL = ''):
        # 發送資訊處理

        arParameters = ECPay_Invoice_Send.process_send(arParameters, HashKey, HashIV, Invoice_Method, ServiceURL)

        szResult = ECPay_IO.ServerPost(arParameters, ServiceURL)
        # 回傳資訊處理
        arParameters_Return = ECPay_Invoice_Send.process_return(szResult, HashKey, HashIV, Invoice_Method)
        return arParameters_Return

    # 資料檢查與過濾(送出)
    @staticmethod
    def process_send(arParameters = dict, HashKey = '', HashIV = '', Invoice_Method = '', ServiceURL = ''):
        # 宣告物件
        InvoiceMethod = 'ECPay_' + Invoice_Method
        class_str = globals()[InvoiceMethod]
        InvoiceObj = class_str()
        # 1寫入參數
        arParameters = InvoiceObj.insert_string(arParameters)
        # 2檢查共用參數
        ECPay_Invoice_Send.check_string(arParameters['MerchantID'], HashKey, HashIV, Invoice_Method, ServiceURL)
        # 3檢查各別參數
        arParameters = InvoiceObj.check_extend_string(arParameters)
        # 4處理需要轉換為urlencode的參數
        arParameters = ECPay_Invoice_Send.urlencode_process(arParameters, InvoiceObj.urlencode_field)
        # 5欄位例外處理方式(送壓碼前)
        arException = InvoiceObj.check_exception(arParameters)
        # 6產生壓碼
        arParameters['CheckMacValue'] = ECPay_Invoice_Send.generate_checkmacvalue(arException, InvoiceObj.none_verification, HashKey, HashIV)
        return arParameters


    '''
    資料檢查與過濾(回傳)
    '''
    @staticmethod
    def process_return(sParameters = '', HashKey = '', HashIV = '', Invoice_Method = ''):
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
            CheckMacValue = ECPay_Invoice_Send.generate_checkmacvalue(arException, InvoiceObj_Return.none_verification, HashKey, HashIV)
            if CheckMacValue != arParameters['CheckMacValue']:
                print '自己壓的：' + CheckMacValue
                print '系統回傳的：' + arParameters['CheckMacValue']
                print '注意：壓碼錯誤'
        # 10處理需要urldecode的參數
        arParameters = ECPay_Invoice_Send.urldecode_process(arParameters, InvoiceObj_Return.urlencode_field)
        return arParameters


    '''
    2檢查共同參數
    '''
    @staticmethod
    def check_string(MerchantID = '', HashKey = '', HashIV = '', Invoice_Method = 'INVOICE', ServiceURL = ''):
        arErrors = list()
        # 檢查是否傳入動作方式
        if Invoice_Method == '' or Invoice_Method == 'Invoice_Method':
            arErrors.append('Invoice_Method is required.')
        # 檢查是否有傳入MerchantID
        if len(MerchantID) == 0:
            arErrors.append('MerchantID is required.')
        if len(MerchantID) > 10:
            arErrors.append('MerchantID max langth as 10.')
        # 檢查是否有傳入HashKey
        if len(HashKey) == 0:
            arErrors.append('HashKey is required.')
        # 檢查是否有傳入HashIV
        if len(HashIV) == 0:
            arErrors.append('HashIV is required.')
        # 檢查是否有傳送網址
        if len(ServiceURL) == 0:
            arErrors.append('Invoice_Url is required.')

        if len(arErrors) > 0:
            print(' '.join(arErrors))
    '''
    *4處理需要轉換為urlencode的參數
    '''
    @staticmethod
    def urlencode_process(arParameters=dict, urlencode_field=dict):
        for key, val in arParameters.items():
            if key in urlencode_field:
                arParameters[key] = urllib.quote(val)
                arParameters[key] = ECPay_CheckMacValue.do_str_replace(arParameters[key])
        return arParameters

    '''
    *6, 9產生壓碼
    '''

    @staticmethod
    def generate_checkmacvalue(arParameters=dict, none_verification=dict, HashKey='', HashIV =''):

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
    def string_to_array(Parameters = ''):
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
    def urldecode_process(arParameters = dict, urlencode_field = dict):
        for key, val in arParameters.items():
            if key in urlencode_field:
                arParameters[key] = ECPay_CheckMacValue.restore_str_replace(arParameters[key])
                arParameters[key] = urllib.unquote_plus(val)

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
    def insert_string(self, arParameters = dict):
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
        parameters['ItemName'] = sItemName		# 商品名稱
        parameters['ItemCount'] = sItemCount
        parameters['ItemWord'] = sItemWord		# 商品單位
        parameters['ItemPrice'] = sItemPrice
        parameters['ItemTaxType'] = sItemTaxType
        parameters['ItemAmount'] = sItemAmount
        parameters['ItemRemark'] = sItemRemark 	# 商品備註
        return parameters
    
    '''
    *2 - 2驗證參數格式
    '''
    def check_extend_string(self, arParameters = dict):

        arErrors = list()

        # 4.廠商自訂編號

        # * 預設不可為空值
        if len(arParameters['RelateNumber']) == 0:
            arErrors.append('4:RelateNumber is required.')
        # *預設最大長度為30碼
        if len(arParameters['RelateNumber']) > 30:
            arErrors.append('4:RelateNumber max langth as 30.')

        # 5.客戶編號CustomerID

        # *預設最大長度為20碼
        if len(arParameters['CustomerID']) > 20:
            arErrors.append('5:CustomerID max langth as 20.')
        # *比對客戶編號 只接受英、數字與下底線格式
        if len(arParameters['CustomerID']) > 0:
            if re.match("^[a-zA-Z0-9_]+$", arParameters['CustomerID']) == None:
                arErrors.append('5:Invalid CustomerID.')

        # 6.統一編號判斷CustomerIdentifier
        # * 若統一編號有值時，則固定長度為數字8碼
        # * 判斷統一編號是否都為數字
        if len(arParameters['CustomerIdentifier']) > 0:
            if len(arParameters['CustomerIdentifier']) != 8:
                arErrors.append('6:CustomerIdentifier length should be 8.')

            if re.match("^[0-9]*$", arParameters['CustomerIdentifier']) == None:
                arErrors.append('6:Invalid CustomerIdentifier.')

        # 6.1 * 若列印註記 = '1'(列印)時，則統一編號須有值
        if arParameters['Print'] == EcpayPrintMark.Yes:
            if len(arParameters['CustomerIdentifier']) == 0:
                arErrors.append('6:CustomerIdentifier is required.')

        # 7.客戶名稱CustomerName
        # x僅能為中英數字格式
        # * 若列印註記 = '1'(列印)時，則客戶名稱須有值
        if arParameters['Print'] == EcpayPrintMark.Yes:
            if len(arParameters['CustomerName']) == 0 and arParameters['OnLine']:
                arErrors.append('7:CustomerName is required.')
        # *預設最大長度為60碼
        if len(arParameters['CustomerName'].decode('utf-8')) > 60:
            arErrors.append('7:CustomerName max length as 60.')

        # 8.客戶地址 CustomerAddr(UrlEncode, 預設為空字串)
        #  *若列印註記 = '1'(列印)時，則客戶地址須有值
        if arParameters['Print'] == EcpayPrintMark.Yes:
            if len(arParameters['CustomerAddr']) == 0 and arParameters['OnLine']:
                arErrors.append("8:CustomerAddr is required.")
        # *預設最大長度為100碼
        if len(arParameters['CustomerAddr'].decode('utf-8')) > 100:
            arErrors.append("8:CustomerAddr max length as 100.")

        # 9.客戶手機號碼CustomerPhone
        # *預設最小長度為1碼，最大長度為20碼
        if len(arParameters['CustomerPhone']) > 20:
            arErrors.append("9:CustomerPhone max length as 20.")
        # *預設格式為數字組成
        if len(arParameters['CustomerPhone']) > 0:
            if re.match('^[0-9]*$', arParameters['CustomerPhone']) == None:
                arErrors.append('9:Invalid CustomerPhone.')

        # 10.客戶電子信箱CustomerEmail(UrlEncode, 預設為空字串, 與CustomerPhone擇一不可為空)
        # *預設最大長度為80碼
        if len(arParameters['CustomerEmail']) > 80:
                arErrors.append("10:CustomerEmail max length as 80.")
        # *若客戶電子信箱有值時，則格式僅能為Email的標準格式
        if len(arParameters['CustomerEmail']) > 0:
            if re.match('^[a-z0-9&\'\.\-_\+]+@[a-z0-9\-_]+\.([a-z0-9\-_]+\.)*?[a-z]+$', arParameters['CustomerEmail']) == None:
                arErrors.append('10:Invalid CustomerEmail Format.')

        # 9.10.
        #  *若客戶手機號碼為空值時，則客戶電子信箱不可為空值
        if len(arParameters['CustomerPhone']) == 0 and len(arParameters['CustomerEmail']) == 0 and arParameters['OnLine']:
            arErrors.append("9-10:CustomerPhone or CustomerEmail is required.")

        # 11.通關方式ClearanceMark(預設為空字串)
        # *最多1字元
        if len(arParameters['ClearanceMark']) > 1:
            arErrors.append("11:ClearanceMark max length as 1.")

        # *請設定空字串，僅課稅類別為零稅率(Zero)時，此參數不可為空字串
        if str(arParameters['TaxType']) == EcpayTaxType.Zero:
            if arParameters['ClearanceMark'] != EcpayClearanceMark.Yes and arParameters['ClearanceMark'] != EcpayClearanceMark.No:
                arErrors.append("11:ClearanceMark is required.")
        else:
            if len(arParameters['ClearanceMark']) > 0:
                arErrors.append("11:Please remove ClearanceMark.")
        # 12.列印註記Print(預設為No)
        #  *列印註記僅能為0或1
        if arParameters['Print'] != EcpayPrintMark.Yes and arParameters['Print'] != EcpayPrintMark.No:
                arErrors.append("12:Invalid Print.")
        # *若捐贈註記 = '1'(捐贈)時，則VAL = '0'(不列印)
        if arParameters['Donation'] == EcpayDonation.Yes:
            if arParameters['Print'] != EcpayPrintMark.No:
                arErrors.append( "12:Donation Print should be No.")
        # *若統一編號有值時，則VAL = '1'(列印)
        if len(arParameters['CustomerIdentifier']) > 0:
            if arParameters['Print'] != EcpayPrintMark.Yes:
                arErrors.append("12:CustomerIdentifier Print should be Yes.")
        # 線下列印判斷
        #  1200079當線下廠商開立發票無載具且無統一編號時，必須列印。
        if arParameters['OnLine'] == False:
            if arParameters['CarruerType'] == EcpayCarruerType.No and len(arParameters['CustomerIdentifier']) == 0:
                if arParameters['Print'] != EcpayPrintMark.Yes:
                    arErrors.append("12:Offline Print should be Yes.")

        # 13.捐贈註記Donation
        #  *固定給定下述預設值若為捐贈時，則VAL = '1'，若為不捐贈時，則VAL = '2'
        if arParameters['Donation'] != EcpayDonation.Yes and arParameters['Donation'] != EcpayDonation.No:
            arErrors.append( "13:Invalid Donation.")
        # *若統一編號有值時，則VAL = '2'(不捐贈)
        if len(arParameters['CustomerIdentifier']) > 0 and arParameters['Donation'] == EcpayDonation.Yes:
            arErrors.append( "13:CustomerIdentifier Donation should be No.")

        # 14.愛心碼LoveCode(預設為空字串)
        #  *若捐贈註記 = '1'(捐贈)時，則須有值
        if arParameters['Donation'] == EcpayDonation.Yes:
            if re.match("^([xX]{1}[0-9]{2,6}|[0-9]{3,7})$", arParameters['LoveCode']) == None:
                arErrors.append("14:Invalid LoveCode.")
        else:
            if len(arParameters['LoveCode']) > 0:
                arErrors.append("14:Please remove LoveCode.")

        # 15.載具類別CarruerType(預設為None)
        # *固定給定下述預設值None、Member、Cellphone
        if arParameters['CarruerType'] != EcpayCarruerType.No and arParameters['CarruerType'] != EcpayCarruerType.Member and arParameters['CarruerType'] != EcpayCarruerType.Citizen and arParameters['CarruerType'] != EcpayCarruerType.Cellphone:
            arErrors.append("15:Invalid CarruerType.")
        else:
            # * 統一編號不為空字串時，則載具類別不可為會載具或自然人憑證載具
            if len(arParameters['CustomerIdentifier']) > 0:
                if arParameters['CarruerType'] == EcpayCarruerType.Member or arParameters['CarruerType'] == EcpayCarruerType.Citizen:
                    arErrors.append("15:Invalid CarruerType.")

        # 16.載具編號CarruerNum(預設為空字串)
        # * 載具類別為無載具(None)或會員載具(Member)時，請設定空字串
        if arParameters['CarruerType'] == EcpayCarruerType.No or arParameters['CarruerType'] == EcpayCarruerType.Member:
            if len(arParameters['CarruerNum']) > 0:
                arErrors.append("16:Please remove CarruerNum.")
        # *載具類別為買受人自然人憑證(Citizen)時，請設定自然人憑證號碼，前2碼為大小寫英文，後14碼為數字
        elif arParameters['CarruerType'] == EcpayCarruerType.Citizen:
            if re.match('^[a-zA-Z]{2}\d{14}$', arParameters['CarruerNum']) == None:
                arErrors.append("16:Invalid CarruerNum.")
        # *載具類別為買受人手機條碼(Cellphone)時，請設定手機條碼，第1碼為「 / 」，後7碼為大小寫英文、數字、「+」、「-」或「.」
        elif arParameters['CarruerType'] == EcpayCarruerType.Cellphone:
            if re.match('^\/{1}[0-9a-zA-Z+-.]{7}$', arParameters['CarruerNum']) == None:
                arErrors.append("16:Invalid CarruerNum.")
        else:
            arErrors.append("16:Please remove CarruerNum.")

        # 17.課稅類別TaxType(不可為空)
        # * 不可為空
        if len(str(arParameters['TaxType'])) == 0:
            arErrors.append("17:TaxType is required.")
        # *僅能為 1應稅 2零稅率 3免稅 9.應稅與免稅混合
        if str(arParameters['TaxType']) != EcpayTaxType.Dutiable and str(arParameters['TaxType']) != EcpayTaxType.Zero and str(arParameters['TaxType']) != EcpayTaxType.Free and str(arParameters['TaxType']) != EcpayTaxType.Mix:
            arErrors.append("17:Invalid TaxType.")
        # 18.發票金額SalesAmount
        # * 不可為空
        if len(str(arParameters['SalesAmount'])) == 0:
            arErrors.append("18:SalesAmount is required.")

        # 20.21.22.23.24.25.商品資訊
        # *不可為空
        if sys.getsizeof(arParameters['Items']) == 0:
            arErrors.append('20-25:Items is required.')

        # 檢查是否存在保留字元'|'
        else:
            bFind_Tag = True
            bError_Tag = False
            for val in arParameters['Items']:
                bFind_Tag = val['ItemName'].find('|')
                if bFind_Tag != -1 or not val['ItemName']:
                    bError_Tag = True
                    arErrors.append('20:Invalid ItemName.')
                    break
                bFind_Tag = str(val['ItemCount']).find('|')
                if bFind_Tag != -1 or not val['ItemCount']:
                    bError_Tag = True
                    arErrors.append('21:Invalid ItemCount.')
                    break
                bFind_Tag = val['ItemWord'].find('|')
                if bFind_Tag != -1 or not val['ItemWord']:
                    bError_Tag = True
                    arErrors.append('22:Invalid ItemWord.')
                    break
                bFind_Tag = str(val['ItemPrice']).find('|')
                if bFind_Tag != -1 or val['ItemPrice'] < 0:
                    bError_Tag = True
                    arErrors.append('23:Invalid ItemPrice.')
                    break

                bFind_Tag = str(val['ItemTaxType']).find('|')
                if bFind_Tag != -1 or not val['ItemTaxType']:
                    if arParameters['TaxType'] == EcpayTaxType.Mix:
                        bError_Tag = True
                        arErrors.append('24:Invalid ItemTaxType.')
                        break
                bFind_Tag = str(val['ItemAmount']).find('|')
                if bFind_Tag != -1 or val['ItemAmount'] < 0:
                    bError_Tag = True
                    arErrors.append('25:Invalid ItemAmount.')
                    break
                # V1.0.3
                if val['ItemRemark']:
                    bFind_Tag = val['ItemRemark'].find('|')
                    if bFind_Tag != -1 or not val['ItemRemark']:
                        bError_Tag = True
                        arErrors.append('143:Invalid ItemRemark.')
                        break
            # 檢查商品格式
            if not bError_Tag:
                for val in arParameters['Items']:
                    # * ItemCount數字判斷
                    if re.match('^[0-9]*$', str(val['ItemCount'])) == None:
                        arErrors.append('21:Invalid ItemCount.')
                    # *ItemWord預設最大長度為6碼
                    if len(val['ItemWord']) > 6:
                        arErrors.append('22:ItemWord max length as 6.')
                    # *ItemPrice數字判斷
                    # 不是小數
                    if re.match('^[-+]?[0-9]*\.[0-9]+$', str(val['ItemPrice'])) == None:
                        # 又不是整數，跳出錯誤訊息
                        if re.match('^[0-9]*$',str(val['ItemPrice'])) == None:
                            arErrors.append('23:Invalid ItemPrice.A')
                    # *ItemAmount數字判斷
                    if re.match('^[-0-9]*$', str(val['ItemAmount']))== None:
                        arErrors.append('25:Invalid ItemAmount.B')
                    # V1.0.3
                    #  * ItemRemark預設最大長度為40碼如果有此欄位才判斷
                    if 'ItemRemark' in val:
                        if len(val['ItemRemark']) > 40:
                            arErrors.append('143:ItemRemark max length as 40.')

        # 27.字軌類別
        # *InvType(不可為空)僅能為07或08狀態
        if arParameters['InvType'] != EcpayInvType.General and arParameters['InvType'] != EcpayInvType.Special:
            arErrors.append("27:Invalid InvType.")
        # 29.商品單價是否含稅(預設為含稅價)
        #  *固定給定下述預設值若為含稅價，則VAL = '1'
        if 'vat' in arParameters:
            if arParameters['vat']:
                if arParameters['vat'] != EcpayVatType.Yes and arParameters['vat'] != EcpayVatType.No:
                    arErrors.append("29:Invalid VatType.")

        if len(arErrors) > 0:
            print(' '.join(arErrors))

        # 刪除items
        del arParameters['Items']
        # 刪除SDK自訂義參數
        del arParameters['OnLine']

        return arParameters


    '''
    *4欄位例外處理方式(送壓碼前)
    '''
    def check_exception(self, arParameters = dict):
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
    def check_extend_string(self, arParameters = dict):

        arErrors = list()

        # 4.廠商自訂編號

        # * 預設不可為空值
        if len(arParameters['RelateNumber']) == 0:
            arErrors.append('4:RelateNumber is required.')
        # *預設最大長度為30碼
        if len(arParameters['RelateNumber']) > 30:
            arErrors.append('4:RelateNumber max langth as 30.')

        # 5.客戶編號CustomerID

        # * 載具類別為1 則客戶編號需有值
        if arParameters['CarruerType'] == '1' and len(arParameters['CustomerID']) == 0:
            arErrors.append('5:CustomerID is required.')
        # *預設最大長度為20碼
        if len(arParameters['CustomerID']) > 20:
            arErrors.append('5:CustomerID max langth as 20.')
        # *比對客戶編號 只接受英、數字與下底線格式
        if len(arParameters['CustomerID']) > 0:
            if re.match("^[a-zA-Z0-9_]+$", arParameters['CustomerID']) == None:
                arErrors.append('5:Invalid CustomerID.')

        # 6.統一編號判斷CustomerIdentifier
        # * 若統一編號有值時，則固定長度為數字8碼
        if len(arParameters['CustomerIdentifier']) > 0:
            if len(arParameters['CustomerIdentifier']) != 8:
                arErrors.append('6:CustomerIdentifier length should be 8.')

            if re.match("^[0-9]*$", arParameters['CustomerIdentifier']) == None:
                arErrors.append('6:Invalid CustomerIdentifier.')

        # 6.1 * 若列印註記 = '1'(列印)時，則統一編號須有值
        if arParameters['Print'] == EcpayPrintMark.Yes:
            if len(arParameters['CustomerIdentifier']) == 0:
                arErrors.append('6:CustomerIdentifier is required.')

        # 7.客戶名稱CustomerName
        # x僅能為中英數字格式
        # * 若列印註記 = '1'(列印)時，則客戶名稱須有值
        if arParameters['Print'] == EcpayPrintMark.Yes:
            if len(arParameters['CustomerName']) == 0:
                arErrors.append('7:CustomerName is required.')
        # *預設最大長度為60碼
        if len(arParameters['CustomerName'].decode('utf-8')) > 60:
            arErrors.append('7:CustomerName max length as 60.')

        # 8.客戶地址 CustomerAddr(UrlEncode, 預設為空字串)
        #  *若列印註記 = '1'(列印)時，則客戶地址須有值
        if arParameters['Print'] == EcpayPrintMark.Yes:
            if len(arParameters['CustomerAddr']) == 0:
                arErrors.append("8:CustomerAddr is required.")
        # *預設最大長度為100碼
        if len(arParameters['CustomerAddr'].decode('utf-8')) > 100:
            arErrors.append("8:CustomerAddr max length as 100.")

        # 9.客戶手機號碼CustomerPhone
        # *預設最小長度為1碼，最大長度為20碼
        if len(arParameters['CustomerPhone']) > 20:
            arErrors.append("9:CustomerPhone max length as 20.")
        # *預設格式為數字組成
        if len(arParameters['CustomerPhone']) > 0:
            if re.match('^[0-9]*$', arParameters['CustomerPhone']) == None:
                arErrors.append('9:Invalid CustomerPhone.')

        # 10.客戶電子信箱CustomerEmail(UrlEncode, 預設為空字串, 與CustomerPhone擇一不可為空)
        # *預設最大長度為80碼
        if len(arParameters['CustomerEmail']) > 80:
                arErrors.append("10:CustomerEmail max length as 80.")
        # *若客戶電子信箱有值時，則格式僅能為Email的標準格式
        if len(arParameters['CustomerEmail']) > 0:
            if re.match('^[a-z0-9&\'\.\-_\+]+@[a-z0-9\-_]+\.([a-z0-9\-_]+\.)*?[a-z]+$', arParameters['CustomerEmail']) == None:
                arErrors.append('10:Invalid CustomerEmail Format.')

        # 9.10.
        #  *若客戶手機號碼為空值時，則客戶電子信箱不可為空值
        if len(arParameters['CustomerPhone']) == 0 and len(arParameters['CustomerEmail']) == 0:
            arErrors.append("9-10:CustomerPhone or CustomerEmail is required.")

        # 11.通關方式ClearanceMark(預設為空字串)
        # *最多1字元
        if len(arParameters['ClearanceMark']) > 1:
            arErrors.append("11:ClearanceMark max length as 1.")

        # *請設定空字串，僅課稅類別為零稅率(Zero)時，此參數不可為空字串
        if str(arParameters['TaxType']) == EcpayTaxType.Zero:
            if arParameters['ClearanceMark'] != EcpayClearanceMark.Yes and arParameters['ClearanceMark'] != EcpayClearanceMark.No:
                arErrors.append("11:ClearanceMark is required.")
        else:
            if len(arParameters['ClearanceMark']) > 0:
                arErrors.append("11:Please remove ClearanceMark.")
        # 12.列印註記Print(預設為No)
        #  *列印註記僅能為0或1
        if arParameters['Print'] != EcpayPrintMark.Yes and arParameters['Print'] != EcpayPrintMark.No:
                arErrors.append( "12:Invalid Print.")
        # *若捐贈註記 = '1'(捐贈)時，則VAL = '0'(不列印)
        if arParameters['Donation'] == EcpayDonation.Yes:
            if arParameters['Print'] != EcpayPrintMark.No:
                arErrors.append( "12:Donation Print should be No.")
        # *若統一編號有值時，則VAL = '1'(列印)
        if len(arParameters['CustomerIdentifier']) > 0:
            if arParameters['Print'] != EcpayPrintMark.Yes:
                arErrors.append( "12:CustomerIdentifier Print should be Yes.")
        # 13.捐贈註記Donation
        #  *固定給定下述預設值若為捐贈時，則VAL = '1'，若為不捐贈時，則VAL = '2'
        if arParameters['Donation'] != EcpayDonation.Yes and arParameters['Donation'] != EcpayDonation.No:
            arErrors.append( "13:Invalid Donation.")
        # *若統一編號有值時，則VAL = '2'(不捐贈)
        if len(arParameters['CustomerIdentifier']) > 0 and arParameters['Donation'] == EcpayDonation.Yes:
            arErrors.append( "13:CustomerIdentifier Donation should be No.")

        # 14.愛心碼LoveCode(預設為空字串)
        #  *若捐贈註記 = '1'(捐贈)時，則須有值
        if arParameters['Donation'] == EcpayDonation.Yes:
            if re.match("^([xX]{1}[0-9]{2,6}|[0-9]{3,7})$", arParameters['LoveCode']) == None:
                arErrors.append("14:Invalid LoveCode.")
        else:
            if len(arParameters['LoveCode']) > 0:
                arErrors.append( "14:Please remove LoveCode.")

        # 15.載具類別CarruerType(預設為None)
        # *固定給定下述預設值None、Member、Cellphone
        if arParameters['CarruerType'] != EcpayCarruerType.No and arParameters['CarruerType'] != EcpayCarruerType.Member and arParameters['CarruerType'] != EcpayCarruerType.Citizen and arParameters['CarruerType'] != EcpayCarruerType.Cellphone:
            arErrors.append("15:Invalid CarruerType.")
        else:
            # * 統一編號不為空字串時，則載具類別不可為會載具或自然人憑證載具
            if len(arParameters['CustomerIdentifier']) > 0:
                if arParameters['CarruerType'] == EcpayCarruerType.Member or arParameters['CarruerType'] == EcpayCarruerType.Citizen:
                    arErrors.append("15:Invalid CarruerType.")

        # 16.載具編號CarruerNum(預設為空字串)
        # * 載具類別為無載具(None)或會員載具(Member)時，請設定空字串
        if arParameters['CarruerType'] == EcpayCarruerType.No or arParameters['CarruerType'] == EcpayCarruerType.Member:
            if len(arParameters['CarruerNum']) > 0:
                arErrors.append("16:Please remove CarruerNum.")
        # *載具類別為買受人自然人憑證(Citizen)時，請設定自然人憑證號碼，前2碼為大小寫英文，後14碼為數字
        elif arParameters['CarruerType'] == EcpayCarruerType.Citizen:
            if re.match('^[a-zA-Z]{2}\d{14}$', arParameters['CarruerNum']) == None:
                arErrors.append("16:Invalid CarruerNum.")
        # *載具類別為買受人手機條碼(Cellphone)時，請設定手機條碼，第1碼為「 / 」，後7碼為大小寫英文、數字、「+」、「-」或「.」
        elif arParameters['CarruerType'] == EcpayCarruerType.Cellphone:
            if re.match('^\/{1}[0-9a-zA-Z+-.]{7}$', arParameters['CarruerNum']) == None:
                arErrors.append("16:Invalid CarruerNum.")
        else:
            arErrors.append("16:Please remove CarruerNum.")

        # 17.課稅類別TaxType(不可為空)
        # * 不可為空
        if len(str(arParameters['TaxType'])) == 0:
            arErrors.append("17:TaxType is required.")
        # *僅能為 1應稅 2零稅率 3免稅 9.應稅與免稅混合
        if str(arParameters['TaxType']) != EcpayTaxType.Dutiable and str(arParameters['TaxType']) != EcpayTaxType.Zero and str(arParameters['TaxType']) != EcpayTaxType.Free and str(arParameters['TaxType']) != EcpayTaxType.Mix:
            arErrors.append("17:Invalid TaxType.")
        # 18.發票金額SalesAmount
        # * 不可為空
        if len(str(arParameters['SalesAmount'])) == 0:
            arErrors.append("18:SalesAmount is required.")

        # 20.21.22.23.24.25.商品資訊
        # *不可為空
        if sys.getsizeof(arParameters['Items']) == 0:
            arErrors.append('20-25:Items is required.')

        # 檢查是否存在保留字元'|'
        else:
            bFind_Tag = True
            bError_Tag = False
            for val in arParameters['Items']:
                bFind_Tag = val['ItemName'].find('|')
                if bFind_Tag != -1 or not val['ItemName']:
                    bError_Tag = True
                    arErrors.append('20:Invalid ItemName.')
                    break
                bFind_Tag = str(val['ItemCount']).find('|')
                if bFind_Tag != -1 or not val['ItemCount']:
                    bError_Tag = True
                    arErrors.append('21:Invalid ItemCount.')
                    break
                bFind_Tag = val['ItemWord'].find('|')
                if bFind_Tag != -1 or not val['ItemWord']:
                    bError_Tag = True
                    arErrors.append('22:Invalid ItemWord.')
                    break
                bFind_Tag = str(val['ItemPrice']).find('|')
                if bFind_Tag != -1 or val['ItemPrice'] < 0:
                    bError_Tag = True
                    arErrors.append('23:Invalid ItemPrice.')
                    break
                bFind_Tag = str(val['ItemTaxType']).find('|')
                if bFind_Tag != -1 or not val['ItemTaxType']:
                    if arParameters['TaxType'] == EcpayTaxType.Mix:
                        bError_Tag = True
                        arErrors.append('24:Invalid ItemTaxType.')
                        break
                bFind_Tag = str(val['ItemAmount']).find('|')
                if bFind_Tag != -1 or val['ItemAmount'] < 0:
                    bError_Tag = True
                    arErrors.append('25:Invalid ItemAmount.')
                    break
                # V1.0.3
                if val['ItemRemark']:
                    bFind_Tag = val['ItemRemark'].find('|')
                    if bFind_Tag != -1 or not val['ItemRemark']:
                        bError_Tag = True
                        arErrors.append('143:Invalid ItemRemark.')
                        break
            # 檢查商品格式
            if not bError_Tag:
                for val in arParameters['Items']:
                    # * ItemCount數字判斷
                    if re.match('^[0-9]*$', str(val['ItemCount'])) == None:
                        arErrors.append('21:Invalid ItemCount.')
                    # *ItemWord預設最大長度為6碼
                    if len(val['ItemWord']) > 6:
                        arErrors.append('22:ItemWord max length as 6.')
                    # *ItemPrice數字判斷
                    if re.match('^[-+]?[0-9]*\.[0-9]+$', str(val['ItemPrice'])) == None:
                        # 又不是整數，跳出錯誤訊息
                        if re.match('^[0-9]*$',str(val['ItemPrice'])) == None:
                            arErrors.append('23:Invalid ItemPrice.A')
                    # *ItemAmount數字判斷
                    if re.match('^[-0-9]*$', str(val['ItemAmount']))== None:
                        arErrors.append('25:Invalid ItemAmount.B')
                    # V1.0.3
                    #  * ItemRemark預設最大長度為40碼如果有此欄位才判斷
                    if 'ItemRemark' in val:
                        if len(val['ItemRemark']) > 40:
                            arErrors.append('143:ItemRemark max length as 40.')

        # 27.字軌類別
        # *InvType(不可為空)僅能為07或08狀態
        if arParameters['InvType'] != EcpayInvType.General and arParameters['InvType'] != EcpayInvType.Special:
            arErrors.append("27:Invalid InvType.")
        # 30.延遲註記DelayFlag
        if arParameters['DelayFlag'] != EcpayDelayFlagType.Delay  and arParameters['DelayFlag'] != EcpayDelayFlagType.Trigger:
            arErrors.append("30:Invalid DelayFlagType.")

        # 31.延遲天數DelayDay
        # 延遲天數，範圍0~15，設定為0時，付款完成後立即開立發票

        # *DelayDay(不可為空, 預設為0)
            arParameters['DelayDay'] = int(arParameters['DelayDay'])

        # *若為延遲開立時，延遲天數須介於1至15天內
        if arParameters['DelayFlag'] == EcpayDelayFlagType.Delay:
            
            if int(arParameters['DelayDay']) < 1 or int(arParameters['DelayDay']) > 15:

                arErrors.append("31:DelayDay should be 1 ~ 15.")
        # *若為觸發開立時，延遲天數須介於0至15天內
        if arParameters['DelayFlag'] == EcpayDelayFlagType.Trigger:
            if arParameters['DelayDay'] < 0 or arParameters['DelayDay'] > 15:
                arErrors.append("31:DelayDay should be 0 ~ 15.")

        # 33.交易單號Tsr
        # *必填項目
        if len(arParameters['Tsr']) == 0:
            arErrors.append('33:Tsr is required.')

        # *判斷最大字元是否超過30字
        if len(arParameters['Tsr']) > 30:
            arErrors.append('33:Tsr max length as 30.')

        # 34.交易類別PayType
        # *2016-10-04 修改為僅允許2
        if arParameters['PayType'] != EcpayPayTypeCategory.Ecpay:
            arErrors.append("34:Invalid PayType.")
        else:
            # * 必填項目交易類別名稱預設不能為空值僅允許ECPAY
            arParameters['PayAct'] = 'ECPAY'

        if len(arErrors) > 0:
            print(' '.join(arErrors))

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
        arErrors = list()

        # 7.客戶名稱CustomerName
        # x僅能為中英數字格式
        # *預設最大長度為60碼
        if len(arParameters['CustomerName'].decode('utf-8')) > 60:
            arErrors.append('7:CustomerName max length as 60.')

        # 20.21.22.23.24.25.商品資訊
        # *不可為空
        if sys.getsizeof(arParameters['Items']) == 0:
            arErrors.append('20-25:Items is required.')

        # 檢查是否存在保留字元'|'
        else:
            bFind_Tag = True
            bError_Tag = False
            for val in arParameters['Items']:
                bFind_Tag = val['ItemName'].find('|')
                if bFind_Tag != -1 or not val['ItemName']:
                    bError_Tag = True
                    arErrors.append('20:Invalid ItemName.')
                    break
                bFind_Tag = str(val['ItemCount']).find('|')
                if bFind_Tag != -1 or not val['ItemCount']:
                    bError_Tag = True
                    arErrors.append('21:Invalid ItemCount.')
                    break
                bFind_Tag = val['ItemWord'].find('|')
                if bFind_Tag != -1 or not val['ItemWord']:
                    bError_Tag = True
                    arErrors.append('22:Invalid ItemWord.')
                    break
                bFind_Tag = str(val['ItemPrice']).find('|')
                if bFind_Tag != -1 or val['ItemPrice'] < 0:
                    bError_Tag = True
                    arErrors.append('23:Invalid ItemPrice.')
                    break
                bFind_Tag = str(val['ItemTaxType']).find('|')
                if bFind_Tag != -1 or not val['ItemTaxType']:
                    if arParameters['TaxType'] == EcpayTaxType.Mix:
                        bError_Tag = True
                        arErrors.append('24:Invalid ItemTaxType.')
                        break
                bFind_Tag = str(val['ItemAmount']).find('|')
                if bFind_Tag != -1 or val['ItemAmount'] < 0:
                    bError_Tag = True
                    arErrors.append('25:Invalid ItemAmount.')
                    break

                # 檢查商品格式
            if not bError_Tag:
                for val in arParameters['Items']:
                    # * ItemCount數字判斷
                    if re.match('^[0-9]*$', str(val['ItemCount'])) == None:
                        arErrors.append('21:Invalid ItemCount.')
                    # *ItemWord預設最大長度為6碼
                    if len(val['ItemWord']) > 6:
                        arErrors.append('22:ItemWord max length as 6.')
                    # *ItemPrice數字判斷
                    if re.match('^[-+]?[0-9]*\.[0-9]+$', str(val['ItemPrice'])) == None:
                        # 又不是整數，跳出錯誤訊息
                        if re.match('^[0-9]*$',str(val['ItemPrice'])) == None:
                            arErrors.append('23:Invalid ItemPrice.A')
                    # *ItemAmount數字判斷
                    if re.match('^[-0-9]*$', str(val['ItemAmount'])) == None:
                        arErrors.append('25:Invalid ItemAmount.B')

        # 37.發票號碼InvoiceNo
        #  *必填項目
        if len(arParameters['InvoiceNo']) == 0:
            arErrors.append('37:InvoiceNo is required.')
        # *預設長度固定10碼
        if len(arParameters['InvoiceNo']) != 10:
            arErrors.append('37:InvoiceNo length as 10.')

        # 38.通知類別AllowanceNotify
        # *固定給定下述預設值
        if arParameters['AllowanceNotify'] != EcpayAllowanceNotifyType.Sms\
                and arParameters['AllowanceNotify'] != EcpayAllowanceNotifyType.Email\
                and arParameters['AllowanceNotify'] != EcpayAllowanceNotifyType.All\
                and arParameters['AllowanceNotify'] != EcpayAllowanceNotifyType.No:
            arErrors.append('38:Invalid AllowanceNotifyType.')
        # 39.通知電子信箱 NotifyMail
        # *若客戶電子信箱有值時，則格式僅能為Email的標準格式
        if len(arParameters['NotifyMail']) > 0:
            if re.match('^[a-z0-9&\'\.\-_\+]+@[a-z0-9\-_]+\.([a-z0-9\-_]+\.)*?[a-z]+$', arParameters['NotifyMail']) == None:
                arErrors.append('39:Invalid Email Format.')
        # *下述情況通知電子信箱不可為空值(通知類別為E-電子郵件)
        if arParameters['AllowanceNotify'] == EcpayAllowanceNotifyType.Email \
                and len(arParameters['NotifyMail']) == 0:
            arErrors.append('39:NotifyMail is required.')
        # 40.通知手機號碼 NotifyPhone
        # *若客戶手機號碼有值時，則預設格式為數字組成
        if len(arParameters['NotifyPhone']) > 0:
            if re.match('^[0-9]*$',arParameters['NotifyPhone']) == None:
                arErrors.append('40:Invalid NotifyPhone.')
        # * 最大20字元
        if len(arParameters['NotifyPhone']) > 20:
            arErrors.append('40:NotifyPhone max length as 20.')
        # *下述情況通知手機號碼不可為空值(通知類別為S-簡訊)
        if arParameters['AllowanceNotify'] == EcpayAllowanceNotifyType.Sms \
                and len(arParameters['NotifyPhone']) == 0:
            arErrors.append('40:NotifyPhone is required.')
        # 39-40 通知電子信箱、通知手機號碼不能全為空值 (如果狀態為SMS 或 EMAIL)
        if len(arParameters['NotifyPhone']) == 0 and len(arParameters['NotifyMail']) == 0 and \
                (arParameters['AllowanceNotify'] == EcpayAllowanceNotifyType.Sms or
                 arParameters['AllowanceNotify'] == EcpayAllowanceNotifyType.Email):
            arErrors.append('39-40:NotifyMail or NotifyPhone is required.')
        else:
            # *下述情況通知手機號碼與電子信箱不可為空值(通知類別為A-皆通知)
            if arParameters['AllowanceNotify'] == EcpayAllowanceNotifyType.All and\
                    (len(arParameters['NotifyMail']) == 0 or
                     len(arParameters['NotifyPhone']) == 0):
                arErrors.append('39-40:NotifyMail And NotifyPhone is required.')
            # *下述情況通知手機號碼與電子信箱為空值(通知類別為N-皆不通知)
            if arParameters['AllowanceNotify'] == EcpayAllowanceNotifyType.No and\
                    (len(arParameters['NotifyMail']) > 0 and len(arParameters['NotifyPhone']) > 0 ):
                arErrors.append('39-40:Please remove NotifyMail And NotifyPhone.')

        # 41.折讓單總金額 AllowanceAmount
        # *必填項目
        if len(str(arParameters['AllowanceAmount'])) == 0:
            arErrors.append('41:AllowanceAmount is required.')
        else:
            # *含稅總金額
            arParameters['AllowanceAmount'] = int(arParameters['AllowanceAmount'])

        if len(arErrors) > 0:
            print(' '.join(arErrors))

        # 刪除items
        del arParameters['Items']

        return arParameters

    '''
    *4欄位例外處理方式(送壓碼前)
    '''
    def check_exception(self, arParameters = dict):
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
        arErrors = list()
        # 42.發票號碼 InvoiceNumber

        # *必填項目
        if len(arParameters['InvoiceNumber']) == 0:
            arErrors.append('42:InvoiceNumber is required.')
        # *預設長度固定10碼
        if len(arParameters['InvoiceNumber']) != 10:
            arErrors.append('42:InvoiceNumber length as 10.')

        # 43.作廢原因 Reason
        # *必填欄位
        if len(arParameters['Reason']) == 0:
            arErrors.append('43:Reason is required.')

        # *字數限制在20(含)個字以內
        if len(arParameters['Reason']) > 20:
            arErrors.append('43:Reason max length as 20.')

        if len(arErrors) > 0:
            print(' '.join(arErrors))

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

        arErrors = list()

        # 37.發票號碼InvoiceNo
        #  *必填項目
        if len(arParameters['InvoiceNo']) == 0:
            arErrors.append('37:InvoiceNo is required.')
        # *預設長度固定10碼
        if len(arParameters['InvoiceNo']) != 10:
            arErrors.append('37:InvoiceNo length as 10.')

        # 43.作廢原因 Reason
        # *必填欄位
        if len(arParameters['Reason']) == 0:
            arErrors.append('43:Reason is required.')

        # *字數限制在20(含)個字以內
        if len(arParameters['Reason']) > 20:
            arErrors.append('43:Reason max length as 20.')

        # 44.折讓編號 AllowanceNo
        if len(arParameters['AllowanceNo']) == 0:
            arErrors.append('44:AllowanceNo is required.')
        # *若有值長度固定16字元
        if len(arParameters['AllowanceNo']) != 0 and len(arParameters['AllowanceNo']) != 16:
            arErrors.append('44:AllowanceNo length as 16.')

        if len(arErrors) > 0:
            print(' '.join(arErrors))

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

        arErrors = list()

        # *預設不可為空值
        if len(arParameters['RelateNumber']) == 0:
            arErrors.append('4:RelateNumber is required.')
        # *預設最大長度為30碼
        if len(arParameters['RelateNumber']) > 30:
            arErrors.append('4:RelateNumber max langth as 30.')

        if len(arErrors) > 0:
            print(' '.join(arErrors))

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

        arErrors = list()

        # 4.廠商自訂編號

        # * 預設不可為空值
        if len(arParameters['RelateNumber']) == 0:
            arErrors.append('4:RelateNumber is required.')
        # *預設最大長度為30碼
        if len(arParameters['RelateNumber']) > 30:
            arErrors.append('4:RelateNumber max langth as 30.')

        if len(arErrors) > 0:
            print(' '.join(arErrors))

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
        arErrors = list()

        # 37.發票號碼InvoiceNo
        #  *必填項目
        if len(arParameters['InvoiceNo']) == 0:
            arErrors.append('37:InvoiceNo is required.')
        # *預設長度固定10碼
        if len(arParameters['InvoiceNo']) != 10:
            arErrors.append('37:InvoiceNo length as 10.')

        # 44.折讓編號 AllowanceNo
        if len(arParameters['AllowanceNo']) == 0:
            arErrors.append('44:AllowanceNo is required.')
        # *若有值長度固定16字元
        if len(arParameters['AllowanceNo']) != 0 and len(arParameters['AllowanceNo']) != 16:
             arErrors.append('44:AllowanceNo length as 16.')

        if len(arErrors) > 0:
            print(' '.join(arErrors))

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
        arErrors = list()

        # 37.發票號碼InvoiceNo
        #  *必填項目
        if len(arParameters['InvoiceNo']) == 0:
            arErrors.append('37:InvoiceNo is required.')
        # *預設長度固定10碼
        if len(arParameters['InvoiceNo']) != 10:
            arErrors.append('37:InvoiceNo length as 10.')

        # 44.折讓編號 AllowanceNo
        if len(arParameters['AllowanceNo']) == 0:
            arErrors.append('44:AllowanceNo is required.')
        # *若有值長度固定16字元
        if len(arParameters['AllowanceNo']) != 0 and len(arParameters['AllowanceNo']) != 16:
            arErrors.append('44:AllowanceNo length as 16.')

        if len(arErrors) > 0:
            print(' '.join(arErrors))

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
        arErrors = list()

        # 37.發票號碼InvoiceNo
        #  *必填項目
        if len(arParameters['InvoiceNo']) == 0:
            arErrors.append('37:InvoiceNo is required.')
        # *預設長度固定10碼
        if len(arParameters['InvoiceNo']) != 10:
            arErrors.append('37:InvoiceNo length as 10.')

        # 44.折讓編號 AllowanceNo
        if arParameters['InvoiceTag'] == EcpayInvoiceTagType.Allowance or arParameters['InvoiceTag'] == EcpayInvoiceTagType.Allowance_Void:
            if len(arParameters['AllowanceNo']) == 0:
                arErrors.append('44:AllowanceNo is required.')
            # *若有值長度固定16字元
            if len(arParameters['AllowanceNo']) != 0 and len(arParameters['AllowanceNo']) != 16:
                arErrors.append('44:AllowanceNo length as 16.')

        # 45.NotifyMail 發送電子信箱
        # *若客戶電子信箱有值時，則格式僅能為Email的標準格式
        if len(arParameters['NotifyMail']) > 0:
            if re.match("^[a-z0-9&\'\.\-_\+]+@[a-z0-9\-_]+\.([a-z0-9\-_]+\.)*?[a-z]+$", arParameters['NotifyMail']) == None:
                arErrors.append('45:Invalid Email Format.')

        # *下述情況通知電子信箱不可為空值(發送方式為E-電子郵件)
        if arParameters['Notify'] == EcpayNotifyType.Email and len(arParameters['NotifyMail']) == 0:
            arErrors.append('39:NotifyMail is required.')

        # 46.通知手機號碼 NotifyPhone
        # *若客戶手機號碼有值時，則預設格式為數字組成
        if len(arParameters['Phone']) > 0:
            if re.match("^[0-9]*$", arParameters['Phone']) == None:
                arErrors.append('46:Invalid Phone.')

        # *最大長度為20碼
        if len(arParameters['Phone']) > 20:
            arErrors.append('46:Phone max length as 20.')

        # *下述情況通知手機號碼不可為空值(發送方式為S-簡訊)
        if arParameters['Notify'] == EcpayNotifyType.Sms and len(arParameters['Phone']) > 0:
            arErrors.append('46:Phone is required.')

        # 45-46 發送簡訊號碼、發送電子信箱不能全為空值
        if len(arParameters['Phone']) == 0 and len(arParameters['NotifyMail']) == 0:
            arErrors.append('45-46:NotifyMail or Phone is required.')
        else:
            if arParameters['Notify'] == EcpayNotifyType.All and\
                    (len(arParameters['NotifyMail']) == 0 or len(arParameters['Phone']) == 0):
                arErrors.append('45-46:NotifyMail and Phone is required.')


        # 47. 發送方式 Notify
        # *固定給定下述預設值
        if arParameters['Notify'] != EcpayNotifyType.Sms and\
                arParameters['Notify'] != EcpayNotifyType.Email and\
                arParameters['Notify'] != EcpayNotifyType.All:
            arErrors.append('47:Notify is required.')

        # 48.發送內容類型 InvoiceTag
        # *固定給定下述預設值
        if arParameters['InvoiceTag'] != EcpayInvoiceTagType.Invoice and\
                arParameters['InvoiceTag'] != EcpayInvoiceTagType.Invoice_Void and\
                arParameters['InvoiceTag'] != EcpayInvoiceTagType.Allowance and\
                arParameters['InvoiceTag'] != EcpayInvoiceTagType.Allowance_Void and\
                arParameters['InvoiceTag'] != EcpayInvoiceTagType.Invoice_Winning:
            arErrors.append('48:InvoiceTag is required.')

        # 49.發送對象 Notified
        # *固定給定下述預設值
        if arParameters['Notified'] != EcpayNotifiedType.Customer and\
                arParameters['Notified'] != EcpayNotifiedType.vendor and\
                arParameters['Notified'] != EcpayNotifiedType.All:
            arErrors.append('49:Notified is required.')

        if len(arErrors) > 0:
            print(' '.join(arErrors))

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
        arErrors = list()

        # 33.交易單號Tsr
        # *必填項目
        if len(arParameters['Tsr']) == 0:
            arErrors.append('33:Tsr is required.')

        # *判斷最大字元是否超過30字
        if len(arParameters['Tsr']) > 30:
            arErrors.append('33:Tsr max length as 30.')

        # 34.交易類別PayType
        # *2016-10-04 修改為僅允許2
        if arParameters['PayType'] != EcpayPayTypeCategory.Ecpay:
            arErrors.append("34:Invalid PayType.")

        if len(arErrors) > 0:
            print(' '.join(arErrors))

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
        arErrors = list()

        # 50.BarCode 手機條碼
        # *僅能為8碼且為必填
        if len(arParameters['BarCode']) != 8:
            arErrors.append("50:BarCode max length as 8.")

        if len(arErrors) > 0:
            print(' '.join(arErrors))

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
        arErrors = list()

        # 51.LoveCode愛心碼
        # *必填 3-7碼
        if len(arParameters['LoveCode']) > 7:
            arErrors.append("51:LoveCode max length as 7.")

        if len(arErrors) > 0:
            print(' '.join(arErrors))

        return arParameters

    '''
    * 4欄位例外處理方式(送壓碼前)
    '''

    def check_exception(self, arParameters=dict):
        return arParameters



