import socket
import argparse
import errno
import sys
import random
import time
import pickle
import traffic_generator_v4

parser = argparse.ArgumentParser(description="This is the client for the multi threaded socket server!")
parser.add_argument('--host', metavar='host', type=str, nargs='?', default=socket.gethostname())
parser.add_argument('--port', metavar='port', type=int, nargs='?', default=9999)
args = parser.parse_args()

HEADER_LENGTH = 10

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((args.host, args.port))
client_socket.setblocking(False)

useraddr = args.host.encode('utf-8')
useraddr_header = f"{len(useraddr):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(useraddr_header + useraddr)

print("New connection made to to server.")

analytics_list = []


def receive_response(s_socket):
    try:
        message_header = s_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())

        return {'header': message_header, 'db_data': s_socket.recv(message_length)}

    except:
        return False


def communication_algorithm():
    client_recvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_recvsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_recvsock.bind((args.host, args.port + 1))
    client_recvsock.listen()
    recvsocklist = [client_recvsock]
    server = {}

    while True:
        query = traffic_generator_v4.generateQuery()
        script = traffic_generator_v4.generateXSS()

        data = random.choice([query, script])
        request = data

        if request:
            request = request.encode('utf-8')
            request_header = f"{len(request):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(request_header + request)
            print("Sent Request:", request)
            time.sleep(4)

            if "SELECT".encode("utf-8") in request:
                try:
                    server_sock, server_address = client_recvsock.accept()
                    serv = receive_response(server_sock)
                    if serv is False:
                        continue

                    recvsocklist.append(client_recvsock)

                    server[client_socket] = serv

                    print('Connection established to receive data from {}:{}'.format(*server_address))

                    raw_db_data = serv['db_data']
                    db_data = pickle.loads(raw_db_data)
                    print("Server Response: ", db_data)
                    print()
                    continue

                except IOError as e:
                    if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                        print('I/O Reading error: {}'.format(str(e)))
                        sys.exit()

                except Exception as e:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()

            else:
                try:
                    server_sock, server_address = client_recvsock.accept()
                    serv = receive_response(server_sock)
                    if serv is False:
                        continue

                    recvsocklist.append(client_recvsock)

                    server[client_socket] = serv

                    print('Connection established to receive data from {}:{}'.format(*server_address))

                    raw_db_data = serv['db_data']
                    db_data = pickle.loads(raw_db_data)
                    db_data = db_data.decode('utf-8')
                    print("Server Response: ", db_data)
                    print()

                except IOError as e:
                    if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                        print('I/O Reading error: {}'.format(str(e)))
                        sys.exit()

                except Exception as e:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()

            client_recvsock.close()

            client_recvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_recvsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            client_recvsock.bind((args.host, args.port + 1))
            client_recvsock.listen()
            recvsocklist = [client_recvsock]

# running main function shows generated outputs for debugging
if __name__ == '__main__':
    communication_algorithm()

