
#  Copyright (c) 2003-2022 Movella Technologies B.V. or subsidiaries worldwide.
#  All rights reserved.
#  
#  Redistribution and use in source and binary forms, with or without modification,
#  are permitted provided that the following conditions are met:
#  
#  1.	Redistributions of source code must retain the above copyright notice,
#  	this list of conditions and the following disclaimer.
#  
#  2.	Redistributions in binary form must reproduce the above copyright notice,
#  	this list of conditions and the following disclaimer in the documentation
#  	and/or other materials provided with the distribution.
#  
#  3.	Neither the names of the copyright holders nor the names of their contributors
#  	may be used to endorse or promote products derived from this software without
#  	specific prior written permission.
#  
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
#  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
#  THE COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
#  OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY OR
#  TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  

# Requires installation of the correct Xsens DOT PC SDK wheel through pip
# For example, for Python 3.9 on Windows 64 bit run the following command
# pip install xsensdot_pc_sdk-202x.x.x-cp39-none-win_amd64.whl

import time
from pynput import keyboard
from threading import Lock
import xsensdot_pc_sdk
from user_settings import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import collections

waitForConnections = True


class CallbackHandler(xsensdot_pc_sdk.XsDotCallback):
    def __init__(self, max_buffer_size=5):
        xsensdot_pc_sdk.XsDotCallback.__init__(self)
        self.m_detectedDots = list()
        self.m_errorReceived = False
        self.m_maxNumberOfPacketsInBuffer = max_buffer_size
        self.m_packetBuffer = collections.defaultdict(list)
        self.m_lock = Lock()

    def getDetectedDots(self):
        return self.m_detectedDots

    def errorReceived(self):
        return self.m_errorReceived

    def packetsAvailable(self):
        for dev in self.m_detectedDots:
            if self.packetAvailable(dev.bluetoothAddress()) == 0:
                return False
        return True

    def packetAvailable(self, bluetoothAddress):
        self.m_lock.acquire()
        res = len(self.m_packetBuffer[bluetoothAddress]) > 0
        self.m_lock.release()
        return res

    def getNextPacket(self, bluetoothAddress):
        if len(self.m_packetBuffer[bluetoothAddress]) == 0:
            return None
        self.m_lock.acquire()
        oldest_packet = xsensdot_pc_sdk.XsDataPacket(self.m_packetBuffer[bluetoothAddress].pop(0))
        self.m_lock.release()
        return oldest_packet

    def onAdvertisementFound(self, port_info):
        if not whitelist or port_info.bluetoothAddress() in whitelist:
            self.m_detectedDots.append(port_info)
        else:
            print(f"Ignoring {port_info.bluetoothAddress()}")

    def onBatteryUpdated(self, dev, batteryLevel, chargingStatus):
        print(dev.deviceTagName() + f" BatteryLevel: {batteryLevel} Charging status: {chargingStatus}")

    def onError(self, errorString):
        print(f"Error received: {errorString}")
        self.m_errorReceived = True

    def onLiveDataAvailable(self, dev, pack):
        self.m_lock.acquire()
        while len(self.m_packetBuffer[dev.portInfo().bluetoothAddress()]) >= self.m_maxNumberOfPacketsInBuffer:
            self.m_packetBuffer[dev.portInfo().bluetoothAddress()].pop()
        self.m_packetBuffer[dev.portInfo().bluetoothAddress()].append(xsensdot_pc_sdk.XsDataPacket(pack))
        self.m_lock.release()


def on_press(key):
    global waitForConnections
    waitForConnections = False

