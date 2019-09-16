import socket


target_host = "127.0.10.1"
target_port = 80


# 建立socket对象
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# 发送数据
client.sendto(b"AAABBBCCC", (target_host, target_port))


# 接收数据
data, addr = client.recvfrom(4096)


print(data)


client.colse()