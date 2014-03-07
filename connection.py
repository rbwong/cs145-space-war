class _myConnection:

	def __init__(self,s):
		self.s = s

	def sendMessage(self,msg):
		byte = self.s.send(msg)
		if byte == 0:
			return False
		else:
			return True

	def getMessage(self):
		return self.s.recv(1024)

	def disconnect(self):
		self.s.close()

def connection(s):
	myConnectionObj = _myConnection(s)
	return myConnectionObj
