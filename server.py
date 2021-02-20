# Code for multi-threaded server
# Python 3
# Usage: python3 server.py server_port admin_passwd
# Coding: utf-8

from sys import argv
from time import sleep
from server_helper import *
from threading import Thread, Condition
from json.decoder import JSONDecodeError
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


def receive_handler():
    '''
    - Handle all client connections and make a new thread for each
    '''
    global t_lock
    global server_socket
    print('Waiting for clients...')

    while True:
        connection, _ = server_socket.accept()
        thread = Thread(
            target=handle_client, args=(connection, ))
        thread.daemon = True
        thread.start()


def handle_client(connection):
    '''
    - loop infinitely and receive client commands
    '''
    global force_shutdown
    while True:
        try:
            data = loads(connection.recv(1024).decode())
        except JSONDecodeError:
            break

        if not data:
            break

        with t_lock:
            if data['command'] == 'LOG':
                print('Client connected')
            elif data['command'] == 'USER':
                username(connection, data)
            elif data['command'] == 'PASS':
                password(connection, data)
            elif data['command'] == 'CRT':
                create_thread(connection, data)
            elif data['command'] == 'MSG':
                post_message(connection, data)
            elif data['command'] == 'DLT':
                delete_message(connection, data)
            elif data['command'] == 'EDT':
                edit_message(connection, data)
            elif data['command'] == 'LST':
                list_threads(connection, data)
            elif data['command'] == 'RDT':
                read_thread(connection, data)
            elif data['command'] == 'UPD':
                upload_file(connection, data)
            elif data['command'] == 'DWN':
                download_file(connection, data)
            elif data['command'] == 'RMV':
                remove_thread(connection, data)
            elif data['command'] == 'XIT':
                client_exit(connection, data)
                break
            elif data['command'] == 'SHT':
                force_shutdown = shutdown(connection, data, admin_passwd)

            t_lock.notify()


# setting up all environment variables
if (len(argv) < 2):
    print('Please provide a server port (admin password is optional).')
    exit()
elif (len(argv) == 2):
    server_port = int(argv[1])
    admin_passwd = None
else:
    server_port = int(argv[1])
    admin_passwd = argv[2]

t_lock = Condition()
server_address = ('localhost', server_port)
force_shutdown = False
unpack_credentials()

# setting up server with given
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen()

# setting up thread to receive clients
receive_thread = Thread(target=receive_handler)
receive_thread.daemon = True
receive_thread.start()

# sleep the main thread unless a shutdown has been forced
while not force_shutdown:
    sleep(0.1)
