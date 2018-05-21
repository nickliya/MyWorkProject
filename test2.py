# coding=utf-8
import itertools
import string


def createTree(inputstr, dictree):
    """对比集合列表得出a，b生成字典"""
    inputlist = inputstr.split(" ")
    newdictree = {}
    for x in dictree:
        a, b = 0, 0
        for i in range(4):
            if inputlist[i] == x[i]:
                a += 1
                continue
            if inputlist[i] in x:
                b += 1
                continue
        newdictree[x] = a, b
    return newdictree


def createList(dic, result):
    """集合字典里面生成有效集合列表"""
    numlist = []
    for k, v in dic.iteritems():
        if v == result:
            numlist.append(k)
    return numlist


def listvalueTostr(listindex):
    inputstr = listindex[0] + " " + listindex[1] + " " + listindex[2] + " " + listindex[3]
    return inputstr


# 第一部初始化列表
# numlist = itertools.permutations(string.digits, 4)
numlist = []
for i in itertools.permutations(string.digits, 4):
    if i[0] == "0":
        pass
    else:
        numlist.append(i)

input1 = "1 2 3 4"
dictree1 = createTree(input1, numlist)
numlist2 = createList(dictree1, (2, 0))
input2 = listvalueTostr(numlist2[0])

dictree2 = createTree(input2, numlist2)
numlist3 = createList(dictree1, (2, 2))

dictree2 = createTree()
