#!/usr/bin/env python

'''
'   Author: Mitchell Steed
'   Contributing Author: Douglas Kelly
'   This file opens up a socket on the Host machine and allows the standard in from the Victim to be piped to it.
'''

'Import argument Parser, a library used for generating easy documentation based on expected parameter flags
import argparse
'Imports the datetime library used for disecting and interpreting datetime formats
import datetime
'Imports the hashlib library, used for creation of hashes based on the content imported from the socket
import hashlib
'Imports the socket library, used to establish a tunnel between the bictim and host machines
import socket

'Set program constants
buff_size = 1024
hash_algorithm = "md5"
data_delim = "%%%%"

def parse_arguments():
    ''' parse arguments, which include '-p' for port and '-a' for algorithms'''
    parser = argparse.ArgumentParser(prog='Forensic Hasher', description='A simple tool to date, and hash linux command outputs', add_help=True)
    parser.add_argument('-p', '--port', type=int, action='store', help='port the victim will listen on', default=3000)
    parser.add_argument('-a', '--algorithm', type=str, action='store',
        help='hashing algorith to use, options include: {}'.format(hashlib.algorithms), default='md5')
    args = parser.parse_args()

    return args.port, args.algorithm.lower()

def getContentsAndFileName(data):
    '' Receives a data string parameter and returns a file name along with the contents of the file being the data
    split_list = data.split(data_delim)
    file_name = split_list[-1]
    file_contents = data_delim.join(split_list[:-1])
    return file_name, file_contents

def getDate():
    '' Returns the current datetime of the imported file
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def getHash(hashable):
    '' Returns the hash of the content delivered to this method as a String parameter
    method = getattr(hashlib, hash_algorithm)
    h = method()
    h.update(hashable)
    return h.hexdigest()


def writeFile(file_name, file_contents):
    '' Writes the file to the system
    with open(file_name, "w+") as f:
        f.write(file_contents)

def writeFiles(data):
    ''' This is the main function called when content is received via the socket. 
        Takes the string data, generate the file, then gives the file to the hasher to create a hash
        Also prints out the datettime of the file, along with its hash
    '''
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
    '' 
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
    '' Main function called from the run method
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
    '' Grabs the arguments input by the user and stores them to the global variables to be used by the listen function
    port, hash_algorithm = parse_arguments()
    listen(port)

if __name__ == "__main__":
    '' Main method defined for the python file by convention
    run()
