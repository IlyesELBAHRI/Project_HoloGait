import tkinter as tk
import socket

UDP_IP_1 = "192.168.1.201"
UDP_IP_2 = "192.168.1.202"
UDP_PORT = 8080

sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_command(sock, ip, command):
    sock.sendto(command.encode(), (ip, UDP_PORT))


def vibrate_system(ip):
    frequency = frequency_entry.get()
    command = f"V {frequency}"
    send_command(sock1, ip, command)


def vibrate_tactors(ip):
    tactor_ids = tactor_ids_entry.get().split()
    frequency = frequency_entry.get()
    command = f"T {' '.join(tactor_ids)} {frequency}"
    send_command(sock2, ip, command)


def stop_vibration(ip):
    command = "S"
    send_command(sock2, ip, command)


window = tk.Tk()
window.title("Tactor Control")
window.geometry("300x300")

frequency_label = tk.Label(window, text="Frequency:")
frequency_label.pack()
frequency_entry = tk.Entry(window)
frequency_entry.pack()

vibrate_system_button_1 = tk.Button(
    window, text="Vibrate System 1", command=lambda: vibrate_system(UDP_IP_1)
)
vibrate_system_button_1.pack()

vibrate_system_button_2 = tk.Button(
    window, text="Vibrate System 2", command=lambda: vibrate_system(UDP_IP_2)
)
vibrate_system_button_2.pack()

tactor_ids_label = tk.Label(window, text="Tactor ID:")
tactor_ids_label.pack()
tactor_ids_entry = tk.Entry(window)
tactor_ids_entry.pack()

vibrate_tactors_button_1 = tk.Button(
    window, text="Vibrate Tactor 1", command=lambda: vibrate_tactors(UDP_IP_1)
)
vibrate_tactors_button_1.pack()

vibrate_tactors_button_2 = tk.Button(
    window, text="Vibrate Tactor 2", command=lambda: vibrate_tactors(UDP_IP_2)
)
vibrate_tactors_button_2.pack()

stop_vibration_button_1 = tk.Button(
    window, text="Stop Vibration 1", command=lambda: stop_vibration(UDP_IP_1)
)
stop_vibration_button_1.pack()

stop_vibration_button_2 = tk.Button(
    window, text="Stop Vibration 2", command=lambda: stop_vibration(UDP_IP_2)
)
stop_vibration_button_2.pack()

window.mainloop()
