# /usr/bin/python
# coding=utf-8

import string
import random


def getvin():
        digipercase = string.digits + string.uppercase  # 数字大写字母集合
        digiper1 = digipercase.replace('I', '')  # 去大写I
        digiper2 = digiper1.replace('O', '')  # 去大写O
        digiper3 = digiper2.replace('Q', '')  # 去大写Q
        digiper4 = digiper3.replace('Z', '')  # 去大写Z
        VIN_number = ''.join(random.choice(digiper4) for i in range(8)) + random.choice(string.digits) + random.choice(
            string.digits) + ''.join(random.choice(digiper4) for i in range(3)) + ''.join(
            random.choice(string.digits) for i in range(4))
        hs = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
              'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
              'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'P': 7, 'R': 9,
              'S': 2, 'T': 3, 'U': 4, 'V': 5, 'W': 6, 'X': 7, 'Y': 8, }
        VIN = (hs[VIN_number[0]] * 8 + hs[VIN_number[1]] * 7 + hs[VIN_number[2]] * 6 + hs[VIN_number[3]] * 5 + hs[
            VIN_number[4]] * 4 + hs[VIN_number[5]] * 3 + hs[VIN_number[6]] * 2 + hs[VIN_number[7]] * 10 + hs[
                   VIN_number[9]] * 9 + hs[VIN_number[10]] * 8 + hs[VIN_number[11]] * 7 + hs[VIN_number[12]] * 6 + hs[
                   VIN_number[13]] * 5 + hs[VIN_number[14]] * 4 + hs[VIN_number[15]] * 3 + hs[VIN_number[16]] * 2) % 11
        if VIN == 10:
            VIN = 'X'
        else:
            pass
        TrueVIN = VIN_number[:8] + str(VIN) + VIN_number[9:]
        # print (str(VIN) + ':' + str(TrueVIN))
        return str(TrueVIN)


print getvin()
