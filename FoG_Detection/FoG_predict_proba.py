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
import scipy.signal as sig
import scipy.fftpack as fft
from scipy.signal import find_peaks
import collections

import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import HistGradientBoostingClassifier

import socket

UDP_IP_1 = "192.168.1.201" # Haptics IP 1
UDP_IP_2 = "192.168.1.202" # Haptics IP 2
HOLO_IP = "192.168.1.102" # Hololens IP address (fix adress with ZyXEL router)
UDP_PORT = 8080

sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Global variables
WINDOW_SIZE = 141
THRESHOLD = 0.55
COEFF_ACC = 570             # Coeff mult = (MAX_X_DATASET+MAX_Y_DATASET)/(max_x_imu+max_y_imu)
# Sampling frequency (Hz)
fs = 60
frequency_range = (0.1, 8)  # Plage de fréquences souhaitée en Hz
fft_frequencies = fft.rfftfreq(WINDOW_SIZE, d=1.0/fs)

reset_orient_flag = False
main_loop = True

# Load model
model = joblib.load('model/hgb_classifier.pkl')




Acc_sk = np.zeros((3, WINDOW_SIZE))
Acc_th = np.zeros((3, WINDOW_SIZE))
Acc_tk = np.zeros((3, WINDOW_SIZE))
FoG_prob = np.zeros(WINDOW_SIZE)
FoG_pred = np.zeros(WINDOW_SIZE)
FFT = np.zeros(WINDOW_SIZE)
time_abs = np.arange(0, WINDOW_SIZE) / fs
freq_abs = np.arange(0, WINDOW_SIZE) / WINDOW_SIZE * fs


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

def send_command(sock, ip, command):
    try:
        sock.sendto(command.encode(), (ip, UDP_PORT))
    except:
        pass


def vibrate_system(ip):
    frequency = 1.0
    command = f"V {frequency}"
    send_command(sock1, ip, command)

def stop_vibration(ip):
    command = "S"
    send_command(sock1, ip, command)

def visual_cues():
    command = "FOG"
    send_command(sock1, HOLO_IP, command)

def maj_acc(acc, device, index):
    if device.deviceTagName() == "Shank":
        np.delete(Acc_sk, 0)
        Acc_sk[0] = np.append(Acc_sk[0], acc[0]*COEFF_ACC)[1:]
        Acc_sk[1] = np.append(Acc_sk[1], acc[1]*COEFF_ACC)[1:]
        Acc_sk[2] = np.append(Acc_sk[2], acc[2]*COEFF_ACC)[1:]
        new_df.loc[index, ['shank_x', 'shank_y', 'shank_z']] = acc
    elif device.deviceTagName() == "Thigh":
        np.delete(Acc_th, 0)
        Acc_th[0] = np.append(Acc_th[0], acc[0]*COEFF_ACC)[1:]
        Acc_th[1] = np.append(Acc_th[1], acc[1]*COEFF_ACC)[1:]
        Acc_th[2] = np.append(Acc_th[2], acc[2]*COEFF_ACC)[1:]
        new_df.loc[index, ['thigh_x', 'thigh_y', 'thigh_z']] = acc
    elif device.deviceTagName() == "Trunk":
        np.delete(Acc_tk, 0)
        Acc_tk[0] = np.append(Acc_tk[0], acc[0]*COEFF_ACC)[1:]
        Acc_tk[1] = np.append(Acc_tk[1], acc[1]*COEFF_ACC)[1:]
        Acc_tk[2] = np.append(Acc_tk[2], acc[2]*COEFF_ACC)[1:]
        new_df.loc[index, ['trunk_x', 'trunk_y', 'trunk_z']] = acc

def predict(index, features):
    return model.predict_proba(np.array(features).reshape(1, -1))[0,1]

