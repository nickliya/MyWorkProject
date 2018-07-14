#!/usr/bin/env python
# coding=utf-8
# author:401219180

import base64
import itertools
import string
import requests
import random
from datetime import date
from datetime import timedelta
import base64
import hashlib
import binascii
from CTF import privateFun

# b = base64.b32decode("gq=")
# print(b)

# cpdic = {
#     "a": "d", "d": "e", "g": "f", "q": "r", "h": "o", "b": "m", "u": "b", "r": "a", "t": "s", "p": "i", "k": "p",
#     "w": "t", "z": "u", "e": "n", "x": "c", "y": "l", "l": "y", "f": "w", "m": "h", "j": "g", "i": "x", "v": "k"
# }
#
# f1 = open("C:\\Users\\fuzhi\\Desktop\\Downloads\\encryption.encrypted", "r")
# data1 = f1.read()
# listdata1 = list(data1)
# i = 0
# for strindex in listdata1:
#     if strindex in cpdic:
#         listdata1[i] = cpdic[strindex]
#     i += 1
#
# s = "".join(listdata1)
# print s


def num_to_bytes(n):
    b = hex(n)[2:-1]
    if len(b) % 2 == 1:
        b = '0' + b
    else:
        b = b
    return b


def num_to_bytes2(n):
    b = hex(n)[2:-1]
    b = '0' + b if len(b)%2 == 1 else b
    return b

print(num_to_bytes(123555))
print(num_to_bytes2(123555))