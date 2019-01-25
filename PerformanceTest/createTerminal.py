# coding=utf-8
from PIL import Image

import requests
import json

url = 'http://192.168.6.52:8000/creatGXCgo'
payload = {
    'carshareip': '192.168.6.221:30011',
    'carshareuser': 'admin',
    'carsharepasswd': 'Admin@fastgo123',
    'levelcode': '1/10/',
    'count': '250',
}
r = requests.get(url, payload)
f = open("C:\\Users\\fuzhi\\Desktop\\aotuTerminal_v1.1.txt", "ab+")

jsondata = json.loads(r.text)
for i in jsondata["data"]:
    writeinfo = i["platenumber"] + "," + i["IMEI"] + "," + i["vin"] + "\n"
    print(writeinfo)
    f.write(writeinfo.encode('UTF-8'))

f.close()
