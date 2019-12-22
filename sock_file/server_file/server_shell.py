import logging
import socketserver
import struct
from datetime import datetime
import subprocess

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s', filename='./server.log', filemode='a')


class ShellRequestHandler(socketserver.BaseRequestHandler):
    """
    继承BaseRequestHandler类，重构handler函数
    唯一需要实现的方法其实只有FileRequestHandler.handler()
    handler()之外的方法只为打印日志信息
    """

    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('ShellRequestHandler')
        self.logger.debug('__init__')
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def handle(self):
        self.logger.debug('connected from: %s' % str(self.client_address))
        while True:
            # 定义文件信息: 128sl表示文件名为128bytes长, l表示一个int或log文件类型, 在此为文件大小
            shell_info = struct.calcsize('128sl')
            buf = self.request.recv(shell_info)
            if buf:
                # 根据128sl解包文件信息, 与socket_client_file.py的打包规则相同
                shell_str, file_size = struct.unpack('128sl', buf)
                # 解码
                shell_str = str(bytes(shell_str).decode('utf-8')).strip('\00')
                # print(shell_str)
                self.logger.debug(
                    'shell_str=%s, file_size=%d, time=%s' % (shell_str, file_size, str(datetime.now()).split('.')[0]))
                command_obj = subprocess.Popen(shell_str, shell=True, stdout=subprocess.PIPE)
                run_result = command_obj.stdout.read()
                run_result_len = len(run_result)
                self.request.send(str(run_result_len).encode('utf-8'))
                self.request.send(run_result)


if __name__ == '__main__':
    instance = socketserver.ThreadingTCPServer(('127.0.0.1', 1802), ShellRequestHandler)
    instance.serve_forever()
