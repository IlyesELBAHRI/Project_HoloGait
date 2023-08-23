#!/usr/bin/env python

# An Python example to demonstrate how to setup a UDP connection to the
# Elitac Communicator software and add tactor states tot a temporary patten.
#
# Use (write in terminal):
# >> python TactorStatesExample.py


from socket import *
import sys
import time
from itertools import cycle

## Setup socket ##
host = "127.0.0.1"
port = 50000
addr = (host, port)
s = socket(AF_INET, SOCK_DGRAM)
s.settimeout(1)  # 1sec timeout


## Get the commando to send ##
commandoStart = "!ClearTactorStates"
commando1 = "!ChangeTactorState,1,15,200"
commando2 = "!ChangeTactorState,2,15,200"
commandoExecute = "!ExecuteTactorStates"


##
## add first tactor state to the list.
##
if s.sendto(commando1.encode(), addr):
    print("sending: " + commando1)
## Receive the result from the server ##
try:
    print(f"receiving: {s.recvfrom(1024)[0]}")  # 1024 bytes for receiving buffer
except timeout:
    print("No response from server (correct commando?)")

##
## add second tactor state to the list.
##
if s.sendto(commando2.encode(), addr):
    print("sending: " + commando2)
## Receive the result from the server ##
try:
    print(f"receiving: {s.recvfrom(1024)[0]}")  # 1024 bytes for receiving buffer
except timeout:
    print("No response from server (correct commando?)")

##
## execute tactor states in list.
##
if s.sendto(commandoExecute.encode(), addr):
    print("sending: " + commandoExecute)
## Receive the result from the server ##
try:
    print(f"receiving: {s.recvfrom(1024)[0]}")  # 1024 bytes for receiving buffer
except timeout:
    print("No response from server (correct commando?)")

s.close()
