# -*- coding: utf-8 -*-
import os
import socket
import struct
import sys


def find_up_file():
    file_list = []
    file_path = os.listdir('./')
    for file in file_path:
        if os.path.isdir(file):
            continue
        elif str(file).split('.')[-1] == 'py':
            continue
        else:
            file_list.append(file)
    return file_list


def client_up_file(client_file_address):
    client_file = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_file.connect(client_file_address)

    for up_file in find_up_file():
        if os.path.isfile(up_file):
            file_info = struct.calcsize('128sl')  # 定义打包规则
            # 定义文件头信息，包含文件名和文件大小
            file_header = struct.pack('128sl', bytes(os.path.basename(up_file).encode('utf-8')),
                                      os.stat(up_file).st_size)
            client_file.send(file_header)
            # with open(filepath,'rb') as fo: 这样发送文件有问题，发送完成后还会发一些东西过去
            f = open(up_file, 'rb')
            file_len = 0
            while True:
                data = f.read(1024)
                # 进度条
                file_len += len(data)
                hashes = '#' * int(file_len / os.stat(up_file).st_size * 50)
                spaces = ' ' * (50 - len(hashes))
                sys.stdout.write("\rPercent: [%s] %d%%" % (hashes + spaces, len(hashes) * 2))
                sys.stdout.flush()
                if not data:
                    break
                client_file.send(data)
            f.close()
            msg = client_file.recv(1024)
            print(bytes(msg).decode('utf-8'))
    client_file.close()


def send_shell(client_shell_address, comm):
    ss = ''
    for file_shell in find_up_file():
        ss += ' ' + file_shell

    # print(ss)
    # 建立socket连接
    client_shell = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_shell.connect(client_shell_address)

    send_str = 'sh builds.sh ' + comm
    file_info = struct.calcsize('128sl')  # 定义打包规则
    # 定义文件头信息，包含文件名和文件大小
    shell_header = struct.pack('128sl', send_str.encode('utf-8'), len(send_str))
    client_shell.send(shell_header)
    len_recv = client_shell.recv(1024)
    print(len_recv)
    run_len = int(len_recv.decode('utf-8'))
    recv_data = bytes()
    while len(recv_data) != run_len:
        data = client_shell.recv(1024)
        recv_data += data
    run_result = recv_data.decode('utf-8')
    print(run_result)


if __name__ == '__main__':
    # 连接地址
    update_file = ('47.91.219.204', 1801)
    send_msg = ('47.91.219.204', 1802)
    client_up_file(update_file)
    up_file_name = input('输入需要更新的文件名称(不输入为更新所有):')
    send_shell(send_msg, up_file_name)
