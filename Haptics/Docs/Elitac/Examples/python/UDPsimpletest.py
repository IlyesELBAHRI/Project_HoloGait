#!/usr/bin/env python

# An Python example to demonstrate how to setup a UDP connection to the 
# Elitac Communicator software
#
# Use (write in terminal):
# >> python UDPsimpletest.py <commando>
# Example for "?IsConnected"
# >> python UDPsimpletest.py ?IsConnected
# Example for "?GetPatterns"
# >> python UPDsimpletest.py ?GetPatterns
 

from socket import *
import sys


## Setup socket ##
host="127.0.0.1"
port = 50000
addr = (host,port)
s = socket(AF_INET,SOCK_DGRAM)

## Get the commando to send ##
#commando = "?IsConnected"
commando = sys.argv[1]

## Send through UDP ##
##s.sendto(commando,addr)
if(s.sendto(commando,addr)):
	print "sending: " + commando
	
## Receive the result from the server ##
s.settimeout(1) #1sec timeout
try:
	print "receiving: " + s.recvfrom(1024)[0] #1024 bytes for receiving buffer
except timeout:
	print "No response from server (correct commando?)"	
s.close()
