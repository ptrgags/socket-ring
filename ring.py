#!/usr/bin/env python
import sys
import socket

input_addr, output_addr, node_id, node_type = sys.argv[1:]
input_host, input_port = input_addr.split(':')
output_host, output_port = output_addr.split(':')

#blank hosts default to localhost
input_host = input_host if input_host else 'localhost'
output_host = output_host if output_host else 'localhost'

#Convert integer arguments
input_port = int(input_port)
output_port = int(output_port)
node_id = int(node_id)

#Make address tuples
input_addr = (input_host, input_port)
output_addr = (output_host, output_port)

def create_sockets():
    input_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    input_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    output_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    output_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return input_sock, output_sock

def listen_input(input_sock, input_addr):
    input_sock.bind(input_addr)
    input_sock.listen(1)
    print "Listening on host {} port {}".format(*input_addr)

def connect_output(output_sock, output_addr):
    output_sock.connect(output_addr)
    print "Connected to host {} port {}".format(*output_addr)

def accept_connection(input_sock):
    conn, client_addr = input_sock.accept()
    print "Accepted connection from {}".format(client_addr)
    return conn

def say_hi(output_sock, n_id):
    message = 'HI' + chr(n_id)
    print "Saying hi to the next node"
    output_sock.sendall(message)

def send_start(ouput_sock, n_id):
    message = 'ST' + chr(n_id)
    print "Telling the end node to being the ring!"
    ouput_sock.sendall(message)

def read_message(conn):
    msg = ''
    while not len(msg) == 3:
	msg += conn.recv(3)
    return (msg[:2], ord(msg[2]))

if node_type == 'end':
    in_socket, out_socket = create_sockets()
    listen_input(in_socket, input_addr)
    conn = accept_connection(in_socket)
    output_enabled = False
    while True:
	msg_type, n_id = read_message(conn)
	if msg_type == 'HI':
	    if n_id == node_id:
		print "Hi returned to sender!"
	    else: 
		print "Node {} says hi!".format(n_id)
		if output_enabled:
		    say_hi(out_socket, n_id)
	elif msg_type == 'ST':
	    print "Node {} is telling me to create a ring!".format(n_id)
	    connect_output(out_socket, output_addr)
	    say_hi(out_socket, node_id)
elif node_type == 'reg':
    in_socket, out_socket = create_sockets()
    listen_input(in_socket, input_addr)
    connect_output(out_socket, output_addr)
    say_hi(out_socket, node_id)
    conn = accept_connection(in_socket)
    while True:
	msg_type, n_id = read_message(conn)
	if msg_type == 'HI':
	    if n_id == node_id:
		print "Hi returned to sender!"
	    else:
		print "Node {} says hi!".format(n_id)
		say_hi(out_socket, n_id)
	elif msg_type == 'ST':
	    send_start(out_socket, n_id)
elif node_type == 'start':
    in_socket, out_socket = create_sockets()
    listen_input(in_socket, input_addr)
    connect_output(out_socket, output_addr)
    say_hi(out_socket, node_id)
    send_start(out_socket, node_id)
    conn = accept_connection(in_socket)
    while True:
	msg_type, n_id = read_message(conn)
	if msg_type == 'HI':
	    if n_id == node_id:
		print "Hi returned to sender!"
	    else:
		print "Node {} says hi!".format(n_id)
		say_hi(out_socket, n_id)
