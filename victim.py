#!/usr/bin/env python

import argparse
import socket
import sys




def getData():
    return sys.stdin.read()



def parse_arguments():
    ''' parse arguments, which include '-p' for port and '-h' for host'''
    parser = argparse.ArgumentParser(prog='Forensic Hasher', description='A simple tool to date, and hash linux command outputs', add_help=True)
    parser.add_argument('-p', '--port', type=int, action='store', help='port the victim will bind to', default=3000)
    parser.add_argument('-d', '--destination', type=str, action='store', help='destination host the victim will connect to', default='localhost')
    parser.add_argument('-n', '--name', type=str, action='store', help='filename to put the output in', default='ForensicHasher.txt')
    args = parser.parse_args()

    return args.destination, args.port, args.name


def send(host, port, name, data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    msg = data + "%%%%" + name
    msglen = len(msg)
    totalsent = 0
    while totalsent < msglen:
        sent = sock.send(msg[totalsent:])
        totalsent += sent
    sock.close()


def run():
    host, port, name = parse_arguments()
    data = getData()
    send(host, port, name, data)



if __name__ == "__main__":
    run()
    
