綠界電子發票Python模組
=======================

綠界電子發票

安裝
-----


利用pip

.. code-block::

    pip install ecpay_invoice

匯入模組

.. code-block::

    from ecpay_invoice.ecpay_main import *

其他範例請看demo

change log:

2018-08-14 v1.0.7 修正ItemTaxtType非必填，修正執行第二次初始字典會被修改問題。

2018-08-10 v1.0.6 更新CustomerName最大可以到60個字

2018-08-09 v1.0.5 修正lovecode判定，移除raise錯誤，只印出錯誤訊息供參考

2018-08-06 v1.0.4 更新CustomerIdentifier錯誤判斷

2018-08-02 v1.0.3 更新錯誤提示方式

2018-07-30 v1.0.1 更新錯誤判斷式

2018-07-19 v1.0 更新demo範例註解

2018-07-17 v0.9 更新商品單價可以為小數，諾驗證沒有通過會停止程式

