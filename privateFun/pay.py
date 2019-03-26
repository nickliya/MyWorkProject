# coding=utf-8
# python3
import hashlib


def wxsign(data, privateKey):
    """微信支付签名md5"""
    keylist = list(data.keys())
    keylist = sorted(keylist)
    signMsg = ""
    for key in keylist:
        value = data[key]
        signMsg += (key + "=" + str(value) + "&")
    signMsg = signMsg[:-1]

    stringSignTemp = signMsg + "&key=" + privateKey

    sign = hashlib.md5(stringSignTemp.encode(encoding='utf-8')).hexdigest()
    return sign.upper()
