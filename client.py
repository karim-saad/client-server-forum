# Code for client contacting multi-threaded server
# Python 3
# Usage: python3 server_IP server_port
# Coding: utf-8

from sys import argv
from client_helper import *
from json.decoder import JSONDecodeError
from socket import socket, AF_INET, SOCK_STREAM


# setting up all environment variables
if (len(argv) < 3):
    print('Please provide a server name and port number.')
    exit()

server_IP = argv[1]
server_port = int(argv[2])
server_address = (server_IP, server_port)

# connecting the client to the existing server socket
client_socket = socket(AF_INET, SOCK_STREAM)
try:
    client_socket.connect(server_address)
except ConnectionRefusedError:
    print(f'There is no server started on port number {server_port}')
    exit()

# send client connection message to server
client_connection(client_socket)

# prompt user to input username and password
username = credentials(client_socket)

# loop infinitely and prompt client for commands
while True:
    info_input = input(
        'Enter one of the following commands: CRT, MSG, DLT, EDT, LST, RDT, UPD, DWN, RMV, XIT, SHT: ').split()

    if info_input[0] == 'CRT' or info_input[0] == 'crt':
        if len(info_input) != 2:
            print('Incorrect syntax for CRT')
            continue

        # load all appropriate data to send to server
        info = {
            'command': 'CRT',
            'thread_title': info_input[1],
            'username': username
        }

        # try-except block to ensure server is still running
        try:
            create_thread(client_socket, info)
        except JSONDecodeError:
            print('Server was shut down')
            exit()
    elif info_input[0] == 'MSG' or info_input[0] == 'msg':
        if len(info_input) < 3:
            print('Incorrect syntax for MSG')
            continue

        # load all appropriate data to send to server
        info = {
            'command': 'MSG',
            'thread_title': info_input[1],
            'message': ' '.join(info_input[2:]),
            'username': username
        }

        # try-except block to ensure server is still running
        try:
            post_message(client_socket, info)
        except JSONDecodeError:
            print('Server was shut down')
            exit()
    elif info_input[0] == 'DLT' or info_input[0] == 'dlt':
        if len(info_input) != 3 or not info_input[2].isdigit() or int(info_input[2]) < 1:
            print('Incorrect syntax for DLT')
            continue

        # load all appropriate data to send to server
        info = {
            'command': 'DLT',
            'thread_title': info_input[1],
            'message_number': int(info_input[2]),
            'username': username
        }

        # try-except block to ensure server is still running
        try:
            delete_message(client_socket, info)
        except JSONDecodeError:
            print('Server was shut down')
            exit()
    elif info_input[0] == 'EDT' or info_input[0] == 'edt':
        if len(info_input) != 4 or not info_input[2].isdigit() or int(info_input[2]) < 1:
            print('Incorrect syntax for EDT')
            continue

        # load all appropriate data to send to server
        info = {
            'command': 'EDT',
            'thread_title': info_input[1],
            'message_number': int(info_input[2]),
            'message': ' '.join(info_input[3:]),
            'username': username
        }

        # try-except block to ensure server is still running
        try:
            edit_message(client_socket, info)
        except JSONDecodeError:
            print('Server was shut down')
            exit()
    elif info_input[0] == 'LST' or info_input[0] == 'lst':
        if len(info_input) != 1:
            print('Incorrect syntax for LST')
            continue

        # load all appropriate data to send to server
        info = {
            'command': 'LST',
            'username': username
        }

        # try-except block to ensure server is still running
        try:
            list_threads(client_socket, info)
        except JSONDecodeError:
            print('Server was shut down')
            exit()
    elif info_input[0] == 'RDT' or info_input[0] == 'rdt':
        if len(info_input) != 2:
            print('Incorrect syntax for RDT')
            continue

        # load all appropriate data to send to server
        info = {
            'command': 'RDT',
            'thread_title': info_input[1],
            'username': username
        }

        # try-except block to ensure server is still running
        try:
            read_thread(client_socket, info)
        except JSONDecodeError:
            print('Server was shut down')
            exit()
    elif info_input[0] == 'UPD' or info_input[0] == 'upd':
        if len(info_input) != 3:
            print('Incorrect syntax for UPD')
            continue

        # load all appropriate data to send to server
        info = {
            'command': 'UPD',
            'thread_title': info_input[1],
            'filename': info_input[2],
            'username': username
        }

        # try-except block to ensure server is still running
        try:
            upload_file(client_socket, info)
        except JSONDecodeError:
            print('Server was shut down')
            exit()
    elif info_input[0] == 'DWN' or info_input[0] == 'dwn':
        if len(info_input) != 3:
            print('Incorrect syntax for DWN')
            continue

        # load all appropriate data to send to server
        info = {
            'command': 'DWN',
            'thread_title': info_input[1],
            'filename': info_input[2],
            'username': username
        }

        # try-except block to ensure server is still running
        try:
            download_file(client_socket, info)
        except JSONDecodeError:
            print('Server was shut down')
            exit()
    elif info_input[0] == 'RMV' or info_input[0] == 'rmv':
        if len(info_input) != 2:
            print('Incorrect syntax for RMV')
            continue

        # load all appropriate data to send to server
        info = {
            'command': 'RMV',
            'thread_title': info_input[1],
            'username': username
        }

        # try-except block to ensure server is still running
        try:
            remove_thread(client_socket, info)
        except JSONDecodeError:
            print('Server was shut down')
            exit()
    elif info_input[0] == 'XIT' or info_input[0] == 'xit':
        if len(info_input) != 1:
            print('Incorrect syntax for XIT')
            continue

        # load all appropriate data to send to server
        info = {
            'command': 'XIT',
            'username': username
        }

        # try-except block to ensure server is still running
        try:
            client_exit(client_socket, info)
        except JSONDecodeError:
            print('Server was shut down')
            exit()
    elif info_input[0] == 'SHT' or info_input[0] == 'sht':
        if len(info_input) != 2:
            print('Incorrect syntax for SHT')
            continue

        # load all appropriate data to send to server
        info = {
            'command': 'SHT',
            'password': info_input[1],
            'username': username
        }

        # try-except block to ensure server is still running
        try:
            shutdown(client_socket, info)
        except JSONDecodeError:
            print('Server was shut down')
            exit()
    else:
        command_error()
