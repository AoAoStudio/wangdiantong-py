# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime
from wangdiantong.api.base import BaseAPIEndpoint


class GoodsAPI(BaseAPIEndpoint):

    def query(self, start_time, end_time,
                    spec_no=None, goods_no=None,
                    page_no=0, page_size=40, **kwargs):
        """
        查询货品档案

        Docs:
            OpenApi:   /openapi2/goods_query.php
            奇门云网官: method=wdt.goods.query

        :param datetime start_time: str datetime.strftime("%Y-%m-%d %H:%M:%S"), required 最后更新时间，开始日期
        :param datetime end_time: str datetime.strftime("%Y-%m-%d %H:%M:%S"), required  最后更新时间，结束日期
        :param int page_no: int(10), required 页号,默认0，从0页开始
        :param int page_size: int(10), required 分页大小（最大不超过40条，默认返回40条）

        :param str spec_no: varchar(40) 商家编码（如果不传时间，则spec_no和goods_no必须传一个）
        :param str goods_no: varchar(4) 货品编号
        :param str brand_no: varchar(32) 品牌编号

        ::kwargs
        :param str class_name: varchar(32) 分类名称
        :param str barcode: varchar(64) 条码

        :return:
        """
        if start_time is None:
            assert goods_no or spec_no

        query = dict(
            start_time=start_time.strftime("%Y-%m-%d %H:%M:%S"),
            end_time=end_time.strftime("%Y-%m-%d %H:%M:%S"),
            page_no=page_no,
            spec_no=spec_no,
            goods_no=goods_no,
            page_size=page_size,
        )
        query.update(**kwargs)
        data = dict(list(filter(lambda x: x[1] is not None, query.items())))
        return self._post("/openapi2/goods_query.php", data=data)



