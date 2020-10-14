#!/usr/bin/env python3
#
# Proxy a tcp port to a remote host+port and log to stdout
#
# Author: Jesper Tiberg 2020
# Home: https://github.com/jtiberg/tcp-forward
# License: LGPL 2.1
#

import logging
import select
import socket
import sys

id_counter = 0
server_socket = socket.socket()
source_to_dest_map = {}  # socket -> socket

log = logging.getLogger("")


def setup_tcp_proxy(server_sock, destination_host, destination_port):
    global id_counter
    client_sock, client_info = server_sock.accept()
    client_sock.setblocking(False)
    try:
        tsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tsock.connect((destination_host, destination_port))
        tsock.setblocking(False)
        id_counter += 1
        source_to_dest_map[client_sock] = ("%d>" % id_counter, tsock)
        source_to_dest_map[tsock] = ("%d<" % id_counter, client_sock)
        log.info("%d\tConnection from %s" % (id_counter, client_info))
    except ConnectionError as e:
        log.error("ERROR: could not setup connection to %d : %s" % (destination_port, e))
        client_sock.close()


# return None if connection was dropped
def socket_recv(s):
    try:
        data = s.recv(1024)
        if len(data) == 0:
            return None
        return data
    except IOError as e:
        print("IOError: ", e)
        return None


# Return True if some action was performed
def do_select():
    inputs = list(source_to_dest_map.keys()) + [server_socket]
    readable, writable, exceptional = select.select(inputs, [], inputs, 5)
    if (len(readable) + len(writable) + len(exceptional)) == 0:
        return False

    for s in exceptional:
        log.warning("Got exceptional reading from %s" % str(s.getsockname()))
    for s in readable:
        if s == server_socket:
            setup_tcp_proxy(s, remote_host, remote_port)
        else:
            con_desc, d = source_to_dest_map[s]
            data = socket_recv(s)
            if data is None:
                log.info("%s\tdisconnected" % str(con_desc))
                del source_to_dest_map[d]
                del source_to_dest_map[s]
                d.close()
                break
            log.info("%s\t%d bytes" % (con_desc, len(data)))
            x = data
            log.debug("%s\t%s" % (con_desc, x))
            d.send(data)

    return True


def fwd(local_port, remote_host, remote_port):
    log.info("Forwarding %d -> %s:%d" % (local_port, remote_host, remote_port))
    log.info("Note: X> means data flowing to remote in connection with id X. X< means data from remote")
    server_socket.bind(("0.0.0.0", local_port))
    server_socket.listen(1)
    try:
        while True:
            do_select()
    except KeyboardInterrupt:
        log.info("ctrl-c pressed")
        pass


def init_logging(log_level=logging.INFO):
    logging.basicConfig(level=log_level,
                        format='%(asctime)s %(levelname)s\t%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[
                            logging.StreamHandler()
                        ]
                        )


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("SYNTAX: fwd.py <local port> <remove host> <remote port> |-v for verbose mode|")
    else:
        argv = list(filter(lambda x: not x.startswith("-"), sys.argv))
        verbose = "-v" in sys.argv
        init_logging(logging.DEBUG if verbose else logging.INFO)
        local_port = int(argv[1])
        remote_host = argv[2]
        remote_port = int(argv[3])
        fwd(local_port, remote_host, remote_port)
