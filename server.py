#!/usr/bin/python

from threading import Thread
from time import sleep
from random import random

import sys, os
import socket
import datetime
import connection

host = ''
port = 5679
key = '70d9573de68a1fa96488b8fbfb9476c8'

"""
client_table schema {
	'key': client_id

	'addr': addr,
	'connection_layer': None
	'team': blue/red
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
			client_id = raw_requests[1]
			
			#fetch user data
			username =  client_table[client_id]['username']
			status = client_table[client_id]['status']
			connection_layer = client_table[client_id]['connection_layer']

			#parse message
			command, headers = parse_message(message)
			print 'debug', command

			#process command
			if command == 'TIME':
				connection_layer.sendMessage("server: The date and time is " + str(datetime.datetime.now()))
			elif command == 'SET':
				args = parse_headers(headers)

				#set username
				if 'username' in args:
					set_username(client_id, args['username'])
					connection_layer.sendMessage('server: New username is ' + args['username'])
				#set status
				elif 'status' in args:
					set_status(client_id, args['status'])
					connection_layer.sendMessage('server: New status is ' + args['status'])
				#send message
				elif 'message' in args:
					send(receipient=int(args['receipient']), sender=client_id, message=args['message'])
				#key events
				elif 'key' in args:
					send_key(sender=client_id, args=args)
				#mouse events
				elif 'mouse' in args:
					send_key(sender=client_id, args=args)
			elif command == 'GET':
				args = parse_headers(headers)

				#get user
				if 'user' in args:
					get_user(client_id, args['user'])
			elif command == 'QUIT ' + key:
				client_table[client_id]['finalquit'] = True
				connection_layer.sendMessage('QUIT2: ' + key)
			else:
				connection_layer.sendMessage("I can't understand what you're saying")

def client(remote_socket, client_id):
	connection_layer = connection.connection(remote_socket)
	connection_layer.sendMessage("assign: " + client_table[client_id]["team"])

	#set connection_layer in 'db'
	client_table[client_id]['connection_layer'] = connection_layer

	while True:
		message = connection_layer.getMessage()
		command, headers = parse_message(message)
		if command == ('QUIT3 ' + key) and client_table[client_id]['finalquit']: 
			client_table[client_id]['connection_layer'].disconnect()
			client_table.pop(client_id, None)
			print "client", str(client_id), "disconnected"
			break
		requests.append((message, client_id))

def accept_clients(s):
	id_counter = 69 #should be random
	while True:
		remote_socket, addr = s.accept()
		print str(addr) + 'connected'

		new_client = Thread(target = client, args = ((remote_socket, id_counter)))

		team = 'Blue' if id_counter == 69 else 'Red'
		client_table[id_counter] = {
						'addr': addr,
						'connection_layer': None,
						'team': team,
						'username': 'Anonymous',
						'status': '',
						'thread': new_client
						}
		new_client.start()
		id_counter += 1
		if id_counter == 71:
			break

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

#GET COMMANDS
def get_user(client_id, username):
	if username == 'all':
		for key in client_table.keys():
			format_message  = 'id: ' + str(key) + ' username: ' + str(client_table[key]['username']) + ' status: ' + str(client_table[key]['status'] + '\n')
			client_table[client_id]['connection_layer'].sendMessage(format_message)
	else:
		pass

#SET COMMANDS
def set_username(client_id, username):
	client_table[client_id]['username'] = username

def set_status(client_id, status):
	client_table[client_id]['status'] = status

def send(receipient=None, sender=None, message=''):
	if receipient and receipient != 0:
		client_table[receipient]['connection_layer'].sendMessage(client_table[sender]['username'] + '(' + client_table[sender]['team'] + ')' + ': ' + message)
	elif receipient == 0:
		for key in client_table.keys():
			client_table[key]['connection_layer'].sendMessage(client_table[sender]['username'] + '(' + client_table[sender]['team'] + ')' + ': ' + message)
	else:
		print "debug: Send - no target"

#Player actions
def send_key(sender=None, args=''):
	hit = random()
	if 'key' in args:
		for key in client_table.keys():
				if args['key'] == "32": #if attack
					client_table[key]['connection_layer'].sendMessage('team: ' + client_table[sender]['team'] + '\r\n' + 'key: ' + args['key'] + '\r\n' + 'hit-rate: ' + str(hit))
				else: 
					client_table[key]['connection_layer'].sendMessage('team: ' + client_table[sender]['team'] + '\r\n' + 'key: ' + args['key'])
	if 'mouse' in args:
		for key in client_table.keys():
				client_table[key]['connection_layer'].sendMessage('team: ' + client_table[sender]['team'] + '\r\n' + 'key: ' + args['mouse']  + '\r\n' + 'x: ' + args['x'] + '\r\n' + 'y: ' + args['y'])

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