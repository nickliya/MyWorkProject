# coding=utf-8
# create by 401219180 2018/02/10

import pymssql
import time
import datetime


class Bianlifunction:
    """个人便利方法集合"""

    @staticmethod
    def time_sfm():
        """
        范围本地时间时分秒
        :return:
        """
        now_stamp = time.time()
        local_time = datetime.datetime.fromtimestamp(now_stamp)
        return local_time.strftime("%H:%M:%S.%f")

    @staticmethod
    def time_nyrsfm():
        """
        返回本地时间年月日时分秒
        :return:
        """
        now_stamp = time.time()
        local_time = datetime.datetime.fromtimestamp(now_stamp)
        return local_time.strftime("%Y%m%d%H%M%S")[2:]

    @staticmethod
    def BSJhextime():
        """
        范围本地时间十六进制
        :return: 示例'13 03 04 06 20 12 '
        """
        now_stamp = time.time()
        local_time = datetime.datetime.fromtimestamp(now_stamp)

        def local2utc(local_st):
            time_struct = time.mktime(local_st.timetuple())
            utc_st = datetime.datetime.utcfromtimestamp(time_struct)
            return utc_st

        data = local2utc(local_time).strftime("%Y %m %d %H %M %S")
        str1 = ''
        str2 = ''
        data = data[2:]
        while data:
            str1 = data[0:2]
            if len(hex(int(str1))[2:4]) == 1:
                head = "0" + hex(int(str1))[2:4]
            else:
                head = hex(int(str1))[2:4]
            str2 += head + " "
            data = data[3:]
        return str2

    @staticmethod
    def hextime():
        """
        范围本地时间十六进制前三分钟
        :return: 示例'13,3,4,6,1b,12'
        """
        now_stamp = time.time()
        local_time = datetime.datetime.fromtimestamp(now_stamp)

        def local2utc(local_st):
            time_struct = time.mktime(local_st.timetuple())
            utc_st = datetime.datetime.utcfromtimestamp(time_struct)
            return utc_st

        utc_tran = local2utc(local_time)
        # nowtime = utc_tran.strftime('%Y%m%d%H%M%S')
        year = utc_tran.strftime('%Y')
        month = utc_tran.strftime('%m')
        day = utc_tran.strftime('%d')
        hour = utc_tran.strftime('%H')
        minute = utc_tran.strftime('%M')
        newminute = int(minute) - 3
        second = utc_tran.strftime('%S')

        if newminute < 0:
            newminute = newminute + 60
            hour = int(hour) - 1
            if hour < 0:
                hour = hour + 24
                day = int(day) - 1
        else:
            pass

        Y = '%x' % int(year[-2:])
        m = '%x' % int(month)
        d = '%x' % int(day)
        H = '%x' % int(hour)
        M = '%x' % newminute
        Sec = '%x' % int(second)
        strhextime = str(Y) + ',' + str(m) + ',' + str(d) + ',' + str(H) + ',' + str(M) + ',' + str(Sec)
        return strhextime


class CRCUtil:
    """思锐CRC解密算法"""

    def __init__(self):
        self.cycleCodes = ['G', 'H', 'I', 'J', '&', '<', '2', '8', 'd', '#', 'N', 'i', 'X', 's', '=', '5', 'R', '0',
                           '$', 'e', '4', 'Q', '%', '[', 'j', 'p', ']', 'c', '1', '3', '7', '9', 'A', '6', 'n', 'z',
                           'B', ';', 'h', 'r', ':', 'a', '_', 'O', '{', 'D', 'E', 'm', 'W', 'Y', 'k', '}', 'x', 'Z',
                           'P', 'u', ',', 'F', 'M', 'g', 'C', 'K', 'f', 't', '+', '>', 'L', 'S', 'T', 'U', 'V', 'q',
                           '|', 'w', 'l', 'y', 'b', 'o', 'v', '.']
        self.cycleIndex = []
        self.OTUMsgEncryptor()

    def OTUMsgEncryptor(self):
        for i in range(128):
            self.cycleIndex.append(-1)
        index = 0
        for i in range(len(self.cycleCodes)):
            self.cycleIndex[ord(self.cycleCodes[index])] = index
            index += 1

    def asiccCrcDecode(self, context, offset):
        index = 0
        plaintext = ""
        for i in range(len(context)):
            value = ord(context[index])
            if self.cycleIndex[value] >= 0:
                nextIndex = (self.cycleIndex[value] - index - offset) % len(self.cycleCodes)
                nextIndex = (len(self.cycleCodes) + nextIndex) % len(self.cycleCodes)
                plaintext += self.cycleCodes[nextIndex]
            index += 1
        print(plaintext)
        return plaintext


class Sqlfunticon:
    """sql方法"""

    @staticmethod
    def getinfo(sql):
        """sqlserver"""
        conn = pymssql.connect(host='192.168.6.51', user='sa', password='test2017')
        cur = conn.cursor()
        cur.execute(sql)
        info = cur.fetchall()
        cur.close()
        conn.close()
        return info
