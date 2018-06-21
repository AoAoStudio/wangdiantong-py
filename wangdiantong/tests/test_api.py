# -*- coding: utf-8 -*-
import datetime
import os
from pprint import pprint
import logging
import unittest

from wangdiantong import settings as wdt
from wangdiantong.client import OpenApiClient
from wangdiantong.client.base import Signer
from wangdiantong.utils import force_bytes

logger = logging.getLogger(__name__)

from .mock import GOODS_PLATFORM
class OpenapiTestCase(unittest.TestCase):

    def setUp(self):
        wdt.APPSECRET = os.environ.get('APPSECRET', 'CHANGE-ME')
        wdt.APPKEY = os.environ.get('APPKEY', 'CHANGE-ME')
        wdt.SID = os.environ.get('SID', 'CHANGE-ME')
        wdt.SHOP_NO = os.environ.get('SHOP_NO', 'CHANGE-ME')
        wdt.PLATFORM_ID = os.environ.get('PLATFORM_ID', 'CHANGE-ME')

        self.shop_no = wdt.SHOP_NO
        self.platform_id = wdt.PLATFORM_ID
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
        logger.info(request)
        logger.info(signed_str)

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
        data = self.openapi.stocks.change_query(shop_no=self.shop_no, limit=100)
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
        self.assertIn('current_count', keys)

    def test_stocks_change_ack(self):
        data = self.openapi.stocks.sync_ack(stock_sync_list=[
            self.openapi.stocks.item_for_ack(1, 100, 20000)]
        )
        self.assertEqual(data['code'], self.openapi.CODE.SUCCESS, data)
        logger.info(data)

    def test_stocks_query(self):
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(days=10)

        data = self.openapi.stocks.query(start_time=start_time,
                                         end_time=end_time,
                                         spec_no='xzabcde-03')
        self.assertEqual(data['code'], self.openapi.CODE.SUCCESS, data)

        keys = list(data.keys())
        self.assertIn('stocks', keys)
        self.assertIn('total_count', keys)

    def test_order_trade_query(self):
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(hours=1)
        data = self.openapi.orders.trade_query(start_time=start_time,
                                               end_time=end_time,
                                               trade_no="123123",
                                               img_url=1,
                                               )
        logger.info(data)
        self.assertEqual(data['code'], self.openapi.CODE.SUCCESS, data)

        keys = list(data.keys())
        self.assertIn('trades', keys)
        self.assertIn('total_count', keys)

    def test_goods_query(self):
        """

        goods query response data

        >>> data = {u'code': 0, u'goods_list': [
        >>>          {u'alias': u'',
        >>>           u'aux_unit_name': None,
        >>>           u'brand_name': u'\u65e0',
        >>>           u'brand_no': u'BRAND',
        >>>           u'class_name': u'\u65e0',
        >>>           u'flag_name': None,
        >>>           u'goods_id': u'209811',
        >>>           u'goods_modified': u'2018-06-06 11:26:37',
        >>>           u'goods_name': u'CESHI20180606',
        >>>           u'goods_no': u'CESHI20180606',
        >>>           u'goods_type': u'1',
        >>>           u'origin': u'',
        >>>           u'pinyin': u'',
        >>>           u'prop1': u'',
        >>>           u'prop2': u'',
        >>>           u'prop3': u'',
        >>>           u'prop4': u'',
        >>>           u'prop5': u'',
        >>>           u'prop6': u'',
        >>>           u'remark': u'',
        >>>           u'short_name': u'',
        >>>           u'spec_count': u'1',
        >>>           u'spec_list': [
        >>>            {u'barcode': u'CESHI20180606S',
        >>>             u'custom_price1': u'0.0000',
        >>>             u'custom_price2': u'0.0000',
        >>>             u'goods_id': u'209811',
        >>>             u'height': u'0.0000',
        >>>             u'img_url': u'',
        >>>             u'is_allow_neg_stock': u'1',
        >>>             u'is_lower_cost': u'0',
        >>>             u'is_not_need_examine': u'0',
        >>>             u'is_not_use_air': u'0',
        >>>             u'is_sn_enable': u'0',
        >>>             u'is_zero_cost': u'1',
        >>>             u'large_type': u'0',
        >>>             u'length': u'0.0000',
        >>>             u'lowest_price': u'0.0000',
        >>>             u'market_price': u'0.0000',
        >>>             u'member_price': u'0.0000',
        >>>             u'pack_score': u'0',
        >>>             u'pick_score': u'0',
        >>>             u'prop1': u'',
        >>>             u'prop2': u'',
        >>>             u'prop3': u'',
        >>>             u'prop4': u'',
        >>>             u'prop5': u'',
        >>>             u'prop6': u'',
        >>>             u'receive_days': u'0',
        >>>             u'remark': u'',
        >>>             u'retail_price': u'0.0000',
        >>>             u'sale_score': u'0',
        >>>             u'sales_days': u'0',
        >>>             u'spec_aux_unit_name': None,
        >>>             u'spec_code': u'',
        >>>             u'spec_modified': u'2018-06-06 11:26:37',
        >>>             u'spec_name': u'\u767d\u8272L',
        >>>             u'spec_no': u'CESHI20180606S',
        >>>             u'spec_unit_name': None,
        >>>             u'tax_rate': u'0.0000',
        >>>             u'validity_days': u'0',
        >>>             u'weight': u'0.0000',
        >>>             u'wholesale_price': u'0.0000',
        >>>             u'width': u'0.0000'}],
        >>>           u'unit_name': None}],
        >>>         u'message': u'',
        >>>         u'total_count': u'1'}
        """

        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(hours=1)
        data = self.openapi.goods.query(start_time=start_time,
                                        end_time=end_time,
                                        spec_no='xzabcde-01'
                                        )
        logger.info(data)
        self.assertEqual(data['code'], self.openapi.CODE.SUCCESS, data)

        keys = list(data.keys())
        self.assertIn('goods_list', keys)
        self.assertIn('total_count', keys)

    def test_trade_push(self):
        """测试推送原始订单"""
        trade_list = [{
            "tid": "xztrade-01",
            "trade_status": 30,
            "pay_status": 2,
            "delivery_term": 1,
            "trade_time": "2015-01-01 10:0:0",
            "pay_time": "",
            "buyer_nick": "行者王",
            "buyer_email": "",
            "pay_id": "1212121",
            "pay_account": "pay@pay.com",
            "receiver_name": "测试者",
            "receiver_province": "北京",
            "receiver_city": "北京市",
            "receiver_district": "昌平区",
            "receiver_address": "天通苑",
            "receiver_mobile": "15345543211",
            "receiver_telno": "",
            "receiver_zip": "",
            "logistics_type": "-1",
            "invoice_type": 1,
            "invoice_title": "行者抬头",
            "buyer_message": "行者留言",
            "seller_memo": "卖家备注",
            "seller_flag": "0",
            "post_amount": "10",
            "cod_amount": 0,
            "ext_cod_fee": 0,
            "paid": 20,
            "order_list": [{
                "oid": "xzorder-01",
                "num": 2,
                "price": 10,
                "status": 30,
                "refund_status": 0,
                "goods_id": "1001",
                "spec_id": "1001",
                "goods_no": "xzabcde",
                "spec_no": "xzabcde-01",
                "goods_name": "测试用例1",
                "spec_name": "规格01",
                "adjust_amount": 0,
                "discount": 10,
                "share_discount": 0,
                "cid": "",
            }]
        }]
        data = self.openapi.orders.trade_push(shop_no=self.shop_no, trade_list=trade_list)
        logger.info(data)
        self.assertEqual(data['code'], self.openapi.CODE.SUCCESS, data)

    def test_goods_push_platfrom(self):
        goods_list = [GOODS_PLATFORM]
        data = self.openapi.goods.goods_push_platfrom(self.shop_no,
                                                      self.platform_id,
                                                      goods_list)
        self.assertEqual(data['code'], self.openapi.CODE.SUCCESS, data)

if __name__ == '__main__':
    unittest.main()
