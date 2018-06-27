#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zs
#   E-mail  :   zs1213yh@gmail.com

# -*- coding: utf-8 -*-
import datetime
import os
import unittest
import json
from pprint import pprint
import logging

logger = logging.getLogger(__name__)

from wangdiantong.client import OpenApiClient
from wangdiantong import settings as wdt
from .mock import MockData


class OrderTransactionTestCase(unittest.TestCase):
    def setUp(self):
        wdt.APPSECRET = os.environ.get('WANGDIANTONG_APPSECRET', 'CHANGE-ME')
        wdt.APPKEY = os.environ.get('WANGDIANTONG_APPKEY', 'CHANGE-ME')
        wdt.SID = os.environ.get('WANGDIANTONG_SID', 'CHANGE-ME')
        wdt.SHOP_NO = os.environ.get('WANGDIANTONG_SHOP_NO', 'CHANGE-ME')
        wdt.PLATFORM_ID = os.environ.get('WANGDIANTONG_SPLATFORM_ID', 'CHANGE-ME')

        self.shop_no = wdt.SHOP_NO
        self.platform_id = wdt.PLATFORM_ID
        self.openapi = OpenApiClient(
            sid=wdt.SID,
            appkey=wdt.APPKEY,
            appsecret=wdt.APPSECRET,
        )
        self.mock_data = MockData

    def test_order_push_success_stock_query(self):
        trade_no = 'xztrade-21'
        goods_no = 'xzabcde'
        # goods_no = 'sku0011'
        spec_no = 'xzabcde-03'
        # spec_no = 'sku0011'
        # trade_data = self.mock_data.trade_single(trade_no, goods_no, spec_no)
        # # self.shop_no = '20160817023956'
        # data_trade_push = self.openapi.orders.trade_push(shop_no=self.shop_no,
        #                                                  trade_list=[
        #                                                      trade_data])
        # self.assertEqual(data_trade_push['code'],
        #                  self.openapi.CODE.SUCCESS, data_trade_push)

        start_time = datetime.datetime.now() - datetime.timedelta(hours=1)
        end_time = start_time + datetime.timedelta(days=10)

        data_stock_query = self.openapi.stocks.query(
            start_time=start_time,
            end_time=end_time,
            spec_no=spec_no)
        self.assertEqual(data_stock_query['code'],
                         self.openapi.CODE.SUCCESS,
                         data_stock_query)
        data = self.openapi.stocks.change_query(shop_no=self.shop_no, limit=10)
        self.assertEqual(data['code'], self.openapi.CODE.SUCCESS, data)

        keys = list(data.keys())
        self.assertIn('stock_change_list', keys)
        # ack handle 防止下次不能查库存
        stock_sync_list = []
        for item in data['stock_change_list']:
            rec_id = item['rec_id']
            sync_stock = item['sync_stock']
            stock_change_count = item['stock_change_count']
            stock_sync_list.append(
                self.openapi.stocks.item_for_ack(
                    rec_id,
                    sync_stock,
                    stock_change_count
                )
            )
        if stock_sync_list:
            data_ack = self.openapi.stocks.sync_ack(stock_sync_list=stock_sync_list)
            self.assertEqual(data_ack['code'], self.openapi.CODE.SUCCESS, data_ack)
