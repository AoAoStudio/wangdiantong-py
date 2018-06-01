# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json

from wangdiantong.api.base import BaseAPIEndpoint


class StocksAPI(BaseAPIEndpoint):
    """ Goods Stocks

    Docs:
        http://112.126.83.15/open_api/wordpress/2017/04/11/%E6%9F%A5%E8%AF%A2%E5%BA%93%E5%AD%98%E5%90%8C%E6%AD%A5/
    """

    def change_query(self, shop_no, limit):
        """
        查询库存同步

        :param str shop_no: varchar(20) required 店铺编号
        :param int limit: int(4) 最多返回条数
        :return:
        """
        data = dict(
            shop_no=shop_no,
            limit=limit
        )
        return self._post("/openapi2/api_goods_stock_change_query.php", data=data)

    def sync_ack(self,  stock_sync_list):
        """
        平台货品库存同步状态回写

        :param list stock_sync_list: [dict(rec_id=1, sync_stoc=100, stock_change_count=5634245)]
        :return:
        """
        data = dict(
            stock_sync_list=json.dumps(stock_sync_list)
        )
        return self._post("/openapi2/api_goods_stock_change_ack.php", data=data)

    def item_for_ack(self, rec_id, sync_stock, stock_change_count):
        """
        sync_ack 请求参数 stock_sync_list的元素

        :param int rec_id: int(11) required Erp内平台货品表主键id
        :param int sync_stock: int(11) required 货品库存
        :param int stock_change_count: int(11) required 库存变化时自增
        :return:
        """
        return dict(
            rec_id=rec_id,
            sync_stock=sync_stock,
            stock_change_count=stock_change_count
        )