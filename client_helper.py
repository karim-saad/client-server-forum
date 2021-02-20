from json import loads, dumps


def client_connection(client_socket):
    '''
    - Send client connection message to server
    '''
    info = {
        'command': 'LOG',
        'message': 'Client connected'
    }
    client_socket.sendall(dumps(info).encode())


def credentials(client_socket):
    '''
    - Prompt the client to input a username and password
    - Return the username
    '''
    username = input('Enter username: ')
    info = {
        'command': 'USER',
        'username': username
    }
    client_socket.sendall(dumps(info).encode())

    response = loads(client_socket.recv(1024).decode())
    if response['response-type'] == 'NEW_USER':
        password = input(f'Enter new password for {username}: ')
        info = {
            'command': 'PASS',
            'username': username,
            'password': password
        }
        client_socket.sendall(dumps(info).encode())
    else:
        password = input('Enter password: ')
        info = {
            'command': 'PASS',
            'username': username,
            'password': password
        }
        client_socket.sendall(dumps(info).encode())

    response = loads(client_socket.recv(1024).decode())
    if response['response-type'] == 'OK':
        print('Welcome to the forum')
        return username
    else:
        print('Invalid password')
        username = credentials(client_socket)


def create_thread(client_socket, info):
    '''
    - Create a new thread in the server
    - Error: thread already exists
    '''
    client_socket.sendall(dumps(info).encode())
    response = loads(client_socket.recv(1024).decode())
    print(response['message'])


def post_message(client_socket, info):
    '''
    - Post a message in an existing thread
    - Error: thread does not exist
    '''
    client_socket.sendall(dumps(info).encode())
    response = loads(client_socket.recv(1024).decode())
    print(response['message'])


def delete_message(client_socket, info):
    '''
    - Delete a message in an exising thread
    - Error: thread does not exist
    - Error: message does not exist
    - Error: user did not post original message
    '''
    client_socket.sendall(dumps(info).encode())
    response = loads(client_socket.recv(1024).decode())
    print(response['message'])


def edit_message(client_socket, info):
    '''
    - Edit a message in an existing thread
    - Error: thread does not exist
    - Error: message does not exist
    - Error: user did not post original message
    '''
    client_socket.sendall(dumps(info).encode())
    response = loads(client_socket.recv(1024).decode())
    print(response['message'])


def list_threads(client_socket, info):
    '''
    - List all exisiting threads in the server
    '''
    client_socket.sendall(dumps(info).encode())
    response = loads(client_socket.recv(1024).decode())
    print(response['message'])


def read_thread(client_socket, info):
    '''
    - Read an existing thread
    - Error: thread does not exist
    '''
    client_socket.sendall(dumps(info).encode())
    response = loads(client_socket.recv(1024).decode())
    print(response['message'])


def upload_file(client_socket, info):
    '''
    - Upload a file to an existing thread
    - Error: thread does not exist
    - Error: file does not exist
    '''
    client_socket.sendall(dumps(info).encode())
    response = loads(client_socket.recv(1024).decode())
    if response['message'] == 'SEND':
        try:
            send_file = open(info['filename'], 'rb')
        except IOError:
            print(f'File {info["filename"]} does not exist')
            info = {
                'response-type': 'BAD',
            }
            client_socket.sendall(dumps(info).encode())
            return

        info = {
            'response-type': 'OK'
        }
        client_socket.sendall(dumps(info).encode())
        client_socket.sendall(send_file.read())
        response = loads(client_socket.recv(1024).decode())
    print(response['message'])


def download_file(client_socket, info):
    '''
    - Download a file from an existing thread
    - Error: thread does not exist
    - Error: file does not exist
    '''
    client_socket.sendall(dumps(info).encode())
    response = loads(client_socket.recv(1024).decode())
    print(response['message'])
    if response['response-type'] == 'SENT':
        sent_file = client_socket.recv(1024)
        receive_file = open(info['filename'], 'wb')
        receive_file.write(sent_file)
        receive_file.close()


def remove_thread(client_socket, info):
    '''
    - Remove existing thread
    - Error: thread does not exist
    '''
    client_socket.sendall(dumps(info).encode())
    response = loads(client_socket.recv(1024).decode())
    print(response['message'])


def client_exit(client_socket, info):
    '''
    - Send a message to server that client is exiting
    - Terminate program
    '''
    client_socket.sendall(dumps(info).encode())
    client_socket.close()
    print('Goodbye')
    exit()


def shutdown(client_socket, info):
    '''
    - Shut down the server
    - Error: Incorrect password specified
    '''
    client_socket.sendall(dumps(info).encode())
    response = loads(client_socket.recv(1024).decode())
    print(response['message'])
    if response['status'] == 'SHUTDOWN':
        exit()


def command_error():
    '''
    - Print invalid message, then prompt user to enter a valid command
    '''
    print('Invalid command.')
    print('Valid commands: CRT, MSG, DLT, EDT, LST, RDT, UPD, DWN, RMV, XIT, SHT')
