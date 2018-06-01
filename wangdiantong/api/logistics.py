# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json

from wangdiantong.api.base import BaseAPIEndpoint


class LogisticsAPI(BaseAPIEndpoint):
    """ Logistics
        Docs:
            http://112.126.83.15/open_api/wordpress/2017/04/11/%E6%9F%A5%E8%AF%A2%E7%89%A9%E6%B5%81%E5%90%8C%E6%AD%A5/
    """

    def sync_query(self, shop_no, limit, is_part_sync_able=None):
        """
        查询物流同步

        Docs:
            http://112.126.83.15/open_api/wordpress/2017/04/11/%E6%9F%A5%E8%AF%A2%E7%89%A9%E6%B5%81%E5%90%8C%E6%AD%A5/

        :param str shop_no: varchar(20) required 店铺编号
        :param int limit: int(4) 最多返回条数
        :param int is_part_sync_able: int(4)  是否支持拆单发货
        :return:
        """
        data = dict(
            shop_no=shop_no,
            limit=limit
        )
        if is_part_sync_able is not None:
            data['is_part_sync_able'] = is_part_sync_able
        return self._post("/openapi2/logistics_sync_query.php", data=data)

    def sync_ack(self, logistics_list):
        """
        物流同步状态回写(批量)

        Docs:
            http://112.126.83.15/open_api/wordpress/2017/04/11/%E6%9F%A5%E8%AF%A2%E7%89%A9%E6%B5%81%E5%90%8C%E6%AD%A5/

        :param list logistics_list: [dict(rec_id=1, status=0, message="同步成功", )] 物流同步状态回传列表
        :return:
        """
        data = dict(
            logistics_list=json.dumps(logistics_list)
        )
        return self._post("/openapi2/logistics_sync_ack.php", data=data)

    ACK_SUCCESS = 0
    ACK_SUCCESS_MESSAGE = "同步成功"
    ACK_FAILURE = 1

    def item_for_ack(self, rec_id,
                     status=ACK_SUCCESS, message=ACK_SUCCESS_MESSAGE):
        return dict(
            rec_id=rec_id,
            status=status,
            message=message,
        )