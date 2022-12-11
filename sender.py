from socket import *
from util import make_packet


class Sender:
    def __init__(self):
        """ 
        Your constructor should not expect any argument passed in,
        as an object will be initialized as follows:
        sender = Sender()
        
        Please check the main.py for a reference of how your function will be called.
        """
        # packet num
        self.__packet_num = 0
        # sequence num
        self.__seq_num = 0

    def send_packet(self, packet, app_msg_str):
        # create socket，Port # = 10000 + 4177208 % 500 = 10208
        client_socket = socket(AF_INET, SOCK_DGRAM)
        # set timeout
        client_socket.settimeout(9)
        dest_addr = ('127.0.0.1', 10208)
        # send packt
        client_socket.sendto(packet, dest_addr)
        self.__packet_num += 1
        print('packet num.' + str(self.__packet_num) + ' is successfully sent to the receiver.')

        try:
            # receive message from receiver
            msg, server_socket = client_socket.recvfrom(1024)
            # get ack number
            ack = msg[11] & 1
            if self.__seq_num == ack:
                # packet is received correctly
                print('packet is received correctly: seq.num ' + str(self.__seq_num) + ' = ' + 'ACK num ' + str(ack) + '. all done!')
                print(''*3)
                self.__seq_num = 0 if self.__seq_num == 1 else 1
            else:
                # packet is corrupted
                print('receiver acked the previous pkt, resend!')
                print(''*3)
                print('[ACK-Previous retransmission]: ' + app_msg_str)
                self.send_packet(packet, app_msg_str)
            client_socket.close()
        except Exception as e:
            # timeout
            print('socket timeout! Resend!')
            print(''*3)
            print('[timeout retransmission]: ' + app_msg_str)
            self.send_packet(packet, app_msg_str)

    def rdt_send(self, app_msg_str):
        """realibly send a message to the receiver (MUST-HAVE DO-NOT-CHANGE)

      Args:
        app_msg_str: the message string (to be put in the data field of the packet)

      """
        print('original message string: ' + app_msg_str)
        # generate packet
        packet = make_packet(app_msg_str, 0, self.__seq_num)
        print('packet created: ', end='')
        print(packet)
        # send packet to receiver
        self.send_packet(packet, app_msg_str)
