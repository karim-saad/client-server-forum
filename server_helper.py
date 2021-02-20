from os.path import isfile
from json import dumps, loads
from os import remove, listdir


users = []
threads = []


def unpack_credentials():
    '''
    - Load all existing credentials
    - Create file if no existing file
    '''
    if not isfile('credentials.txt'):
        open('credentials.txt', 'x')
    creds = open('credentials.txt').readlines()
    global users
    users = list(map(lambda x: {
        'username': x.split()[0],
        'password': x.split()[1]
    }, creds))


def username(connection, data):
    '''
    - Request new password if user does not exist
    - Request corresponding password if user is existing
    '''
    username = data['username']
    if username not in list(map(lambda x: x['username'], users)):
        print('New user')
        response = {
            'response-type': 'NEW_USER',
        }
        connection.sendall(dumps(response).encode())
    else:
        response = {
            'response-type': 'REQUEST_PASSWORD'
        }
        connection.sendall(dumps(response).encode())


def password(connection, data):
    '''
    - Enter new username-password combination if username not existing
    - Verify corresponding password if username existing
    '''
    _, username, password = data.values()
    if username not in list(map(lambda x: x['username'], users)):
        users.append({
            'username': username,
            'password': password
        })

        num_lines = len(open('credentials.txt').readlines())
        new_creds = open('credentials.txt', 'a')
        if num_lines == 0:
            new_creds.write(f'{username} {password}')
        else:
            new_creds.write(f'\n{username} {password}')
        new_creds.close()

        print(f'{username} successful login')
        response = {
            'response-type': 'OK',
        }
        connection.sendall(dumps(response).encode())
    else:
        for user in users:
            if user['username'] == username and user['password'] == password:
                print(f'{username} successful login')
                response = {
                    'response-type': 'OK'
                }
                connection.sendall(dumps(response).encode())
                return

        print('Incorrect password')
        response = {
            'response-type': 'BAD-PASSWORD'
        }
        connection.sendall(dumps(response).encode())


def create_thread(connection, data):
    '''
    - Create a new file named with the provided thread title
    - Error: file with that name already exists
    '''
    command, thread_title, username = data.values()
    print(f'{username} issued {command} command')

    if thread_title in threads:
        print(f'Thread {thread_title} exists')
        response = {
            'message': f'Thread {thread_title} exists'
        }
        connection.sendall(dumps(response).encode())
    else:
        threads.append(thread_title)
        new_thread = open(thread_title, 'w')
        new_thread.write(username)
        new_thread.close()

        print(f'Thread {thread_title} created')
        response = {
            'message': f'Thread {thread_title} created'
        }
        connection.sendall(dumps(response).encode())


def post_message(connection, data):
    '''
    - Append a message line to a file with corresponding thread title
    - Format: message_number username: message
    - Error: a file with that name does not exist
    '''
    command, thread_title, message, username = data.values()
    print(f'{username} issued {command} command')

    if thread_title not in threads:
        print(f'Invalid thread specified')
        response = {
            'message': f'Thread {thread_title} does not exist'
        }
        connection.sendall(dumps(response).encode())
    else:
        num_lines = len(open(thread_title).readlines())

        thread = open(thread_title, 'a')
        thread.write(f'\n{num_lines} {username}: {message.rstrip()}')
        thread.close()

        print(f'Message posted to thread {thread_title}')
        response = {
            'message': f'Message posted to thread {thread_title}'
        }
        connection.sendall(dumps(response).encode())


