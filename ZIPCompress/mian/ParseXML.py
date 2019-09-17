import xml.sax


class MovieHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "gameitem":
            gid = attributes["id"]
            serverid = attributes["serverid"]
            status = attributes["status"]
            gamelist = {"gid": gid, "serverid": serverid, "status": status}
            print(gamelist)


if __name__ == "__main__":
    # 创建XMLReader
    parser = xml.sax.make_parser()

    # 关闭命名空间
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写ContextHandler
    Handler = MovieHandler()
    parser.setContentHandler(Handler)

    # 读取xml文件
    parser.parse("../res/roomconfig_hot.xml")
