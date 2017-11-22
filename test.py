# -*- coding:utf-8 -*-

import requests

header = {"user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36"}
payload = {
    "action": "parse",
    "prop": "text|images|links|externallinks|wikitext",
    "page": "料理次元",
    "format": "json"
}
r = requests.get("https://zh.moegirl.org/api.php", params=payload, headers=header)
htmlData = r.json()
print htmlData