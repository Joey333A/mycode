#!/usr/bin/env python3

## std library imports on top
import os

## 3rd party imports below
import paramiko

## work assigned to a junior programming asset on our team
from jrprogrammer import cmdissue

def main():
  ## create session object
  sshsession = paramiko.SSHClient()
  sshsession.set_missing_host_key_policy(paramiko.AutoAddPolicy())

  mykey = paramiko.RSAKey.from_private_key_file("/home/student/.ssh/id_rsa")
  
  ## create SSH connection
  sshsession.connect(hostname='10.10.2.3', username='bender', pkey=mykey)
  
  our_commands = ["touch sshworked.txt", "touch create.txt", "touch file3.txt", "ls"]
  
  for x in our_commands:
    ## call our imported function and save the value returned
    resp = cmdissue(x, sshsession)
    ## if returned response is not null, print it out
    if resp != "":
      print(resp)
  
  ## end the SSH connection
  sshsession.close()

if __name__ == '__main__':
  main()

