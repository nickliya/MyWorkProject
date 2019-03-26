# coding=utf-8
"""python2 RSA签名"""

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256, SHA
import base64


def RSA_signWithSHA256(data, rsakey):
    keylist = data.keys()
    keylist.sort()
    signMsg = ""
    for key in keylist:
        value = data[key]
        if type(value) == unicode:
            signMsg += (key + "=" + value + "&")
        else:
            signMsg += (key + "=" + str(value) + "&")

    privateKey = rsakey

    try:
        private_keyBytes = base64.b64decode(privateKey)
        priKey = RSA.importKey(private_keyBytes)
        signer = PKCS1_v1_5.new(priKey)
    except Exception as msg:
        return "传入的私钥不合法"
    signMsg = signMsg[:-1]
    h = SHA256.new(signMsg.encode("utf-8"))
    signature = signer.sign(h)
    signatureBase64 = base64.b64encode(signature)
    return signatureBase64


def RSA_signWithSHA(data, rsakey):
    keylist = data.keys()
    keylist.sort()
    signMsg = ""
    for key in keylist:
        value = data[key]
        if type(value) == unicode:
            signMsg += (key + "=" + value + "&")
        else:
            signMsg += (key + "=" + str(value) + "&")

    privateKey = rsakey

    try:
        private_keyBytes = base64.b64decode(privateKey)
        priKey = RSA.importKey(private_keyBytes)
        signer = PKCS1_v1_5.new(priKey)
    except Exception as msg:
        return "传入的私钥不合法"
    signMsg = signMsg[:-1]
    # signMsg = signMsg.encode("utf-8")
    h = SHA.new(signMsg.encode("utf-8"))
    signature = signer.sign(h)
    signatureBase64 = base64.b64encode(signature)
    return signatureBase64
