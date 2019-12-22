import pymongo


class ProxyMongo:
    def __init__(self):
        self.conn = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.conn.db_proxy
