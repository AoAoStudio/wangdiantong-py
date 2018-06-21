#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zs
#   E-mail  :   zs1213yh@gmail.com
#   Description: mockdata
import copy

##### 平台货品示例 ####
# GOODS_PLATFORM = dict(
#     status=1,
#     goods_id=1,
#     goods_no='xzsc0001',
#     goods_name='行者0001商品',
#     spec_id=1,
#     spec_no='xzsc0001-a',
#     stock_num=10,
#     price=12.4
# )

GOODS_PLATFORM = {
    "status": 1,
    "goods_id": 1,
    "goods_no": "xzsc0001",
    "goods_name": "行者0001商品",
    "spec_id": 1,
    "spec_no": "xzsc0001-a",
    "stock_num": 10,
    "price": 12.4
}

TRADE_SUB = {
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
}

TRADE = {
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
    "order_list": []
}


class MockData(object):
    @staticmethod
    def trade_single(order_no, goods_no, spec_no):
        trade = copy.deepcopy(TRADE)
        trade_sub = copy.deepcopy(TRADE_SUB)
        trade['tid'] = order_no
        trade_sub['oid'] = order_no
        trade_sub['goods_no'] = goods_no
        trade_sub['spec_no'] = spec_no
        trade['order_list'].append(trade_sub)
        return trade

    @staticmethod
    def goods_sigle(goods_id=1):
        return GOODS_PLATFORM
