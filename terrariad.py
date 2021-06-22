#!/usr/bin/env python3

import argparse
import logging
import shlex
import struct
import socket
import subprocess
import sys

from argparse import ArgumentTypeError
from socket   import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET

def main(args):
    logger = logging.getLogger()

    def setup_terraria_socket():
        terraria_socket = socket.socket(AF_INET, SOCK_STREAM)
        terraria_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        terraria_socket.bind((args.host, args.port))
        terraria_socket.listen()
        return terraria_socket

    def send_disconnect_message(connection):
        #      type rsnlen
        #       /\    /\
        # xx xx 02 00 yy zz ... zz
        # \---/    \/    \-------/
        # msglen  pad       rsn
        message_format = f"<hbbb{len(args.reason)}s"
        message_length = 2 + (3 * 1) + len(args.reason)
        message_type   = 2

        message = struct.pack(message_format, message_length, message_type, 0,
            len(args.reason), args.reason)
        connection.send(message)

    while True:
        try:
            with setup_terraria_socket() as terraria_socket:
                (connection, _) = terraria_socket.accept()
                with connection:
                    send_disconnect_message(connection)
            # TODO: Text entered into terminal is invisible if the subprocess
            #       is started and then both the subprocess as well as the
            #       terrariad process are stopped via CTRL + C.
            subprocess.run(args.exec)
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            logger.exception("Encountered unexpected exception")

class ReasonAction(argparse.Action):

    _MAX_REASON_LEN = 127

    def __call__(self, parser, namespace, values, option_string):
        reason_bytes = values.encode("ascii")
        if (len(reason_bytes) > MessageAction._MAX_REASON_LEN):
            raise ArgumentTypeError("test")
        setattr(namespace, self.dest, reason_bytes)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", default="")
    parser.add_argument("-p", "--port", default=7777)
    parser.add_argument("-e", "--exec", required=True)
    parser.add_argument("-r", "--reason", action=ReasonAction, default=b"The server is starting. Please wait and retry connecting in a bit.")

    args      = parser.parse_args()
    args.exec = shlex.split(args.exec)

    main(args)
