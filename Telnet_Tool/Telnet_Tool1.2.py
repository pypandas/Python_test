import socket
import sys


def get_ip_status(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect((ip, port))
        print('{0}:{1} open'.format(ip, port))
    except Exception:
        print('{0}:{1} close'.format(ip, port))
    finally:
        server.close()


if __name__ == '__main__':
    try:
        hosts = sys.argv[1]
        port = sys.argv[2]
        get_ip_status(hosts, int(port))
    except IndexError:
        print('expect: python filename.py 127.0.0.1 80', '\n', sys.exc_info())
