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
import collections

import pandas as pd


# Global variables
WINDOW_SIZE = 140

reset_orient_flag = False
main_loop = True

# Sampling frequency (Hz)
fs = 60

# Cutoff frequency (Hz)
cutoff_freq = 10

# Normalize the cutoff frequency
nyquist_freq = 0.5 * fs
normalized_cutoff_freq = cutoff_freq / nyquist_freq

# Order of the filter
order = 4


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
    global main_loop
    global reset_orient_flag
    if key == keyboard.Key.esc:
        main_loop = False
    elif key == keyboard.Key.space:
        reset_orient_flag = True

def reset_orient():
    for device in deviceList:
        print(f"\nResetting heading to default for device {device.portInfo().bluetoothAddress()}: ", end="", flush=True)
        if device.resetOrientation(xsensdot_pc_sdk.XRM_DefaultAlignment):
            print("OK", end="", flush=True)
        else:
            print(f"NOK: {device.lastResultText()}", end="", flush=True)
    print("\n", end="", flush=True)


def maj_plot(acc, device, index):
    # reset the background back in the canvas state, screen unchanged
    fig.canvas.restore_region(bg)
    if device.deviceTagName() == "Shank":
        Acc_sk[0] = np.append(Acc_sk[0], acc[0])[1:]
        Acc_sk[1] = np.append(Acc_sk[1], acc[1])[1:]
        Acc_sk[2] = np.append(Acc_sk[2], acc[2])[1:]
        ln_sk_x.set_ydata(Acc_sk[0])
        ln_sk_y.set_ydata(Acc_sk[1])
        ln_sk_z.set_ydata(Acc_sk[2])
        new_df.loc[index, ['shank_x', 'shank_y', 'shank_z']] = acc
    elif device.deviceTagName() == "Thigh":
        np.delete(Acc_th, 0)
        Acc_th[0] = np.append(Acc_th[0], acc[0])[1:]
        Acc_th[1] = np.append(Acc_th[1], acc[1])[1:]
        Acc_th[2] = np.append(Acc_th[2], acc[2])[1:]
        ln_th_x.set_ydata(Acc_th[0])
        ln_th_y.set_ydata(Acc_th[1])
        ln_th_z.set_ydata(Acc_th[2])
        new_df.loc[index, ['thigh_x', 'thigh_y', 'thigh_z']] = acc
    elif device.deviceTagName() == "Trunk":
        np.delete(Acc_tk, 0)
        Acc_tk[0] = np.append(Acc_tk[0], acc[0])[1:]
        Acc_tk[1] = np.append(Acc_tk[1], acc[1])[1:]
        Acc_tk[2] = np.append(Acc_tk[2], acc[2])[1:]
        ln_tk_x.set_ydata(Acc_tk[0])
        ln_tk_y.set_ydata(Acc_tk[1])
        ln_tk_z.set_ydata(Acc_tk[2])
        new_df.loc[index, ['trunk_x', 'trunk_y', 'trunk_z']] = acc

    # redraw just the points
    sk_plot.draw_artist(ln_sk_x)
    sk_plot.draw_artist(ln_sk_y)
    sk_plot.draw_artist(ln_sk_z)
    th_plot.draw_artist(ln_th_x)
    th_plot.draw_artist(ln_th_y)
    th_plot.draw_artist(ln_th_z)
    tk_plot.draw_artist(ln_tk_x)
    tk_plot.draw_artist(ln_tk_y)
    tk_plot.draw_artist(ln_tk_z)

    # copy the image to the GUI state, but screen might not be changed yet
    fig.canvas.blit(fig.bbox)

    # flush any pending GUI events, re-painting the screen if needed
    fig.canvas.flush_events()


