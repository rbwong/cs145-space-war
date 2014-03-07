#!/usr/bin/python

import socket
import connection
from threading import Thread

host = 'localhost'
port =  8888
key = '70d9573de68a1fa96488b8fbfb9476c8'

finalquit = False

def receive_message(connection_layer):
	while True:
		recv_msg = connection_layer.getMessage()
		if recv_msg == ('QUIT2 ' + key):
			connection_layer.sendMessage('QUIT3 ' + key + '\r\n\ndate: january')
			connection_layer.disconnect()
			break
		else:
			finalquit = False
		print recv_msg


if __name__ == '__main__':
	s = socket.socket()

	s.connect((host, port))

	connection_layer = connection.connection(s)

	print "Client tries to connect to server..."

	#start receiver thread
	receiver_thread = Thread(target=receive_message, args=(connection_layer,))
	receiver_thread.start()

	while True:
		send_msg = raw_input('')
		send_msg = send_msg.split(' ')

		if send_msg[0] == 'QUIT':
			connection_layer.sendMessage('QUIT ' + key + '\r\n\ndate: january')
			finalquit = True
			break
		elif send_msg[0] == 'TIME':
			connection_layer.sendMessage('TIME\r\n\ndate: january')

		elif send_msg[0] == 'SETUSERNAME':
			connection_layer.sendMessage('SET\r\n\nusername: ' + send_msg[1])
		elif send_msg[0] == 'SETSTATUS':
			connection_layer.sendMessage('SET\r\n\nstatus: ' + send_msg[1])
		else:
			print send_msg[0] + ": command not recognized"