def maj_tab(dot_id, acc, device):
    if dot_id == 1:
        if len(accel1) != len(acc):
            print("Error in data length")
            exit(-1)
        for i in range(len(accel1)):
            accel1[i].popleft()
            accel1[i].append(acc[i])
        a1.cla()
        a1.set_title(device.deviceTagName())
        #a1.set_xlabel('Time')
        a1.set_ylabel('Acceleration (m/s²)', labelpad=-40)
        a1.tick_params(direction='in')
        for i in range(len(accel1)):
            if(i==0):
                a1.plot(accel1[i], label='aX')
            elif(i==1):
                a1.plot(accel1[i], label='aY')
            elif(i==2):
                a1.plot(accel1[i], label='aZ')
            """
            a1.scatter(len(accel1[i])-1, accel1[i][-1])
            a1.text(len(accel1[i])-1, accel1[i][-1]+2, "{:.2f}".format(accel1[i][-1]))
            """
            a1.set_ylim(-20, 20)
        a1.legend(loc='upper left')
    elif dot_id == 2:
        if len(accel2) != len(acc):
            print("Error in data length")
            exit(-1)
        for i in range(len(accel2)):
            accel2[i].popleft()
            accel2[i].append(acc[i])
        a2.cla()
        a2.set_title(device.deviceTagName())
        #a2.set_xlabel('Time')
        a2.set_ylabel('Acceleration (m/s²)', labelpad=-40)
        a2.tick_params(direction='in')
        for i in range(len(accel2)):
            if(i==0):
                a2.plot(accel2[i], label='aX')
            elif(i==1):
                a2.plot(accel2[i], label='aY')
            elif(i==2):
                a2.plot(accel2[i], label='aZ')
            """
            a2.scatter(len(accel2[i])-1, accel2[i][-1])
            a2.text(len(accel2[i])-1, accel2[i][-1]+2, "{:.2f}".format(accel2[i][-1]))
            """
            a2.set_ylim(-20, 20)
            
        a2.legend(loc='upper left')
    elif dot_id == 3:
        if len(accel3) != len(acc):
            print("Error in data length")
            exit(-1)
        for i in range(len(accel3)):
            accel3[i].popleft()
            accel3[i].append(acc[i])
        a3.cla()
        a3.set_title(device.deviceTagName())
        #a3.set_xlabel('Time')
        a3.set_ylabel('Acceleration (m/s²)', labelpad=-40)
        a3.tick_params(direction='in')
        for i in range(len(accel3)):
            if(i==0):
                a3.plot(accel3[i], label='aX')
            elif(i==1):
                a3.plot(accel3[i], label='aY')
            elif(i==2):
                a3.plot(accel3[i], label='aZ')
            """
            a3.scatter(len(accel3[i])-1, accel3[i][-1])
            a3.text(len(accel3[i])-1, accel3[i][-1]+2, "{:.2f}".format(accel3[i][-1]))
            """
            a3.set_ylim(-20, 20)
        a3.legend(loc='upper left')
    elif dot_id == 4:
        if len(accel4) != len(acc):
            print("Error in data length")
            exit(-1)
        for i in range(len(accel4)):
            accel4[i].popleft()
            accel4[i].append(acc[i])
        a4.cla()
        a4.set_title(device.deviceTagName())
        #a4.set_xlabel('Time')
        a4.set_ylabel('Acceleration (m/s²)', labelpad=-40)
        a4.tick_params(direction='in')
        for i in range(len(accel4)):
            if(i==0):
                a4.plot(accel4[i], label='aX')
            elif(i==1):
                a4.plot(accel4[i], label='aY')
            elif(i==2):
                a4.plot(accel4[i], label='aZ')
            """
            a4.scatter(len(accel4[i])-1, accel4[i][-1])
            a4.text(len(accel4[i])-1, accel4[i][-1]+2, "{:.2f}".format(accel4[i][-1]))
            """
            a4.set_ylim(-20, 20)
        a4.legend(loc='upper left')
    elif dot_id == 5:
        if len(accel5) != len(acc):
            print("Error in data length")
            exit(-1)
        for i in range(len(accel5)):
            accel5[i].popleft()
            accel5[i].append(acc[i])
        a5.cla()
        a5.set_title(device.deviceTagName())
        #a5.set_xlabel('Time')
        a5.set_ylabel('Acceleration (m/s²)', labelpad=-40)
        a5.tick_params(direction='in')
        for i in range(len(accel5)):
            if(i==0):
                a5.plot(accel5[i], label='aX')
            elif(i==1):
                a5.plot(accel5[i], label='aY')
            elif(i==2):
                a5.plot(accel5[i], label='aZ')
            """
            a5.scatter(len(accel5[i])-1, accel5[i][-1])
            a5.text(len(accel5[i])-1, accel5[i][-1]+2, "{:.2f}".format(accel5[i][-1]))
            """
            a5.set_ylim(-20, 20)
        a5.legend(loc='upper left')