def update_data(index):
    if callback.packetsAvailable():
        new_df.loc[index, 'time'] = index/fs
        for device in deviceList:
            s = f"{device.deviceTagName()} \n"
            # Retrieve a packet
            packet = callback.getNextPacket(device.portInfo().bluetoothAddress())
            if packet.containsFreeAcceleration():
                acc = packet.freeAcceleration()
                s += f"Acc: X:{acc[0]:7.4f}, Y:{acc[1]:7.4f}, Z:{acc[2]:7.4f} \n"
                maj_plot(acc, device, index)
            print("%s" % s, flush=True)
        



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
    print("Wait until all IMUS are connected or wait 20 seconds to stop scanning...")
    connectedDOTCount = 0
    startTime = xsensdot_pc_sdk.XsTimeStamp_nowMs()
    while len(callback.getDetectedDots())<3 and not callback.errorReceived() and xsensdot_pc_sdk.XsTimeStamp_nowMs() - startTime <= 20000:
        time.sleep(0.1)
        nextCount = len(callback.getDetectedDots())
        if nextCount != connectedDOTCount:
            print(f"Number of connected DOTs: {nextCount}\r", end="", flush=True)
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
        s += f"{device.deviceTagName()}: Acc: X, Y, Z \t"
    print("%s" % s, flush=True)



    #PLOT
    fig, (sk_plot, th_plot, tk_plot) = plt.subplots(3, 1, figsize=(13, 7))

    Acc_sk = np.zeros((3, WINDOW_SIZE))
    Acc_th = np.zeros((3, WINDOW_SIZE))
    Acc_tk = np.zeros((3, WINDOW_SIZE))
    time_abs = np.arange(0, WINDOW_SIZE) / fs
    
    ln_sk_x, = sk_plot.plot(time_abs, Acc_sk[0, :], animated=True, label='acc_x')
    ln_sk_y, = sk_plot.plot(time_abs, Acc_sk[1, :], animated=True, label='acc_y')
    ln_sk_z, = sk_plot.plot(time_abs, Acc_sk[2, :], animated=True, label='acc_z')
    ln_th_x, = th_plot.plot(time_abs, Acc_th[0, :], animated=True, label='acc_x')
    ln_th_y, = th_plot.plot(time_abs, Acc_th[1, :], animated=True, label='acc_y')
    ln_th_z, = th_plot.plot(time_abs, Acc_th[2, :], animated=True, label='acc_z')
    ln_tk_x, = tk_plot.plot(time_abs, Acc_tk[0, :], animated=True, label='acc_x')
    ln_tk_y, = tk_plot.plot(time_abs, Acc_tk[1, :], animated=True, label='acc_y')
    ln_tk_z, = tk_plot.plot(time_abs, Acc_tk[2, :], animated=True, label='acc_z')

    # Set up plot parameters
    sk_plot.set_title('Shank Acceleration')
    sk_plot.set_xlabel('Time (s)')
    sk_plot.set_ylabel('Acceleration (m/s^2)')
    sk_plot.set_ylim(-20, 20)
    sk_plot.legend(loc='upper left')
    th_plot.set_title('Thigh Acceleration')
    th_plot.set_xlabel('Time (s)')
    th_plot.set_ylabel('Acceleration (m/s^2)')
    th_plot.set_ylim(-20, 20)
    th_plot.legend(loc='upper left')
    tk_plot.set_title('Trunk Acceleration')
    tk_plot.set_xlabel('Time (s)')
    tk_plot.set_ylabel('Acceleration (m/s^2)')
    tk_plot.set_ylim(-20, 20)
    tk_plot.legend(loc='upper left')

    # Set the title of the plotting window
    plt.gcf().canvas.set_window_title('Holo-Gait FoG Detection. Press any key to quit.')

    plt.tight_layout()

    # plt.show(block=False)
    plt.pause(0.5)
    # get copy of entire figure (everything inside fig.bbox) sans animated artist
    bg = fig.canvas.copy_from_bbox(fig.bbox)

    # draw the animated artist, this uses a cached renderer
    sk_plot.draw_artist(ln_sk_x)
    sk_plot.draw_artist(ln_sk_y)
    sk_plot.draw_artist(ln_sk_z)
    th_plot.draw_artist(ln_th_x)
    th_plot.draw_artist(ln_th_y)
    th_plot.draw_artist(ln_th_z)
    tk_plot.draw_artist(ln_tk_x)
    tk_plot.draw_artist(ln_tk_y)
    tk_plot.draw_artist(ln_tk_z)

    # show the result to the screen, this pushes the updated RGBA buffer from the
    # renderer to the GUI framework so you can see it
    fig.canvas.blit(fig.bbox)


    reset_orient()

    # Main loop
    print("Main loop. Press Esc to quit.", flush=True)
    cpt_meas = 0
    new_df = pd.DataFrame(columns=['time', 'shank_x', 'shank_y', 'shank_z', 'thigh_x', 'thigh_y', 'thigh_z', 'trunk_x', 'trunk_y', 'trunk_z'])
    while main_loop:
        update_data(cpt_meas)
        cpt_meas += 1

    print("\n-----------------------------------------", end="", flush=True)

    reset_orient()

    print("\nStopping measurement...")
    for device in deviceList:
        if not device.stopMeasurement():
            print("Failed to stop measurement.")
        if not device.disableLogging():
            print("Failed to disable logging.")

    print("Closing ports...")
    manager.close()
    print("Successful exit.")

    new_df.to_csv('IMU_data.csv', index=False)