FoG_flag = 0
old_FoG_flag = 0
def maj_plot(prob, fft_xyz):
    global FoG_prob
    global FoG_pred
    global FoG_flag
    global old_FoG_flag

    # reset the background back in the canvas state, screen unchanged
    fig.canvas.restore_region(bg)

    # update the data
    np.delete(FoG_prob, 0)
    FoG_prob = np.append(FoG_prob, prob)[1:]
    FoG_prob_filtered = sig.savgol_filter(FoG_prob, (int) (WINDOW_SIZE/15), 3)
    np.delete(FoG_pred, 0)
    old_FoG_flag = FoG_flag
    FoG_flag = 1 if np.mean(FoG_prob_filtered[-(int)(WINDOW_SIZE/4):-1])>THRESHOLD else 0
    FoG_pred = np.append(FoG_pred, FoG_flag)[1:]
    if old_FoG_flag == 0 and FoG_flag == 1:
        vibrate_system(UDP_IP_1)
        vibrate_system(UDP_IP_2)
        visual_cues()
    elif old_FoG_flag == 1 and FoG_flag == 0:
        stop_vibration(UDP_IP_1)
        stop_vibration(UDP_IP_2)

    # update the plot
    ln_prob.set_ydata(FoG_prob_filtered*100)
    ln_pred.set_ydata(FoG_pred)
    #ln_fft.set_ydata(fft_xyz)

    # just draw the animated artist
    prob_plot.draw_artist(ln_prob)
    pred_plot.draw_artist(ln_pred)
    #fft_plot.draw_artist(ln_fft)

    # copy the image to the GUI state, but screen might not be changed yet
    fig.canvas.blit(fig.bbox)

    # flush any pending GUI events, re-painting the screen if needed
    fig.canvas.flush_events()


def update_data(index):
    if callback.packetsAvailable():
        new_df.loc[index, 'time'] = round(index/fs, 3)
        for device in deviceList:
            s = f"{device.deviceTagName()} \n"
            # Retrieve a packet
            packet = callback.getNextPacket(device.portInfo().bluetoothAddress())
            if packet.containsFreeAcceleration():
                acc = packet.freeAcceleration()
                s += f"Acc: X:{acc[0]:7.4f}, Y:{acc[1]:7.4f}, Z:{acc[2]:7.4f} \n"
                maj_acc(acc, device, index)
            print("%s" % s, flush=True)
        sk_xyz = np.sqrt(np.square(Acc_sk[0])+np.square(Acc_sk[1])+np.square(Acc_sk[2]))
        th_xyz = np.sqrt(np.square(Acc_th[0])+np.square(Acc_th[1])+np.square(Acc_th[2]))
        tk_xyz = np.sqrt(np.square(Acc_tk[0])+np.square(Acc_tk[1])+np.square(Acc_tk[2]))
        all_imu = np.sqrt(np.square(Acc_sk[0])+np.square(Acc_sk[1])+np.square(Acc_sk[2])+np.square(Acc_th[0])+np.square(Acc_th[1])+np.square(Acc_th[2])+np.square(Acc_tk[0])+np.square(Acc_tk[1])+np.square(Acc_tk[2]))
        fft_sk_xyz = fft.rfft(sk_xyz)
        fft_sk_xyz[(fft_frequencies < frequency_range[0]) | (fft_frequencies > frequency_range[1])] = 0
        fft_th_xyz = fft.rfft(th_xyz)
        fft_th_xyz[(fft_frequencies < frequency_range[0]) | (fft_frequencies > frequency_range[1])] = 0
        fft_tk_xyz = fft.rfft(tk_xyz)
        fft_tk_xyz[(fft_frequencies < frequency_range[0]) | (fft_frequencies > frequency_range[1])] = 0
        fft_all_imu = fft.rfft(all_imu)
        fft_all_imu[(fft_frequencies < frequency_range[0]) | (fft_frequencies > frequency_range[1])] = 0

        features_1 = []
        features_1.extend(extract_features(Acc_sk[0]))
        features_1.extend(extract_features(Acc_sk[1]))
        features_1.extend(extract_features(Acc_sk[2]))
        features_1.extend(extract_features(Acc_th[0]))
        features_1.extend(extract_features(Acc_th[1]))
        features_1.extend(extract_features(Acc_th[2]))
        features_1.extend(extract_features(Acc_tk[0]))
        features_1.extend(extract_features(Acc_tk[1]))
        features_1.extend(extract_features(Acc_tk[2]))
        
        features_2 = []
        features_2.extend(extract_features(sk_xyz))
        features_2.extend(extract_features(th_xyz))
        features_2.extend(extract_features(tk_xyz))

        features_3 = []
        features_3.extend(extract_features(all_imu))

        fft_features_1 = []
        fft_features_1.extend(extract_features(fft_sk_xyz))
        fft_features_1.extend(extract_features(fft_th_xyz))
        fft_features_1.extend(extract_features(fft_tk_xyz))

        fft_features_2 = []
        fft_features_2.extend(extract_features(fft_all_imu))

        features = []
        features.extend(features_1)
        features.extend(features_2)
        features.extend(features_3)
        features.extend(fft_features_1)
        features.extend(fft_features_2)

        pred = predict(index, features)
        new_df.loc[index, 'FoG_prob'] = pred

        # update the plot
        maj_plot(pred, fft_sk_xyz)



        

