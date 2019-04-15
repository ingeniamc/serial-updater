import serial
import struct
import binascii

#fixme: Implemneted crypto
__all__ = ['Mcb',
           'McbException']


class McbException(Exception):
    pass

class Mcb(object):
    # Header definition bits
    def __init__(self, port, baudrate, timeout):
        try:
            self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
            self.ser.flush()
        except serial.SerialException as ex:
            print ('Port already in use')

    def __del__(self):        
        self.ser.close()

    def unmsg(self, inframe):
        # Base uart frame (subnode [4 bits], node [12 bits],
        # addr [12 bits], cmd [3 bits], pending [1 bit], 
        # data [8 bytes]) and CRC [2 bytes] is 14 bytes long
        header = inframe[2:4]
        cmd = struct.unpack('<H', header)[0] >> 1
        cmd = cmd & 0x7;

        # CRC is computed with header and data (removing Tx CRC)
        crc = binascii.crc_hqx(inframe[0:-2], 0)
        crcread = struct.unpack('<H', inframe[-2:])[0]
        if crcread != crc:
           raise McbException('CRC error')

        return cmd

    def check_ack(self):
        rcv = self.read()
        ret_cmd = self.unmsg(rcv)
        if ret_cmd != 3:
            raise Exception('No ACK received (command received %d)' % (ret_cmd))

        return ret_cmd

    def read_buffer(self):
        uart_frame_size_bytes = 14
        try:
            rcv = self.ser.read(uart_frame_size_bytes)

        except self.ser.SerialTimeoutException:
            print ('Error reading serial port')

        if rcv == "":
            raise McbException('No frame received')
        return rcv

    def write(self, cmd, data, size):
        frame = self.msg(cmd, data, size)
        self.ser.write(frame)

    def read(self):
        rcv = self.read_buffer()
        return rcv

    def raw_msg(self, node, subnode, cmd, data, segmented):
        node_head = (node << 4) | (subnode & 0xf)
        node_head = struct.pack('<H', node_head)

        if segmented:
            cmd = cmd + 1
        head = struct.pack('<H', cmd)

        ret = node_head + head + data + struct.pack('<H', binascii.crc_hqx(node_head + head + data, 0))
        return ret


    def raw_cmd(self, node, subnode, cmd, data):
        print ('.', end = '', flush=True)

        while len(data) > 8:
            shortdata = data[0:8]
            data = data[8:]
            frame = self.raw_msg(node, subnode, cmd, shortdata, True)
            self.ser.write(frame)
            self.check_ack()

        if len(data) < 8:
            data = data + bytes([0] * (8 - len(data)))

        frame = self.raw_msg(node, subnode, cmd, data, False)
        self.ser.write(frame)
