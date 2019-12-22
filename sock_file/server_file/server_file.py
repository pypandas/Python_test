import logging
import os
import socketserver
import struct
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s', filename='./server.log', filemode='a')


class FileRequestHandler(socketserver.BaseRequestHandler):
    """
    继承BaseRequestHandler类，重构handler函数
    唯一需要实现的方法其实只有FileRequestHandler.handler()
    handler()之外的方法只为打印日志信息
    """

    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('FileRequestHandler')
        self.logger.debug('__init__')
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def setup(self):
        self.logger.debug('setup')
        return socketserver.BaseRequestHandler.setup(self)

    def handle(self):
        self.logger.debug('connected from: %s' % str(self.client_address))
        while True:
            # 定义文件信息: 128sl表示文件名为128bytes长, l表示一个int或log文件类型, 在此为文件大小
            file_info = struct.calcsize('128sl')
            buf = self.request.recv(file_info)
            if buf:
                # 根据128sl解包文件信息, 与socket_client_file.py的打包规则相同
                file_name, file_size = struct.unpack('128sl', buf)
                # 解码
                file_name = str(bytes(file_name).decode('utf-8')).strip('\00')
                self.logger.debug(
                    'file_name=%s, file_size=%d, time=%s' % (file_name, file_size, str(datetime.now()).split('.')[0]))
                recv_size = 0
                file = open(file_name, 'wb')
                while not recv_size == file_size:
                    if file_size - recv_size > 1024:
                        r_data = self.request.recv(1024)
                        recv_size += len(r_data)
                    else:
                        r_data = self.request.recv(file_size - recv_size)
                        recv_size = file_size
                    file.write(r_data)
                file.close()

                # 验证文件大小
                if file_size == os.stat(file_name).st_size:
                    self.request.send(str(file_name).encode('utf-8'))

    def finish(self):
        self.logger.debug('finish')
        return socketserver.BaseRequestHandler.finish(self)


if __name__ == '__main__':
    instance = socketserver.ThreadingTCPServer(('127.0.0.1', 1801), FileRequestHandler)
    instance.serve_forever()
