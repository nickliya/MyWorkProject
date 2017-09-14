# coding=utf-8
# create by 15025463191 2017/07/12

import requests

s = requests.Session()


def sethost(x):
    global host
    host = x


def req_get(url, payload):
    r = s.get(url, params=payload)
    return r.json()


def req_post(url, payload):
    r = s.post(url, data=payload)
    return r.json()


class Yqtest:
    def __init__(self):
        pass

    def setname(self, name):
        self.priname = name

    def greet(self):
        print "Hello, world! I'm "

    def zh(self):
        self.setname('yangqing')
        self.greet()

