import sys
import pandas as pd
import matplotlib.pyplot as plt
from math import ceil
import numpy as np


def mean_acc(data_imu):
    mean_acc = [
        (FreeAcc_X**2 + FreeAcc_Y**2 + FreeAcc_Z**2) ** 0.5
        for FreeAcc_X, FreeAcc_Y, FreeAcc_Z in zip(
            data_imu["Acc_X"], data_imu["Acc_Y"], data_imu["Acc_Z"]
        )
    ]

    return mean_acc


def get_data(num_imu):
    current_path = sys.path[0]
    csv_path = current_path + "/CSV"

    with open(f"{csv_path}/data_imu_{num_imu}.csv", "r") as f:
        data_imu = pd.read_csv(f)

    mean_acc_imu = mean_acc(data_imu)

    data_imu.drop(
        columns=[
            "PacketCounter",
            "Euler_X",
            "Euler_Y",
            "Euler_Z",
            "Acc_X",
            "Acc_Y",
            "Acc_Z",
            "Gyr_X",
            "Gyr_Y",
            "Gyr_Z",
        ],
        inplace=True,
    )

    data_imu["mean_acc"] = mean_acc_imu

    return data_imu


def sync(data_imu_1, data_imu_2):
    i = 0
    while data_imu_1["SampleTimeFine"][i] < data_imu_2["SampleTimeFine"][0]:
        data_imu_1.drop(i, inplace=True)
        i += 1

    data_imu_1.reset_index(drop=True, inplace=True)

    i = 0
    while data_imu_2["SampleTimeFine"][i] < data_imu_1["SampleTimeFine"][1]:
        data_imu_2.drop(i, inplace=True)
        i += 1

    data_imu_2.reset_index(drop=True, inplace=True)

    while len(data_imu_2) > len(data_imu_1):
        data_imu_2.drop(len(data_imu_2) - 1, inplace=True)

    while len(data_imu_1) > len(data_imu_2):
        data_imu_1.drop(len(data_imu_1) - 1, inplace=True)

    data_imu_1.reset_index(drop=True, inplace=True)
    data_imu_2.reset_index(drop=True, inplace=True)

    base_time = data_imu_1["SampleTimeFine"][0]

    time = [
        (data_imu_1["SampleTimeFine"][i] - base_time) * 10**-3
        for i in range(len(data_imu_1))
    ]

    data_imu_1.drop(columns=["SampleTimeFine"], inplace=True)
    data_imu_1["time"] = time

    data_imu_2.drop(columns=["SampleTimeFine"], inplace=True)
    data_imu_2["time"] = time

    return data_imu_1, data_imu_2


def derivative(data_imu_1, data_imu_2):
    data_imu_1["d_mean_acc"] = np.gradient(data_imu_1["mean_acc"])
    data_imu_2["d_mean_acc"] = np.gradient(data_imu_2["mean_acc"])

    for i in range(len(data_imu_1)):
        data_imu_1["d_mean_acc"][i] = np.floor(abs(data_imu_1["d_mean_acc"][i]))
        data_imu_2["d_mean_acc"][i] = np.floor(abs(data_imu_2["d_mean_acc"][i]))

    return data_imu_1, data_imu_2


def analyze(data_imu_1, data_imu_2):
    time_1 = 0
    time_2 = 0
    for time, d_mean_acc_1, d_mean_acc_2 in zip(
        data_imu_1["time"], data_imu_1["d_mean_acc"], data_imu_2["d_mean_acc"]
    ):
        if d_mean_acc_1 > 0 and time_1 == 0:
            time_1 = time

        if d_mean_acc_2 > 0 and time_2 == 0:
            time_2 = time

    return ceil(abs(time_1 - time_2))


if __name__ == "__main__":
    data_imu_1 = get_data(1)
    data_imu_2 = get_data(2)

    data_imu_1, data_imu_2 = sync(data_imu_1, data_imu_2)
    data_imu_1, data_imu_2 = derivative(data_imu_1, data_imu_2)

    plt.title("Mean Acceleration Gradient / Time")
    plt.xlabel("Time (ms)")
    plt.ylabel("Acceleration")
    plt.plot(data_imu_1["time"], data_imu_1["d_mean_acc"])
    plt.plot(data_imu_2["time"], data_imu_2["d_mean_acc"])
    plt.legend(["IMU 1", "IMU 2"])
    plt.text(
        0.18,
        0.95,
        f"Elapsed time: {analyze(data_imu_1, data_imu_2)} ms",
        horizontalalignment="center",
        verticalalignment="center",
        transform=plt.gca().transAxes,
    )
    plt.show()

    # latency = [300, 150, 234, 92, 159] Mean = 187 ms
