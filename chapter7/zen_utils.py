#!/usr/bin/env python3
import argparse, time, socket

aphorisms = {b'Beautiful is better than?': b'Ugly.',
			 b'Explicit is better than?': b'Implicit.',
			 b'Simple is better than?': b'Complex.'}

def get_answer(aphorism):
	"""Return the correct answer to a given Zen-of-Python aphorism."""
	time.sleep(0.0)	#having fun with the time module
	return aphorisms.get(aphorism, b'Error: unknown aphorism.')

def parse_commnad_line(description):
	"""Parse a command line and return a socket address."""
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('host', help='IP or hostname')
	parser.add_argument('-p', metavar='port', type=int, default=1060,
						help='TCP port number (default %(default)s)')
	args = parser.parse_args()
	address = (args.host, args.p)
	return address

def create_srv_socket(address):
	"""Build and return a listening server socket."""
	listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	listener.bind(address)
	listener.listen(64)
	print('Listening at {}'.format(address))
	return listener

def accept_connections(listener):
	"""On an infinite loop, answer incoming connections on a listening 
	socket."""
	while True:
		sock, address = listener.accept()
		print('Accepted connection from {}'.format(address))
		handle_conversation(sock, address)

def handle_conversation(sock, address):
	"""Converse with client until they are done talking."""
	try:
		while True:
			handle_request(sock)
	except EOFError:
		print('Client socket to {} has closed'.format(address))
	except Exception as e:
		print('Client {} error: {}'.format(address, e))
	finally:
		sock.close()

def handle_request(sock):
	"""Receive a single client request on `sock` and send the answer."""
	aphorism = recv_until(sock, b'?')
	answer = get_answer(aphorism)
	sock.sendall(answer)

def recv_until(sock, suffix):
	"""Receive bytes over socket `sock` until we receive the suffix."""
	message = sock.recv(4096)
	if not message:
		raise EOFError('socket closed')
	while not message.endswith(suffix):
		data = sock.recv(4096)
		if not data:
			raise IOError('received {!r} then socket closed'.format(message))
		message += data
	return message