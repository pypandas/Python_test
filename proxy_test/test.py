import json
from urllib.parse import *
import socketserver

import requests


def request(url):
    url_str = 'http://dx.blm.ymffw.cn/dwz.php?longurl=' + str(url)
    response = requests.get(url=url_str)

    return json.loads(response.text)['longurl']


if __name__ == '__main__':
    url_s = 'https://emw06.com/pop_4/index.html?ruid=0&agentid=108'
    url_qp = quote_plus(url_s)
    print(request(url_qp))
