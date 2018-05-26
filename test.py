#!/usr/bin/env python
# coding=utf-8
# author:401219180

import base64
import itertools
import string

# flag = flag.flag
# sands = int(flag[5:-1].encode("hex"), 16)

flag = ""

holes = [257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373]
# holes = [263, 277, 293, 311]
print len(holes)
# with open("sand.txt", "w") as f:
#     for i in range(len(holes)):
#         sand = sands % holes[i]
#         f.write(str(sand)+"\n")


file1 = open("C:\\Users\\fuzhi\\Desktop\\SUCTF\\MISC\\sandgame\\sand.txt", "r")
data = file1.read()
datalist = data.split("\n")


# datalist = ["203", "203", "82", "82"]


def getglist(a, b, c, d):
    list1 = []
    list2 = []
    for i in range(1000):
        list1.append(a * i + c)
        list2.append(b * i + d)
        # glist = list(set(list1) & set(list2))
        # if glist != []:
        #     break
    glist = list(set(list1) & set(list2))
    yu = min(glist)
    chushu = a * b
    return [chushu, yu]


i = 0
while 1:
    print getglist(holes[i], holes[i + 1], int(datalist[i]), int(datalist[i+1]))
    i += 2
    if i == 22:
        break
