# coding=utf-8
# /usr/bin/python
# coding=utf-8
# create by 15025463191 2017/10/11


def getcode(strindex):
    number = 0
    for i in strindex:
        number += ord(i)
    hexnumber = hex(number)[-2:]
    code = "lin bus tx *"+hexnumber+"#"+strindex
    return code

codeindex = raw_input("please input your code:")
print getcode(codeindex)
