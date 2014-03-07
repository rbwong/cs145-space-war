#!/usr/bin/python

from threading import Thread
from time import sleep
import sys, os
import socket
import datetime
import connection

host = ''
port = 8888
key = '70d9573de68a1fa96488b8fbfb9476c8'

"""
client_table schema {
	'key': addr

	'connection_layer': None
	'username': 'Anonymous'
	'status': None
	'thread': new_client	
}
"""

client_table = {}

#command/request queue
requests = []

def command_processor():
	while True:
		if requests:
			#raw message
			raw_requests = requests.pop(0)
			message = raw_requests[0]
			addr = raw_requests[1]
			
			#fetch user data
			username =  client_table[addr]['username']
			status = client_table[addr]['status']
			connection_layer = client_table[addr]['connection_layer']

			#parse message
			command, headers = parse_message(message)
			print 'DEBUG', command

			#process command
			if command == 'TIME':
				connection_layer.sendMessage("server: The date and time is " + str(datetime.datetime.now()))
			elif command == 'SET':
				args = parse_headers(headers)

				#set username
				if 'username' in args:
					client_table[addr]['username'] = args['username']
					connection_layer.sendMessage('New username is ' + args['username'])
				#set status
				elif 'status' in args:
					client_table[addr]['status'] = args['status']
					connection_layer.sendMessage('New status is ' + args['status'])
			elif command == 'QUIT ' + key:
				client_table[addr]['finalquit'] = True
				connection_layer.sendMessage('QUIT2 ' + key)
			else:
				connection_layer.sendMessage("I can't understand what you're saying")

def client(remote_socket, addr):
	connection_layer = connection.connection(remote_socket)
	connection_layer.sendMessage("Client connected!")

	#set connection_layer in 'db'
	client_table[addr]['connection_layer'] = connection_layer

	while True:
		message = connection_layer.getMessage()
		command, headers = parse_message(message)
		if command == ('QUIT3 ' + key) and client_table[addr]['finalquit']: 
			client_table[addr]['connection_layer'].disconnect()
			client_table.pop(addr, None)
			print str(addr), "disconnected"
			break
		requests.append((message, addr))

def accept_clients(s):
	while True:
		remote_socket, addr = s.accept()
		print str(addr) + 'connected'

		new_client = Thread(target = client, args = ((remote_socket, addr)))

		client_table[addr] = {'connection_layer': None,
						'username': 'Anonymous',
						'status': None,
						'thread': new_client}
		new_client.start()

def send(receipient=None):
	pass

def parse_message(message):
	raw = message.split('\r\n\n')
	print 'debug:', raw[0], raw[1]
	return raw[0], raw[1]

def parse_headers(headers):
	context = {}
	headers = headers.split('\r\n')

	#generate dictionary for headers
	for raw in headers:
		headings = raw.split(': ')
		context[headings[0]] = headings[1]

	return context

if __name__ == "__main__":
	s = socket.socket()
	s.bind((host, port))

	print "server ready..."

	s.listen(5)

	command_processor_thread = Thread(target = command_processor)
	client_connector_thread = Thread(target = accept_clients, args = (s,))

	command_processor_thread.start()
	client_connector_thread.start()
	
	while True:
		command = raw_input('command: ')
		if command == 'exit':
			s.close()
			os._exit(0)