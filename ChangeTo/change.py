# coding=utf-8
# /usr/bin/python
# coding=utf-8
# create by 15025463191 2017/10/30
# -*- coding: utf-8 -*

from random import seed, randint

def strtoAscii(strindex):
    """字符串转16进制"""
    hexlist = []
    for i in strindex:
        number = ord(i)
        hexnumber = hex(number)
        # print hexnumber
        hexlist.append(number)
    return hexlist

# def stringXOR(stringlist):
#     """XOR校验"""
#     number = 0x00
#     for i in stringlist:
#         number ^= i
#     hexxor = hex(number)
#     hexxorlist = ["0x00", hexxor]
#     return hexxorlist
#
#
# a="adsa"
#
# print stringXOR(a)
