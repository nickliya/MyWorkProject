# -*- coding: utf-8 -*-
"""微信小程序支付接口测试"""
from privateFun.pay import *
import xmltodict
import json
import requests
import re

dataxml = '''
<xml>
  <appid><![CDATA[wx0990efa71fd864b8]]></appid>
  <attach><![CDATA[nisda]]></attach>
  <bank_type><![CDATA[CFT]]></bank_type>
  <fee_type><![CDATA[CNY]]></fee_type>
  <is_subscribe><![CDATA[Y]]></is_subscribe>
  <mch_id><![CDATA[1336809401]]></mch_id>
  <nonce_str><![CDATA[5d2b6c2a8db53831f7eda20af46e531c]]></nonce_str>
  <openid><![CDATA[oUpF8uMEb4qRXf22hE3X68TekukE]]></openid>
  <out_trade_no><![CDATA[1190214610495749A]]></out_trade_no>
  <result_code><![CDATA[SUCCESS]]></result_code>
  <return_code><![CDATA[SUCCESS]]></return_code>
  <sub_mch_id><![CDATA[10000100]]></sub_mch_id>
  <time_end><![CDATA[20140903131540]]></time_end>
  <total_fee>1</total_fee>
  <trade_type><![CDATA[JSAPI]]></trade_type>
  <transaction_id><![CDATA[1004400740201409030005092168]]></transaction_id>
</xml>'''

dataxml2 = '''
<xml>
  <appid><![CDATA[wx0990efa71fd864b8]]></appid>
  <attach><![CDATA[中文测试]]></attach>
  <bank_type><![CDATA[CFT]]></bank_type>
  <fee_type><![CDATA[CNY]]></fee_type>
  <is_subscribe><![CDATA[Y]]></is_subscribe>
  <mch_id><![CDATA[1336809401]]></mch_id>
  <nonce_str><![CDATA[5d2b6c2a8db53831f7eda20af46e531c]]></nonce_str>
  <openid><![CDATA[oUpF8uMEb4qRXf22hE3X68TekukE]]></openid>
  <out_trade_no><![CDATA[1190214610495749A]]></out_trade_no>
  <result_code><![CDATA[FAIL]]></result_code>
  <err_code><![CDATA[FAIL]]></err_code>
  <err_code_des><![CDATA[SYSTEMERROR]]></err_code_des>
  <return_code><![CDATA[系统错误]]></return_code>
  <sub_mch_id><![CDATA[10000100]]></sub_mch_id>
  <time_end><![CDATA[20140903131540]]></time_end>
  <total_fee>1</total_fee>
  <trade_type><![CDATA[JSAPI]]></trade_type>
  <transaction_id><![CDATA[1004400740201409030005092168]]></transaction_id>
</xml>'''

xmlparse = xmltodict.parse(dataxml)
jsondata = json.loads(json.dumps(xmlparse))

key = "9g5389qhcf5nw9vp5bmr1kre2ax0ywyf"
sign = wxsign(jsondata["xml"], key)

jsondata["xml"]["sign"] = sign

postxml2 = xmltodict.unparse(jsondata).encode('utf-8')
postxml = xmltodict.unparse(jsondata, pretty=True)


def addcdata(s):
    a = s
    return "<![CDATA[%s]]>" % s


r = r'<.*?>.*?</.*?>'
postxml3 = re.sub(r, addcdata, postxml)

# url = "http://pre-4s.mysirui.com/basic/account/WXAppletCallBack"  # 小程序
# url = "http://pre-4s.mysirui.com/basic/account/wxPayFinishPayCallback"  # 微信
url = "http://192.168.6.49:8088/basic/account/wxPayFinishPayCallback"  # 微信
# url = "http://192.168.6.49:8088/basic/account/WXAppletCallBack"

r = requests.post(url=url, data=postxml2, headers={'Content-Type': 'text/xml'})

print(r.text)