def delete_message(connection, data):
    '''
    - Delete a line with corresponding message number from a file with corresponding thread title
    - Error: a file with that name does not exist
    - Error: a message line with that message number does not exist
    - Error: the message line with the corresponding username does not belong to that user
    '''
    command, thread_title, message_number, username = data.values()
    print(f'{username} issued {command} command')

    if thread_title not in threads:
        print('Invalid thread specified')
        response = {
            'message': f'Thread {thread_title} does not exist'
        }
        connection.sendall(dumps(response).encode())
    else:
        thread = open(thread_title).readlines()

        delete_index = 0
        for index, line in enumerate(thread):
            msg_no = line.split(':')[0].split(' ')[0]
            if msg_no.isdigit() and int(msg_no) == message_number:
                delete_index = index

        if delete_index == 0:
            print('Invalid message number specified')
            response = {
                'message': f'Message number {message_number} does not exist in {thread_title} thread'
            }
            connection.sendall(dumps(response).encode())
            return

        proposed_user = thread[delete_index].split(':')[0].split(' ')[1]
        if username != proposed_user:
            print('Message cannot be removed')
            response = {
                'message': f'Message number {message_number} to another user and cannot be removed'
            }
            connection.sendall(dumps(response).encode())
        else:
            thread.pop(delete_index)

            new_thread = ''
            for i, msg in enumerate(thread):
                if not msg[0].isdigit() or i < message_number:
                    new_thread += msg
                else:
                    new_thread += str(i) + msg[1:]

            if len(thread) == delete_index:
                new_thread = new_thread[:-1]

            new_thread_file = open(thread_title, 'w')
            new_thread_file.write(new_thread)

            print(f'Message deleted from {thread_title} thread')
            response = {
                'message': f'Message number {message_number} deleted from {thread_title} thread'
            }
            connection.sendall(dumps(response).encode())


def edit_message(connection, data):
    '''
    - Edit a line with corresponding message number from a file with corresponding thread title
    - Error: a file with that name does not exist
    - Error: a message line with that message number does not exist
    - Error: the message line with the corresponding username does not belong to that user
    '''
    command, thread_title, message_number, message, username = data.values()
    print(f'{username} issued {command} command')

    if thread_title not in threads:
        print('Invalid thread specified')
        response = {
            'message': f'Thread {thread_title} does not exist'
        }
        connection.sendall(dumps(response).encode())
    else:
        thread = open(thread_title).readlines()

        edit_index = 0
        for index, line in enumerate(thread[1:]):
            msg_no = line.split(':')[0].split(' ')[0]
            if msg_no.isdigit() and int(msg_no) == message_number:
                edit_index = index + 1

        if edit_index == 0:
            print('Invalid message number specified')
            response = {
                'message': f'Message number {message_number} does not exist in {thread_title} thread'
            }
            connection.sendall(dumps(response))
            return

        proposed_user = thread[edit_index].split(':')[0].split(' ')[1]
        if username != proposed_user:
            print('Message cannot be edited')
            response = {
                'message': f'Message number {message_number} belongs to another user and cannot be edited'
            }
            connection.sendall(dumps(response).encode())
        else:
            new_thread = ''
            for i, msg in enumerate(thread):
                if not msg[0].isdigit() or i != message_number:
                    new_thread += msg
                else:
                    new_thread += f'{msg.split(":")[0]}: {message}\n'

            if len(thread) == edit_index + 1:
                new_thread = new_thread[:-1]

            new_thread_file = open(thread_title, 'w')
            new_thread_file.write(new_thread)

            print(
                f'Message number {message_number} edited in {thread_title} thread')
            response = {
                'message': f'Message number {message_number} edited in {thread_title} thread'
            }
            connection.sendall(dumps(response).encode())


def list_threads(connection, data):
    '''
    - Retrieve a list of all existing threads and provide to client
    '''
    command, username = data.values()
    print(f'{username} issued {command} command')

    if len(threads) == 0:
        response = {
            'message': 'No threads to list'
        }
        connection.sendall(dumps(response).encode())
    else:
        response = {
            'message': '\n'.join(threads)
        }
        connection.sendall(dumps(response).encode())


def read_thread(connection, data):
    '''
    - Retrieve all messages from a file with corresponding thread title and provide to client
    - Error: a file with that name does not exist
    '''
    command, thread_title, username = data.values()
    print(f'{username} issued {command} command')

    if thread_title not in threads:
        print('Invalid thread specified')
        response = {
            'message': f'Thread {thread_title} does not exist'
        }
        connection.sendall(dumps(response).encode())
    else:
        thread = open(thread_title).readlines()
        if len(thread) == 1:
            response = {
                'message': f'Thread {thread_title} is empty'
            }
            connection.sendall(dumps(response).encode())
        else:
            response = {
                'message': ''.join(thread[1:])
            }
            connection.sendall(dumps(response).encode())
        print(f'Thread {thread_title} read')


