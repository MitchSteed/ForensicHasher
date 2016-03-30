#!/usr/bin/env python

'''
'   Authors: Mitchell Steed
'   Contributing Author: Douglas Kelly
'   This file is meant to be ran on a victim machine. It pipes the content of Standard Out to the socket that this file opens
'   with the example: ls | python victim.py
'''

'Import argument Parser, a library used for generating easy documentation based on expected parameter flags'
import argparse
'Imports the socket library, used to establish a tunnel between the bictim and host machines'
import socket
'Imports the system library, used for interacting with the underlying operating system'
import sys

'Retrieves the Data from Standard In'
def getData():
    return sys.stdin.read()

'Parses the incoming arguments, or if none are provided provides content regarding which flags are available'
def parse_arguments():
    ''' parse arguments, which include '-p' for port and '-d' for host'''
    parser = argparse.ArgumentParser(prog='Forensic Hasher', description='A simple tool to date, and hash linux command outputs', add_help=True)
    parser.add_argument('-p', '--port', type=int, action='store', help='port the victim will bind to', default=3000)
    parser.add_argument('-d', '--destination', type=str, action='store', help='destination host the victim will connect to', default='localhost')
    parser.add_argument('-n', '--name', type=str, action='store', help='filename to put the output in', default='ForensicHasher.txt')
    args = parser.parse_args()

    return args.destination, args.port, args.name

'Sends the data to the established connection port on the Host machine'
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

'Function called at runtime, clean separation of running function from main'
def run():
    host, port, name = parse_arguments()
    data = getData()
    send(host, port, name, data)
    
'The Main method for Python programs as a best practice, clear code start'
if __name__ == "__main__":
    run()
