#!/usr/bin/env python

import argparse
import datetime
import hashlib
import socket

buff_size = 1024
hash_algorithm = "md5"
data_delim = "%%%%"


def parse_arguments():
    ''' parse arguments, which include '-p' for port and '-h' for host'''
    parser = argparse.ArgumentParser(prog='Forensic Hasher', description='A simple tool to date, and hash linux command outputs', add_help=True)
    parser.add_argument('-p', '--port', type=int, action='store', help='port the victim will listen on', default=3000)
    parser.add_argument('-a', '--algorithm', type=str, action='store',
        help='hashing algorith to use, options include: {}'.format(hashlib.algorithms), default='md5')
    args = parser.parse_args()

    return args.port, args.algorithm.lower()

def getContentsAndFileName(data):
    split_list = data.split(data_delim)
    file_name = split_list[-1]
    file_contents = data_delim.join(split_list[:-1])
    return file_name, file_contents

def getDate():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def getHash(hashable):
    method = getattr(hashlib, hash_algorithm)
    h = method()
    h.update(hashable)
    return h.hexdigest()


def writeFile(file_name, file_contents):
    with open(file_name, "w+") as f:
        f.write(file_contents)

def writeFiles(data):

    # main file and hash
    file_name, file_contents = getContentsAndFileName(data)
    file_hash = getHash(file_contents)
    writeFile(file_name, file_contents)
    writeFile(file_name +"." + hash_algorithm, file_hash)

    # date and date hash
    date = getDate()
    date_hash = getHash(date)
    writeFile(file_name + ".date", date)
    writeFile(file_name + ".date." + hash_algorithm, date_hash)



def handle(client):
    data = ""
    while True:
        localData = client.recv(buff_size)
        if localData:
            data += localData
        else:
            client.close()
            break

    writeFiles(data)

def listen(port):
    print "Now listening for input: "
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    sock.bind(("", port))
    sock.listen(5)
    while True:
        client, _ = sock.accept()
        handle(client)

    sock.close()

def run():
    port, hash_algorithm = parse_arguments()
    listen(port)



if __name__ == "__main__":
    run()
