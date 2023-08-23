#!/usr/bin/env python

# An Python example to demonstrate how to setup a UDP connection to the
# Elitac Communicator software


from socket import *
import sys


## Setup socket ##
host = "127.0.0.1"
port = 50000
addr = (host, port)
s = socket(AF_INET, SOCK_DGRAM)
s.settimeout(1)  # 1sec timeout

## Get the commando to send ##
commando = [
    "?IsConnected",
    "?GetPatterns",
    "!PlayPattern,front",
    "!PlayPattern,front,circumferenceCoorOffset=256",
    "!PlayPattern,front,circumferenceCoorOffset=-256",
    "!PlayPattern,front,circumferenceCoorOffset=256,invertHorizontal=true",
    "!PlayPattern,left,invertHorizontal=true",
    "!PlayPattern,front,horizontalAngleOffset=90.0",
    "!PlayPattern,front,horizontalAngleOffset=-90.0",
    "!PlayPattern,front,displayID=2",
    "!PlayPattern,front,intensityIncrease=-8",
    "!PlayPattern,front,intensityIncrease=-13",
    "!PlayPattern,front,latitude=0.0,longitude=0.0",
    "!PlayPattern,front,compassAngle=0.0",
    "!PlayPattern,front,longitude=0.0",
    "!PlayPattern,front,latitude=0.0",
    "!PlayPattern,front,longitude=0.0,latitude=0.0,compassAngle=90.0",
    "!PlayPattern,front,test=1234",
]

for ii in commando:
    ## Send through UDP ##
    if s.sendto(ii.encode(), addr):
        print("sending: " + ii)

    ## Receive the result from the server ##
    try:
        print(f"receiving: {s.recvfrom(1024)[0]}")  # 1024 bytes for receiving buffer
    except timeout:
        print("No response from server (correct commando?)")
    input("> press any key to proceed")

s.close()
