# -*- coding:utf8 -*-
import os
import requests
import urllib
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
}

mainUrl = "https://zh.moegirl.org/舰队Collection/图鉴/舰娘"
mainResponse = requests.get(mainUrl)
htmlInfo = mainResponse.content

print htmlInfo

# name_re = r'style=";;">(.*?)<.*?display: table-row;'
# name_re = r'padding:0em 0.25em.*?title="舰队Collection:(.*?)">.*?</a>'
name_re = r'href=".*?" title="艦隊Collection:(.*?)">No.\d\d\d .*?</a>'
nameLisi = re.findall(name_re, htmlInfo)
print len(nameLisi)
for i in nameLisi:
    print i

def downloadMp3():
    mainUrl = "https://zh.moegirl.org/%E8%88%B0%E9%98%9FCollection:%E9%99%86%E5%A5%A5"
    mainResponse = requests.get(mainUrl)
    htmlInfo = mainResponse.content

    mp3url_re = r'data-filesrc="(.*?.mp3)"'
    mp3urlList = re.findall(mp3url_re, htmlInfo)
    print len(mp3urlList)
    for mp3url in mp3urlList:
        print "正在请求"+mp3url
        mp3Response = requests.get(mp3url, headers=headers)
        name = mp3url.split("/")[-1]
        f = open("luao/"+name, "wb")
        f.write(mp3Response.content)
        f.close()


