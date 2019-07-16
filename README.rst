綠界電子發票 Python 3
=====================


綠界電子發票建置中...

安裝
----

利用pip

.. code-block:: python

    pip install ecpay_invoice3



匯入模組

.. code-block:: python

    from ecpay_invoice.ecpay_main import *



其他範例請看demo

change log:

2019-07-05 v1.1.1 移除所有驗證資訊，統一由後端server驗證

2019-01-07 v1.1.0 修正延遲開立的驗證ItemTaxtType欄位錯誤

2019-01-05 v1.0.9 修正折讓與延遲開立的驗證ItemTaxtType欄位錯誤

2018-08-27 v1.0.8 修正urlencode將空白轉成%20 bug

2018-08-14 v1.0.7 修正ItemTaxtType非必填，修正執行第二次初始字典會被修改問題。

2018-08-13 v1.0.6 更新CustomerName最大可以到60個字

2018-07-30 v1.0 Python3 初版



