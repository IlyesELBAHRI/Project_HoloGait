#!/usr/bin/env python

# An Python example to demonstrate how to setup a UDP connection to the 
# Elitac Communicator software and add tactor states to a temporary patten.
#
# Use (write in terminal):
# >> python TactorStatesExample2.py

 
from socket import *
import sys
import time
from itertools import cycle

## Setup socket ##
host="127.0.0.1"
port = 50000
addr = (host,port)
s = socket(AF_INET,SOCK_DGRAM)
s.settimeout(1) #1sec timeout



## Get the commando to send ##
commandoStart = "!ClearTactorStates"
commandoExecute = "!ExecuteTactorStates"
commandString = ["!ChangeTactorState,1,0,200","!ChangeTactorState,1,1,200","!ChangeTactorState,1,2,200","!ChangeTactorState,1,3,200","!ChangeTactorState,1,4,200","!ChangeTactorState,1,5,200","!ChangeTactorState,1,6,200","!ChangeTactorState,1,7,200","!ChangeTactorState,1,8,200","!ChangeTactorState,1,9,200","!ChangeTactorState,1,10,200","!ChangeTactorState,1,11,200","!ChangeTactorState,1,12,200","!ChangeTactorState,1,13,200","!ChangeTactorState,1,14,200","!ChangeTactorState,1,15,200","!ChangeTactorState,1,0,0"]
##commandString = ["!ChangeTactorState,1,0,200","!ChangeTactorState,1,1,200","!ChangeTactorState,1,0,200","!ChangeTactorState,1,1,200","!ChangeTactorState,1,0,200","!ChangeTactorState,1,1,200","!ChangeTactorState,1,0,200","!ChangeTactorState,1,1,200","!ChangeTactorState,1,0,200","!ChangeTactorState,1,1,200","!ChangeTactorState,1,0,200","!ChangeTactorState,1,1,200","!ChangeTactorState,1,0,200","!ChangeTactorState,1,1,200","!ChangeTactorState,1,0,200","!ChangeTactorState,1,1,200","!ChangeTactorState,1,0,0"]


##
## Clear states.
##
if(s.sendto(commandoStart,addr)):
	print "sending: " + commandoStart
## Receive the result from the server ##
try:
	print "receiving: " + s.recvfrom(1024)[0] #1024 bytes for receiving buffer
except timeout:
	print "No response from server (correct commando?)"
y=0;
while (y<10000):
	print y
	for x in commandString:
		s.sendto(x,addr);
		s.sendto(commandoExecute,addr);
		
		time.sleep(0.180);
	y=y+1;
	
s.close()