def extract_features(X):
    feat = []
    #mean
    feat.append(np.mean(X))
    #standard deviation
    feat.append(np.std(X))
    #median
    feat.append(np.median(X))
    #min
    feat.append(np.min(X))
    #max
    feat.append(np.max(X))
    # max-min diff
    #feat.append(np.max(X) - np.min(X))
    #average absolute deviation
    feat.append(np.mean(np.absolute(X - np.mean(X))))
    #root mean square
    feat.append(np.sqrt(np.mean(np.square(X))))
    #interquartile range
    feat.append(np.percentile(X, 75) - np.percentile(X, 25))
    #skewness
    feat.append(np.mean(np.power((X - np.mean(X)) / np.std(X), 3))) if np.std(X) != 0 else feat.append(0)
    #kurtosis
    feat.append(np.mean(np.power((X - np.mean(X)) / np.std(X), 4))) if np.std(X) != 0 else feat.append(0)
    #variance
    feat.append(np.var(X))
    """
    #median absolute deviation
    feat.append(np.median(np.absolute(X - np.median(X))))
    #average absolute difference
    feat.append(np.mean(np.absolute(np.diff(X))))
    #number of negative values
    feat.append(len(X[X < 0]))
    #number of positive values
    feat.append(len(X[X > 0]))
    #number of values above mean
    feat.append(len(X[X > np.mean(X)]))
    #number of peaks
    feat.append(len(find_peaks(X)[0]))
    #energy
    feat.append(np.sum(np.square(X)))
    #magnitude
    feat.append(np.linalg.norm(X))
    """
    return feat

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
   
    # First printing some headers so we see which data belongs to which device
    s = ""
    for device in deviceList:
        s += f"{device.deviceTagName()}: Acc: X, Y, Z \t"
    print("%s" % s, flush=True)



    #PLOT
    fig, (prob_plot, pred_plot) = plt.subplots(2, 1, figsize=(13, 7))
    #fig, (prob_plot, pred_plot, fft_plot) = plt.subplots(3, 1, figsize=(13, 7))


    # Create the lines for the plot
    ln_prob, = prob_plot.plot(time_abs, FoG_prob, 'r-', animated=True, label='FoG Probability')
    ln_pred, = pred_plot.plot(time_abs, FoG_pred, 'b-', animated=True, label='FoG Prediction')
    #ln_fft, = fft_plot.plot(freq_abs, FFT, 'g-', animated=True, label='FFT')

    # Set up plot parameters
    prob_plot.set_ylim(-5, 105)
    prob_plot.set_ylabel('Probability [%]')
    prob_plot.set_title('FoG Probability')

    pred_plot.set_ylim(-0.5, 1.5)
    pred_plot.set_ylabel('Prediction')
    pred_plot.set_title('FoG prob thresholded at {:.2f}'.format(THRESHOLD))

    """
    fft_plot.set_xlim(0, 10)
    fft_plot.set_ylim(-100000, 100000)
    fft_plot.set_xlabel('Frequency [Hz]')
    fft_plot.set_ylabel('Amplitude')
    fft_plot.set_title('FFT')
    """

    # Set the title of the plotting window
    #plt.gcf().canvas.set_window_title('Holo-Gait FoG Detection. Press ''Esc'' to quit.')

    plt.tight_layout()

    # plt.show(block=False)
    plt.pause(0.5)
    # get copy of entire figure (everything inside fig.bbox) sans animated artist
    bg = fig.canvas.copy_from_bbox(fig.bbox)

    # draw the animated artist, this uses a cached renderer
    prob_plot.draw_artist(ln_prob)
    pred_plot.draw_artist(ln_pred)
    #fft_plot.draw_artist(ln_fft)

    # show the result to the screen, this pushes the updated RGBA buffer from the
    # renderer to the GUI framework so you can see it
    fig.canvas.blit(fig.bbox)



    
    
    
    
    
    
    # Main loop
    print("Main loop. Press Esc to quit.", flush=True)
    cpt_meas = 0
    new_df = pd.DataFrame(columns=['time', 'shank_x', 'shank_y', 'shank_z', 'thigh_x', 'thigh_y', 'thigh_z', 'trunk_x', 'trunk_y', 'trunk_z', 'FoG_prob'])
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

    new_df.to_csv('2nd-trial.csv', index=False)