def update_data(i):
    if callback.packetsAvailable():
        s = ""
        dot_id = 1
        for device in deviceList:
            # Retrieve a packet
            packet = callback.getNextPacket(device.portInfo().bluetoothAddress())
            if packet.containsFreeAcceleration():
                acc = packet.freeAcceleration()
                s += f"DOT:{dot_id}, Acc: X:{acc[0]:7.4f}, Y:{acc[1]:7.4f}, Z:{acc[2]:7.4f} \n"
                maj_tab(dot_id, acc, device)
                dot_id+=1
            """
            if packet.containsOrientation():
                euler = packet.orientationEuler()
                s += f"Roll:{euler.x():7.2f}, Pitch:{euler.y():7.2f}, Yaw:{euler.z():7.2f}| "
            """
        print("%s\r" % s, end="", flush=True)

    
    


if __name__ == "__main__":
    # Print SDK version
    version = xsensdot_pc_sdk.XsVersion()
    xsensdot_pc_sdk.xsdotsdkDllVersion(version)
    print(f"Using Xsens DOT SDK version: {version.toXsString()}")

    # Create connection manager
    manager = xsensdot_pc_sdk.XsDotConnectionManager()
    if manager is None:
        print("Manager could not be constructed, exiting.")
        exit(-1)

    # Create and attach callback handler to connection manager
    callback = CallbackHandler()
    manager.addXsDotCallbackHandler(callback)

    #IMU_addresses = ["D4:22:CD:00:34:17", "D4:22:CD:00:34:21", "D4:22:CD:00:33:1E", "D4:22:CD:00:31:ED", "D4:22:CD:00:31:7D"]
    
    # Start a scan and wait until we have found one or more DOT Devices
    print("Scanning for devices...")
    manager.enableDeviceDetection()

    # Setup the keyboard input listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    print("Press any key or wait 20 seconds to stop scanning...")
    connectedDOTCount = 0
    startTime = xsensdot_pc_sdk.XsTimeStamp_nowMs()
    while waitForConnections and not callback.errorReceived() and xsensdot_pc_sdk.XsTimeStamp_nowMs() - startTime <= 20000:
        time.sleep(0.1)

        nextCount = len(callback.getDetectedDots())
        if nextCount != connectedDOTCount:
            print(f"Number of connected DOTs: {nextCount}. Press any key to start.")
            connectedDOTCount = nextCount

    manager.disableDeviceDetection()
    print("Stopped scanning for devices.")

    if len(callback.getDetectedDots()) == 0:
        print("No Xsens DOT device(s) found. Aborting.")
        exit(-1)

    # Set the device tag name of a device
    
    deviceList = list()
    sequence_number = 0
    for portInfo in callback.getDetectedDots():
        address = portInfo.bluetoothAddress()

        print(f"Opening DOT with address: @ {address}")
        if not manager.openPort(portInfo):
            print(f"Connection to Device {address} failed, retrying...")
            print(f"Device {address} retry connected:")
            if not manager.openPort(portInfo):
                print(f"Could not open DOT. Reason: {manager.lastResultText()}")
                continue

        device = manager.device(portInfo.deviceId())
        if device is None:
            continue

        deviceList.append(device)
        print(f"Found a device with Tag: {device.deviceTagName()} @ address: {address}")

        filterProfiles = device.getAvailableFilterProfiles()
        print("Available filter profiles:")
        for f in filterProfiles:
            print(f.label())

        print(f"Current profile: {device.onboardFilterProfile().label()}")
        if device.setOnboardFilterProfile("General"):
            print("Successfully set profile to General")
        else:
            print("Setting filter profile failed!")

        print("Setting quaternion CSV output")
        device.setLogOptions(xsensdot_pc_sdk.XsLogOptions_Quaternion)

        logFileName = "logfile_" + device.deviceTagName().replace(' ', '_') + ".csv"
        print(f"Enable logging to: {logFileName}")
        if not device.enableLogging(logFileName):
            print(f"Failed to enable logging. Reason: {manager.lastResultText()}")

        print("Putting device into measurement mode.")
        if not device.startMeasurement(xsensdot_pc_sdk.XsPayloadMode_FreeAcceleration):
            print(f"Could not put device into measurement mode. Reason: {manager.lastResultText()}")
            continue

    print("\nMain loop. Recording data for 10 seconds.")
    print("-----------------------------------------")

    # First printing some headers so we see which data belongs to which device
    s = ""
    for device in deviceList:
        s += f"{device.portInfo().bluetoothAddress():42}"
    print("%s" % s, flush=True)

    # figure for real time plotting
    fig = plt.figure(figsize=(12,8), facecolor='#DEDEDE')
    a1 = plt.subplot2grid(shape=(2,6), loc=(0,0), colspan=2)
    a2 = plt.subplot2grid((2,6), (0,2), colspan=2)
    a3 = plt.subplot2grid((2,6), (0,4), colspan=2)
    a4 = plt.subplot2grid((2,6), (1,1), colspan=2)
    a5 = plt.subplot2grid((2,6), (1,3), colspan=2)

    a1.set_title('DOT 1')
    a1.set_facecolor('#EEEEEE')

    a2.set_title('DOT 2')
    a2.set_facecolor('#EEEEEE')

    a3.set_title('DOT 3')
    a3.set_facecolor('#EEEEEE')

    a4.set_title('DOT 4')
    a4.set_facecolor('#EEEEEE')

    a5.set_title('DOT 5')
    a5.set_facecolor('#EEEEEE')

    x_acc1 = collections.deque(np.zeros(100))
    y_acc1 = collections.deque(np.zeros(100))
    z_acc1 = collections.deque(np.zeros(100))

    x_acc2 = collections.deque(np.zeros(100))
    y_acc2 = collections.deque(np.zeros(100))
    z_acc2 = collections.deque(np.zeros(100))

    x_acc3 = collections.deque(np.zeros(100))
    y_acc3 = collections.deque(np.zeros(100))
    z_acc3 = collections.deque(np.zeros(100))

    x_acc4 = collections.deque(np.zeros(100))
    y_acc4 = collections.deque(np.zeros(100))
    z_acc4 = collections.deque(np.zeros(100))

    x_acc5 = collections.deque(np.zeros(100))
    y_acc5 = collections.deque(np.zeros(100))
    z_acc5 = collections.deque(np.zeros(100))

    accel1 = [x_acc1, y_acc1, z_acc1]
    accel2 = [x_acc2, y_acc2, z_acc2]
    accel3 = [x_acc3, y_acc3, z_acc3]
    accel4 = [x_acc4, y_acc4, z_acc4]
    accel5 = [x_acc5, y_acc5, z_acc5]
    temps = []
    #animated plotting
    ani = FuncAnimation(fig, update_data, interval=100)
    plt.show()
    """
    orientationResetDone = False
    
    if callback.packetsAvailable():
        s = ""
        for device in deviceList:
            # Retrieve a packet
            packet = callback.getNextPacket(device.portInfo().bluetoothAddress())
            if packet.containsFreeAcceleration():
                acc = packet.freeAcceleration()
                s += f"Acc: X:{acc[0]:7.4f}, Y:{acc[1]:7.4f}, Z:{acc[2]:7.4f}| "
                

            if packet.containsOrientation():
                euler = packet.orientationEuler()
                s += f"Roll:{euler.x():7.2f}, Pitch:{euler.y():7.2f}, Yaw:{euler.z():7.2f}| "

        print("%s\r" % s, end="", flush=True)
        
        if not orientationResetDone and xsensdot_pc_sdk.XsTimeStamp_nowMs() - startTime > 5000:
            for device in deviceList:
                print(f"\nResetting heading for device {device.portInfo().bluetoothAddress()}: ", end="", flush=True)
                if device.resetOrientation(xsensdot_pc_sdk.XRM_Heading):
                    print("OK", end="", flush=True)
                else:
                    print(f"NOK: {device.lastResultText()}", end="", flush=True)
            print("\n", end="", flush=True)
            orientationResetDone = True
        """
    print("\n-----------------------------------------", end="", flush=True)

    for device in deviceList:
        print(f"\nResetting heading to default for device {device.portInfo().bluetoothAddress()}: ", end="", flush=True)
        if device.resetOrientation(xsensdot_pc_sdk.XRM_DefaultAlignment):
            print("OK", end="", flush=True)
        else:
            print(f"NOK: {device.lastResultText()}", end="", flush=True)
    print("\n", end="", flush=True)

    print("\nStopping measurement...")
    for device in deviceList:
        if not device.stopMeasurement():
            print("Failed to stop measurement.")
        if not device.disableLogging():
            print("Failed to disable logging.")

    print("Closing ports...")
    manager.close()

    print("Successful exit.")




