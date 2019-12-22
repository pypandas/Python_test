import requests
from bs4 import BeautifulSoup
from multiprocessing import Queue
from concurrent.futures import ThreadPoolExecutor

from data_mongo import ProxyMongo


class GetProxyIp:
    def __init__(self):
        self.get_proxy_url = 'https://www.xicidaili.com/nt/'
        self.testing_url = 'http://ip.tool.chinaz.com/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        }
        self.queue_list = Queue()
        self.xpath_ip_list = self.xpath_proxy_ip()
        self.pool = ThreadPoolExecutor(max_workers=20)
        while self.xpath_ip_list.qsize() > 0:
            self.test = self.pool.submit(self.testing_proxy_ip, self.xpath_ip_list.get())
        self.proxy_db = ProxyMongo()

    def get_proxy_ip(self, index=1):
        self.get_proxy_url = str(self.get_proxy_url) + str(index)
        proxy_response = requests.get(url=self.get_proxy_url, headers=self.headers)
        return proxy_response.text

    def xpath_proxy_ip(self):
        for i in range(1, 5):
            soup = BeautifulSoup(self.get_proxy_ip(i), 'html.parser')
            ip_tr = soup.findAll('tr')
            for i in range(1, len(ip_tr)):
                ip_td = ip_tr[i].findAll('td')
                proxy_temp = ip_td[5].contents[0].lower() + '://' + ip_td[1].contents[0] + ':' + ip_td[2].contents[0]
                self.queue_list.put(proxy_temp)
            return self.queue_list

    def testing_proxy_ip(self, proxy_ip):
        proxy_ip_json = {'http': proxy_ip}
        try:
            # 检测代理IP是否可用
            requests.get(url=self.testing_url, proxies=proxy_ip_json, timeout=5)
            # 将可用的代理IP转换成列表
            proxy_ip_list = {'proxy_ip': proxy_ip}
            # 存入mongodb
            self.proxy_db.db.col.insert(proxy_ip_list)
            return proxy_ip
        except Exception as e:
            pass
