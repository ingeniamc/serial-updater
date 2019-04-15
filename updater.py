'''
Framing support for X-Core Ingenia Drives

Author/s:
    Roger Juanpere <rjuanpere@ingeniamc.com>

Copyright (c) 2017 Ingenia Motion Control
'''

import argparse
from mcb import *
import time
import struct

__all__ = ['firmware_updater']
__version__ = "1.3.0"

# serial port settings (baudrate, timeout (s))
SER_BAUDRATE = 115200
SER_TIMEOUT = 1.0

def boot_process(mcb, node, subnode, input):
    if (input):
        load_file = open(input, "r")
        try:
            for line in load_file:
                words = line.split()
                
                cmd = int (words[1] + words[0], 16)

                data = b''
                num = 2
                while num in range(2, len(words)):
                    # load data MCB
                    data = data + bytes([int(words[num], 16)])
                    num = num + 1

                # send message
                mcb.raw_cmd(node, subnode, cmd, data)
                # read from buffer the answer
                rcv = mcb.read()
                cmd_rcv = mcb.unmsg(rcv)
                if cmd_rcv != 3:
                    raise Exception('\nNo ACK received (cmd : %d' % (cmd_rcv))

                if cmd == 0x67E4:
                    time.sleep(1)

            print ('\nBootloader process success!\n\n')
        except Exception as ex:
            print ('Error during bootloading process (' + repr(ex) + ')\n\n')


def firmware_updater(port, input, node, subnode):
    # welcome message
    print ('Firmware updater for Motion Core [Version ' + __version__ + ']')
    print ('Ingenia Motion Control (c) 2018')
    print ('')
    print ('[Node %d ]' % node)
    print ('[SubNode %d]' % subnode )

    # Open MCB comm
    mcb = Mcb(port, SER_BAUDRATE, SER_TIMEOUT)

    boot_process(mcb, node, subnode, input)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--com', type=str, required=True,
                        help='COM port used')
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='Input file')
    parser.add_argument('-n', '--node', type=int, default=10, required=False,
                        help='Driver Node id')
    parser.add_argument('-sn', '--subnode', type=int, default=1, required=False,
                        help='Driver SubNode id ')
    args = parser.parse_args()

    firmware_updater(args.com, args.input, args.node, args.subnode)
