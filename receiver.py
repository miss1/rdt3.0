from socket import *
from time import sleep
## No other imports allowed

from util import make_packet, verify_checksum


class UDPServer:
    def __init__(self):
        # create socket, Port # = 10000 + 4177208 % 500 = 10208
        server_port = 10208
        self.__server_socket = socket(AF_INET, SOCK_DGRAM)
        # Prepare a server socket
        self.__server_socket.bind(('', server_port))
        # packet num
        self.__packet_num = 0
        # previous packet sequence
        self.__previous_seq = -1
        print('The UDP serve is ready to receive...')

    def start(self):
        while True:
            msg, client_socket = self.__server_socket.recvfrom(1024)
            self.__packet_num += 1
            print('packet num.' + str(self.__packet_num) + ' received: ', end='')
            print(msg)
            # Check if the packet is corrupted
            is_msg_valid = verify_checksum(msg)
            if self.__packet_num % 6 == 0:
                # packet loss
                print('simulating packet loss: sleep a while to trigger timeout event on the send side...')
                sleep(10)
            elif (not is_msg_valid) or self.__packet_num % 3 == 0:
                # packet corruption
                print('simulating packet bit errors/corrupted: ACK the previous packet!')
                response_packet = make_packet('', 1, self.__previous_seq)
                self.__server_socket.sendto(response_packet, client_socket)
            else:
                # The packet is well received
                print('packet is expected, message string delivered: ' + msg[12:].decode())
                print('packet is delivered, now creating and sending the ACK packet...')
                seq = msg[11] & 1
                response_packet = make_packet('', 1, seq)
                self.__server_socket.sendto(response_packet, client_socket)
                self.__previous_seq = seq
            print('all done for this packet!')
            print(''*3)


def main():
    server = UDPServer()
    server.start()


if __name__ == '__main__':
    main()