def upload_file(connection, data):
    '''
    - Download content from file sent by client
    - Error: a file with corresponding thread name does not exist
    '''
    command, thread_title, filename, username = data.values()
    print(f'{username} issued {command} command')

    if thread_title not in threads:
        print('Invalid thread specified')
        response = {
            'message': f'Thread {thread_title} does not exist'
        }
        connection.sendall(dumps(response).encode())
    else:
        thread = open(thread_title, 'a')
        thread.write(f'\n{username} uploaded {filename}')
        thread.close()

        response = {
            'message': 'SEND'
        }
        connection.sendall(dumps(response).encode())

        data = loads(connection.recv(1024).decode())
        if data['response-type'] == 'BAD':
            print(f'Invalid file specified')
        else:
            sent_file = connection.recv(1024)
            receive_file = open(f'{thread_title}-{filename}', 'wb')
            receive_file.write(sent_file)
            receive_file.close()
            print(f'{username} uploaded file {filename} to {thread_title} thread')
            response = {
                'message': f'{filename} uploaded to {thread_title} thread'
            }
            connection.sendall(dumps(response).encode())


def download_file(connection, data):
    '''
    - Send content from file requested by client
    - Error: a file with corresponding thread name does not exist
    - Error: the file requested by file does not exist
    '''
    command, thread_title, filename, username = data.values()
    print(f'{username} issued {command} command')

    if thread_title not in threads:
        print('Invalid thread specified')
        response = {
            'message': f'Thread {thread_title} does not exist'
        }
        connection.sendall(dumps(response).encode())
    else:
        try:
            send_file = open(f'{thread_title}-{filename}', 'rb')
        except IOError:
            print(f'{filename} does not exist in {thread_title} thread')
            response = {
                'response-type': 'BAD',
                'message': f'File {filename} does not exist'
            }
            connection.sendall(dumps(response).encode())
            return

        print(f'{filename} downloaded from {thread_title} thread')
        info = {
            'response-type': 'SENT',
            'message': f'{filename} successfully downloaded'
        }
        connection.sendall(dumps(info).encode())
        connection.sendall(send_file.read())


def remove_thread(connection, data):
    '''
    - Remove a file named with the provided thread title
    - Error: file with that name does not exist
    '''
    command, thread_title, username = data.values()
    print(f'{username} issued {command} command')

    if thread_title not in threads:
        print('Invalid thread specified')
        response = {
            'message': f'Thread {thread_title} does not exist'
        }
        connection.sendall(dumps(response).encode())
    else:
        thread = open(thread_title).readlines()
        if thread[0].rstrip() != username:
            print(f'Thread {thread_title} cannot be removed')
            response = {
                'message': f'Thread {thread_title} belongs to another user and cannot be removed'
            }
            connection.sendall(dumps(response).encode())
        else:
            threads.remove(thread_title)
            for filename in listdir():
                if filename.split('-')[0] == thread_title:
                    remove(filename)
            print(f'Thread {thread_title} removed')
            response = {
                'message': f'Thread {thread_title} removed'
            }
            connection.sendall(dumps(response).encode())


def client_exit(connection, data):
    '''
    - Close connection with a client
    '''
    username = data['username']
    print(f'{username} exited')
    connection.close()


def shutdown(connection, data, admin_passwd):
    '''
    - Close connection with all clients
    - Remove all files associated with servers
    - Shut down server
    - Error: Incorrect password specified
    '''
    command, password, username = data.values()
    print(f'{username} issued {command} command')

    if admin_passwd is None or admin_passwd == password:
        remove('credentials.txt')
        for filename in listdir():
            if filename.split('-')[0] in threads:
                remove(filename)

        print('Server shutting down')
        response = {
            'status': 'SHUTDOWN',
            'message': 'Goodbye. Server shutting down'
        }
        connection.sendall(dumps(response).encode())
        return True
    else:
        print('Incorrect password')
        response = {
            'status': 'WRONG_PASSWORD',
            'message': 'Incorrect password'
        }
        connection.sendall(dumps(response).encode())
        return False
