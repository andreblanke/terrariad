#!/usr/bin/env python3

import argparse
import logging
import os
import shlex
import struct
import socket
import subprocess
import sys

from argparse import ArgumentParser
from socket   import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET

def parse_args():
    _DEFAULT_HOST = ""
    _DEFAULT_PORT = 7777

    _DEFAULT_REASON = (b"The server is starting. Please wait and retry"
                       b" connecting in a bit")

    class ReasonAction(argparse.Action):
        _MAX_REASON_LEN = 127

        def __call__(self, parser, namespace, values, option_string):
            reason_bytes = values.encode("ascii")
            if (len(reason_bytes) > ReasonAction._MAX_REASON_LEN):
                raise argparse.ArgumentTypeError("test")
            setattr(namespace, self.dest, reason_bytes)

    parser = ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
        description="Launches a Terraria daemon to start the actual server"
                    " on the first connection attempt made and disconnects"
                    " the client sending a configurable reason.")

    parser.add_argument("-H", "--host", default=_DEFAULT_HOST,
        help="hostname or IP address to bind the socket to.\n"
             "default: empty string used to bind to all network interfaces")
    parser.add_argument("-p", "--port",default=_DEFAULT_PORT,
        help="port on which to run the daemon.\n"
             f"default: standard Terraria port {_DEFAULT_PORT}")
    parser.add_argument("-e", "--exec", required=True,
        help="program to execute once a connection on the socket has been"
             " attempted")
    parser.add_argument("-d", "--working-directory", default=os.getcwd(),
        help="working directory from which to execute the program from -e\n"
             "default: current working directory")
    parser.add_argument("-r", "--reason", default=_DEFAULT_REASON,
        help="reason for disconnect sent to connecting Terraria client\n"
             f"  ASCII string with max length {ReasonAction._MAX_REASON_LEN}\n"
             f"default: '{_DEFAULT_REASON.decode('ascii')}'",
        action=ReasonAction)

    args      = parser.parse_args()
    args.exec = shlex.split(args.exec)
    return args

def main(args):
    logger = logging.getLogger()

    def setup_terraria_socket(host, port):
        terraria_socket = socket.socket(AF_INET, SOCK_STREAM)
        terraria_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        terraria_socket.bind((host, port))
        terraria_socket.listen()
        return terraria_socket

    def send_disconnect_message(connection, reason):
        #      type rsnlen
        #       /\    /\
        # xx xx 02 00 yy zz ... zz
        # \---/    \/    \-------/
        # msglen  pad       rsn
        message_format = f"<hbbb{len(reason)}s"
        message_length = 2 + (3 * 1) + len(reason)
        message_type   = 2

        message = struct.pack(message_format, message_length, message_type, 0,
            len(reason), reason)
        connection.send(message)

    os.chdir(args.working_directory)
    while True:
        try:
            with setup_terraria_socket(args.host, args.port) as terraria_socket:
                (connection, _) = terraria_socket.accept()
                with connection:
                    send_disconnect_message(connection, args.reason)
            # TODO: Text entered into terminal is invisible if the subprocess
            #       is started and then both the subprocess as well as the
            #       terrariad process are stopped via CTRL + C.
            subprocess.run(args.exec)
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            logger.exception("Encountered unexpected exception")

if __name__ == "__main__":
    main(args=parse_args())
