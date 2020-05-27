import socket
import argparse
import select
import pymysql
import pickle

parser = argparse.ArgumentParser(description="This is the server for the multithreaded socket demo!")
parser.add_argument('--host', metavar='host', type=str, nargs='?', default=socket.gethostname())
parser.add_argument('--port', metavar='port', type=int, nargs='?', default=9999)
args = parser.parse_args()

username = "kb16315"
password = "mqttdbpwd"
database = "mqtt_mock_db"

HEADER_LENGTH = 10

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((args.host, args.port))
server_socket.listen()
sockets_list = [server_socket]
clients = {}

import detection_script_net_v3 as dsn3
received_signal = dsn3.DetectionAlgorithm().signal_to_server('')

unpacked_data = []
unpacked_data.clear()

print(f'Listening for connections on {args.host}:{args.port}...')


def receive_request(c_socket):
    try:
        message_header = c_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())

        return {'header': message_header, 'data': c_socket.recv(message_length)}

    except:
        return False


while received_signal == 'OK' or received_signal == 'NOT OK':
    read_sockets, _, exception_sockets = select.select(sockets_list, [], [])
    global client_socket, client_address

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_request(client_socket)
            if user is False:
                continue

            sockets_list.append(client_socket)

            clients[client_socket] = user

            print('Accepted new connection from {}:{}, Name: {}'.format(*client_address, user['data'].decode('utf-8')))

        else:
            message = receive_request(notified_socket)

            if message is False:
                print('Main Connection closed')
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]

            encoded_message = message["data"].decode("utf-8")
            print(f'Received message from {user["data"].decode("utf-8")}: {encoded_message}')

            # Stage 1 # Send traffic to detection script
            traffic_to_detector = dsn3.DetectionAlgorithm().query_analysis(encoded_message)
            processing = dsn3.DetectionAlgorithm().caught_injection_parts(encoded_message)
            xss_analysis = dsn3.DetectionAlgorithm().xss_max_threshold(encoded_message)

            # Stage 2 # Receive OK/NOT OK signal from detection script
            received_signal = dsn3.DetectionAlgorithm().signal_to_server(encoded_message)

            # Stage 3 # IF OK signal returned from script connect to DB ELSE send warning message
            if "SELECT" in encoded_message or "INSERT" in encoded_message:
                if received_signal == "NOT OK":
                    sqli_warning = "Potentially malicious query detected. Request denied."
                    sqli_warning = sqli_warning.encode("utf-8")
                    server_sendsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_sendsock.connect((args.host, args.port + 1))
                    server_sendsock.setblocking(False)

                    pickle_data = pickle.dumps(sqli_warning)
                    print("Sending data to client:", sqli_warning)
                    print()
                    full_response = bytes(f'{len(pickle_data):<{HEADER_LENGTH}}', 'utf-8') + pickle_data
                    try:
                        server_sendsock.sendto(full_response, client_address)
                    except OSError as e:
                        print(e)
                elif received_signal == "OK":
                    mqtt_db = pymysql.connect(host=args.host, user=username, passwd=password, db=database)
                    the_cursor = mqtt_db.cursor()
                    the_cursor.execute(message["data"].decode("utf-8"))
                    result_for_client = the_cursor.fetchall()
                    mqtt_db.commit()
                    mqtt_db.close()

                    encoded_db_data = [[str(result).encode('utf8') for result in db_data] for db_data in result_for_client]
                    decoded_db_data = []
                    db_results = []
                    # decoded_db_data.clear()
                    for encoded in encoded_db_data:
                        for data in encoded:
                            decoded_db_data.append(data.decode("utf-8"))
                        unpacked_data.append(decoded_db_data)
                    db_results.append(unpacked_data)
                    # print(unpacked_data)

                    server_sendsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_sendsock.connect((args.host, args.port + 1))
                    server_sendsock.setblocking(False)

                    if 'SELECT' in encoded_message:
                        pickle_data = pickle.dumps(db_results)
                        print("Sending data to client:", encoded_db_data)
                        print()
                        full_response = bytes(f'{len(pickle_data):<{HEADER_LENGTH}}', 'utf-8') + pickle_data
                        try:
                            server_sendsock.sendto(full_response, client_address)
                        except OSError as e:
                            print(e)
                    elif 'INSERT' in encoded_message:
                        insert_output = "Data Successfully Inserted"
                        pickle_data = pickle.dumps(insert_output.encode('utf-8'))
                        print("Sending data to client:", insert_output)
                        print()
                        full_response = bytes(f'{len(pickle_data):<{HEADER_LENGTH}}', 'utf-8') + pickle_data
                        try:
                            server_sendsock.sendto(full_response, client_address)
                        except OSError as e:
                            print(e)
                    else:
                        print("Some funny business occurred")
                    unpacked_data.clear()
            elif '<' in encoded_message:
                if received_signal == "NOT OK":
                    xss_response = "JS Found: Potentially XSS. Prevented execution as could be malicious."
                    xss_response = xss_response.encode("utf-8")
                    server_sendsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_sendsock.connect((args.host, args.port + 1))
                    server_sendsock.setblocking(False)

                    pickle_data = pickle.dumps(xss_response)
                    print("Sending data to client:", xss_response)
                    print()
                    full_response = bytes(f'{len(pickle_data):<{HEADER_LENGTH}}', 'utf-8') + pickle_data
                    try:
                        server_sendsock.sendto(full_response, client_address)
                    except OSError as e:
                        print(e)
                elif received_signal == "OK":
                    xss_response = "JS Found: Not detected as malicious. Executed Successfully"
                    xss_response = xss_response.encode("utf-8")
                    server_sendsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_sendsock.connect((args.host, args.port + 1))
                    server_sendsock.setblocking(False)

                    pickle_data = pickle.dumps(xss_response)
                    print("Sending data to client:", xss_response)
                    print()
                    full_response = bytes(f'{len(pickle_data):<{HEADER_LENGTH}}', 'utf-8') + pickle_data
                    try:
                        server_sendsock.sendto(full_response, client_address)
                    except OSError as e:
                        print(e)
            else:
                print("A problem occurred")

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
