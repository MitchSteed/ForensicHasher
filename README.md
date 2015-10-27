# ForensicHasher

The Forensic Hasher is basically an enhanced netcat (although it doesn't use netcat under the hood). It is made up of two parts the workstation and the victm

## Workstation
The workstation listens for any and all incoming requests and upon receipt of those requests writes the data to a file, creates a hash of that file and a timestamp writing to the local directory.

The workstation can receive a parameter for which port to bind to (defaults to 3000) and a hashing algorithm to use (to view available algorithsm on your system run ./workstation -h). The workstation will continue listening until shut down.

Example Usage:

python workstation -p 3000 -a md5

## Victim
The victim connects to a remote host over the network and passes whatever it receives from standard input to the workstation. The victim has arguments to pass host, port, and filename. Port defaults to 3000, host defaults to localhost, and filename defaults to ForensicHasher.txt although you certainly would want to generally pass this argument. 

Example Usage:
```
cat /etc/passwd python victim.py -p 3000 -d 192.192.192.192 -n etc.passwd.txt
```

Which then will connect to the workstation which will create the following files:
etc.passwd.txt
etc.passwd.txt.md5
etc.passwd.txt.date

### Add Victim to the path
To add the victim.py to your path to simplify usage simply change the permissions by
```
chmod +x victim.py
cd /usr/bin
ln -s ~/path/to/victim.py
```
