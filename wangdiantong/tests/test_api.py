# -*- coding: utf-8 -*-
import os
import unittest

from wangdiantong.client import OpenApiClient
from wangdiantong.client.base import Signer
from wangdiantong import settings as wdt
from wangdiantong.utils import force_bytes


class OpenapiTestCase(unittest.TestCase):

    def setUp(self):
        wdt.APPSECRET = os.environ.get('APPSECRET', 'CHANGE-ME')
        wdt.APPKEY = os.environ.get('APPKEY', 'CHANGE-ME')
        wdt.SID = os.environ.get('SID', 'CHANGE-ME')
        wdt.SHOP_NO = os.environ.get('SHOP_NO', 'CHANGE-ME')

        self.shop_no = wdt.SHOP_NO
        self.openapi = OpenApiClient(
            sid=wdt.SID,
            appkey=wdt.APPKEY,
            appsecret=wdt.APPSECRET,
        )
        # self.openapi.NOW = int(time.time())

    def test_signer(self):
        signer = Signer(
            sid=wdt.SID,
            appkey=wdt.APPKEY,
            appsecret=wdt.APPSECRET,
        )
        signed_str, request = signer.sign_data(request=dict(
            shop_no=self.shop_no,
            limit=10
        ))
        assert len(signed_str) == 32
        print(request)
        print(signed_str)

    def test_logistics_sync_query(self):
        data = self.openapi.logistics.sync_query(shop_no=self.shop_no, limit=10)
        self.assertEqual(data['code'], self.openapi.CODE.SUCCESS, data)
        self.assertIsInstance(data['trades'], list)

        if not data['trades']: return

        """
        trade = {'rec_id': '3296',
                 'shop_no': 'CHANGE-ME',
                 'tid': 'HP201805311733579305415',
                 'logistics_type': '35',
                 'logistics_no': '48524753313',
                 'delivery_term': '1',
                 'consign_time': '2018-05-31 17:40:42',
                 'contact': '',
                 'mobile': '',
                 'telno': '',
                 'address': '',
                 'oids': '',
                 'is_part_sync': '0',
                 'platform_id': '127',
                 'trade_id': '42097',
                 'logistics_code_erp': 'YS001',
                 'logistics_name_erp': '优速快递',
                 'logistics_name': '优速物流'}
         """

        d1 = data['trades'][0]
        self.assertIn([
            'rec_id',
            'shop_no',
            'tid',
            'logistics_type',
            'logistics_no',
            'delivery_term',
            'consign_time',
            'contact',
            'mobile',
            'telno',
            'address',
            'oids',
            'is_part_sync',
            'platform_id',
            'trade_id',
            'logistics_code_erp',
            'logistics_name_erp',
            'logistics_name',
        ], list(d1.keys()))

    def test_logistics_sync_ack(self):
        data = self.openapi.logistics.sync_ack(logistics_list=[
            self.openapi.logistics.item_for_ack(1)]
        )
        self.assertEqual(data['code'], self.openapi.CODE.SUCCESS, data)
        self.assertEqual(force_bytes(data['errors'][0]['error']),
                         force_bytes('非待同步状态,不可更新'))

    def test_stocks_change_query(self):
        data = self.openapi.stocks.change_query(shop_no=self.shop_no, limit=10)
        self.assertEqual(data['code'], self.openapi.CODE.SUCCESS, data)

        keys = list(data.keys())
        self.assertIn('stock_change_list', keys)
        self.assertIn('current_count', keys)

    def test_stocks_change_ack(self):
        data = self.openapi.stocks.sync_ack(stock_sync_list=[
            self.openapi.stocks.item_for_ack(1, 100, 20000)]
        )
        self.assertEqual(data['code'], self.openapi.CODE.SUCCESS, data)
        print(data)


if __name__ == '__main__':
    unittest.main()
