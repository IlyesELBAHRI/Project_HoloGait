""" CODE FOR ONLY ONE IMU ON SACRUM (lower back) """
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

from scipy.fft import fft, fftfreq
from scipy.signal import windows, butter, lfilter

waitForConnections = True
# Sampling frequency (Hz)
fs = 60

# Cutoff frequency (Hz)
cutoff_freq = 10

# Normalize the cutoff frequency
nyquist_freq = 0.5 * fs
normalized_cutoff_freq = cutoff_freq / nyquist_freq

# Order of the filter
order = 4

# Compute the filter coefficients
b, a = butter(order, normalized_cutoff_freq, btype='low', analog=False)

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

# Function to apply the filter to the acceleration data
def apply_filter(accel_data):
    filtered_data = lfilter(b, a, accel_data)
    return filtered_data

def maj_tab(acc, device):
    global accel_globale
    if len(accel1) != len(acc):
        print("Error in data length")
        exit(-1)
    for i in range(len(accel1)):
        accel1[i].popleft()
        accel1[i].append(acc[i])
    #acc = apply_filter(acc)

    #offset = np.mean(accel_globale)
    accel_globale.popleft()
    accel_globale.append(np.sqrt(acc[0]**2 + acc[1]**2 + acc[2]**2))

    a1.cla()
    a1.set_title("Lower Back")
    #a1.set_xlabel('Time')
    a1.set_ylabel('Acceleration (m/s²)', labelpad=-40)
    a1.tick_params(direction='in')

    a2.cla()
    a2.set_title("Global Acceleration")
    a2.set_ylabel('Acceleration (m/s²)', labelpad=-40)
    a2.tick_params(direction='in')
    
    for i in range(len(accel1)):
        if(i==0):
            a1.plot(accel1[i], label='aX')
        elif(i==1):
            a1.plot(accel1[i], label='aY')
        elif(i==2):
            a1.plot(accel1[i], label='aZ')
        a1.set_ylim(-30, 30)
    a1.legend(loc='upper left')

    #plot global acceleration
    a2.plot(accel_globale)
    a2.set_ylim(-10, 30)

    #plot fft
    graph_fft = 20*np.log(np.abs(fft((accel_globale - np.mean(accel_globale))*fenetre)[:(int)(N_points/2)]))
    graph_fft *= freq_mask[:(int)(N_points/2)]
    ind_max = np.argmax(graph_fft)
    f0 = freq[ind_max]
    a_fft.cla()
    a_fft.set_title(f"FFT (f0 = {f0:.2f}Hz)")
    a_fft.set_xlabel('Frequency (Hz)')
    a_fft.set_ylabel('Amplitude', labelpad=-40)
    a_fft.tick_params(direction='in')
    a_fft.plot(freq[:(int)(N_points/2)],graph_fft)
    a_fft.set_xlim(0, 10)
    a_fft.set_ylim(-5, 100)

def update_data(i):
    if callback.packetsAvailable():
        s = ""
        for device in deviceList:
            # Retrieve a packet
            packet = callback.getNextPacket(device.portInfo().bluetoothAddress())
            if packet.containsFreeAcceleration():
                acc = packet.freeAcceleration()
                s += f"Acc: X:{acc[0]:7.4f}, Y:{acc[1]:7.4f}, Z:{acc[2]:7.4f} \n"
                print(acc)
                maj_tab(acc, device)
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
    
    # Start a scan and wait until we have found one or more DOT Devices
    print("Scanning for devices...")
    manager.enableDeviceDetection()

    # Setup the keyboard input listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    print("Press any key or wait 20 seconds to stop scanning...")
    connectedDOTCount = 0
    startTime = xsensdot_pc_sdk.XsTimeStamp_nowMs()
    while waitForConnections and len(callback.getDetectedDots())<1 and not callback.errorReceived() and xsensdot_pc_sdk.XsTimeStamp_nowMs() - startTime <= 20000:
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

        print("Putting device into measurement mode.")
        if not device.startMeasurement(xsensdot_pc_sdk.XsPayloadMode_FreeAcceleration):
            print(f"Could not put device into measurement mode. Reason: {manager.lastResultText()}")
            continue

    print("\nMain loop.")
    print("-----------------------------------------")

    # First printing some headers so we see which data belongs to which device
    s = ""
    for device in deviceList:
        s += f"{device.portInfo().bluetoothAddress():42}"
    print("%s" % s, flush=True)

    # figure for real time plotting
    fig = plt.figure(figsize=(12,8), facecolor='#DEDEDE')
    a1 = plt.subplot2grid(shape=(2,3), loc=(0,0),facecolor='#EEEEEE', colspan = 1)
    a2 = plt.subplot2grid(shape=(2,3), loc=(0,1),facecolor='#EEEEEE', colspan = 2)
    a_fft = plt.subplot2grid(shape=(2,3), loc=(1,0), facecolor='#EEEEEE', colspan=3)

    x_acc1 = collections.deque(np.zeros(100))
    y_acc1 = collections.deque(np.zeros(100))
    z_acc1 = collections.deque(np.zeros(100))

    N_points = 60
    accel_globale = collections.deque(np.zeros(N_points)) # set to have at least 5 periods of 0,5Hz
    freq = fftfreq(len(accel_globale), d=1/30) # 60Hz sampling frequency
    fenetre = windows.bartlett(len(accel_globale))
    freq_mask = freq <= 8       # 8Hz max frequency of gait
    accel1 = [x_acc1, y_acc1, z_acc1]
    temps = []
    #animated plotting
    ani = FuncAnimation(fig, update_data, interval=16.667)      # 16.66ms = 60Hz
    plt.show()


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




