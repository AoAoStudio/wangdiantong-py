# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from wangdiantong.api.base import BaseAPIEndpoint


class OrderAPI(BaseAPIEndpoint):
    """
    Order

    Docs:
        http://112.126.83.15/open_api/wordpress/2018/05/30/%E8%AE%A2%E5%8D%95api/
    """


    """
    接口名称	接口功能描述	接口简称	ERP功能界面的操作路径
    stockin_refund_push.php	创建ERP销售退货入库单	创建销售退货入库单	库存-》入库管理-》退货入库单管理界面
    stockin_order_query_refund.php	查询ERP中退换入库单信息	查询退换入库单	库存-》入库管理-》退货入库单管理界面
    trade_push.php	订单推送到ERP系统中；更新ERP原始订单信息	创建原始订单	订单-》原始订单界面）
    trade_query.php	查询ERP中系统订单	查询系统订单	订单-》订单管理界面
    logistics_sync_query.php	将erp中已发货的处于等待同步的订单抓取到进行物流同步	查询物流同步	订单-》物流同步界面
    logistics_sync_ack.php	将同步的结果回传到erp系统，系统会更新物流同步状态	物流同步状态回写	
    api_goods_stock_change_query.php	查询出ERP中库存发生了变化，此时平台和ERP的库存不一致的货品库存，然后去修改平台上的货品库存	查询库存同步	设置-》策略设置-》库存同步
    api_goods_stock_change_ack.php	将同步结果回传到ERP系统，这样下次再查询库存的时候，就不会再把这次已经库存同步了的货品查出来。	平台货品库存同步状态回写	
    sales_refund_push.php	已经发货的订单，如果退款或退货，需要调用该接口 创建原始退款单	创建原始退款单	订单-》原始退款单
    refund_query.php	查询ERP中退货或者换货的订单信息	查询退换管理	订单-》退换管理界面
    """

    def trade_query(self):
        """
        查询ERP中系统订单

        :return:
        """
        pass