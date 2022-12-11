def create_checksum(packet_wo_checksum):
    """create the checksum of the packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet_wo_checksum: the packet byte data (including headers except for checksum field)

    Returns:
      the checksum in bytes

    """
    checksum = 0
    # Group the data into groups of 2 bytes, then sum the grouped data
    for index in range(0, len(packet_wo_checksum), 2):
        if index + 1 >= len(packet_wo_checksum):
            checksum += (packet_wo_checksum[index] << 8) + 0
        else:
            checksum += (packet_wo_checksum[index] << 8) + packet_wo_checksum[index + 1]
    # Add the carryout of the most significant bit to the result
    checksum = (checksum & 0xffff) + (checksum >> 16)
    # 1's complement of sum
    checksum = (~checksum) & 0xffff
    return checksum.to_bytes(2, "big")


def verify_checksum(packet):
    """verify packet checksum (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet: the whole (including original checksum) packet byte data

    Returns:
      True if the packet checksum is the same as specified in the checksum field
      False otherwise

    """
    checksum = 0
    # Group the data into groups of 2 bytes, then sum the grouped data
    for index in range(0, len(packet), 2):
        if index + 1 >= len(packet):
            checksum += (packet[index] << 8) + 0
        else:
            checksum += (packet[index] << 8) + packet[index + 1]
    # Add the carryout of the most significant bit to the result
    checksum = (checksum & 0xffff) + (checksum >> 16)
    # 1's complement of sum
    checksum = (~checksum) & 0xffff
    return checksum == 0


def make_packet(data_str, ack_num, seq_num):
    """Make a packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      data_str: the string of the data (to be put in the Data area)
      ack: an int tells if this packet is an ACK packet (1: ack, 0: non ack)
      seq_num: an int tells the sequence number, i.e., 0 or 1

    Returns:
      a created packet in bytes

    """
    # make sure your packet follows the required format!
    # the first 8 bytes
    prefix = 'COMPNETW'.encode()
    # the 11th and 12th bytes
    length = 12 + len(data_str)
    length = (length << 1) + ack_num
    length = (length << 1) + seq_num
    length = length.to_bytes(2, "big")
    # get checksum
    checksum = create_checksum(prefix + length + data_str.encode())
    # return packet
    return prefix + checksum + length + data_str.encode()

