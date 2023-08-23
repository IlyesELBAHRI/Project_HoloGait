import tkinter as tk
import socket
from PIL import Image, ImageTk

def send_message(command):
    # Send the command to the Hololens
    print("Sending command: " + command)
    try:
        client_socket.sendto(command.encode(), (hololens_ip, hololens_port))
        message_label.config(text="Sending command: " + command)
        print("Command sent successfully!")
        status_label.config(text="Command sent successfully!")

    except socket.error as e:
        print("Error sending command: " + str(e))
        status_label.config(text="Error sending command: " + str(e))
        # response_text.config(text="No response received")

def check_config_file():
    # Read the config file and send the "CUES" command if the file contains "1"
    with open("config.txt", "r") as f:
        config_value = f.read().strip()
        if config_value == "1":
            send_message("CUES")
            # Write "0" to the config file to indicate that the command has been sent
            with open("config.txt", "w") as f:
                f.write("0")

    # Call this function again after 1 second
    window.after(1000, check_config_file)

# Configuration of the Hololens IP address and port
hololens_ip = "192.168.1.102" # Hololens IP address (fix adress with ZyXEL router) 
#hololens_ip = "172.18.2.224" # Hololens IP address with PHV-Guest network (can change)
#hololens_ip = "172.18.3.108" # PC1 IP address for debugging on unity editor
hololens_port = 8080 # Hololens port

# Creation of the UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Creation of the GUI window
window = tk.Tk()
window.title("Send UDP message")
window.geometry("550x350")

# Creation of the list of commands
commands = [
    {"text": "FOG", "image": "fog.png"}, # show visual cues with eyetracking data
    {"text": "YES", "image": "yes.png"}, # send this if it is the floor at the beginning
    {"text": "NO", "image": "no.png"}, # send this if it is not the floor at the beginning
    {"text": "CUES", "image": "cues.png"}, # show the cue path
    {"text": "MESH", "image": "mesh.png"}, # show/hide the mesh (hide after finding the floor)
    {"text": "STOP", "image": "stop.png"}, # stop the course and show another environment
    {"text": "PARKOUR", "image": "parkour.png"}, # change the course
    {"text": "RESET", "image": "reset.png"}, # reset cues
    {"text": "RESTART", "image": "restart.png"}, # restart the scene
    {"text": "TYPE", "image": "type.png"}, # change type of cues
    {"text": "DOOR", "image": "door.png"}, # open the door

]

# Creation of the frames to hold the buttons
button_frames = []
for i in range(0, len(commands), 3):
    button_frame = tk.Frame(window)
    button_frame.pack()
    button_frames.append(button_frame)

# Creation of the command buttons
for i, command in enumerate(commands):
    image = Image.open(command["image"]).resize((15, 15))
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(button_frames[i//3], image=photo, text=" " +command["text"], compound="left")
    label.image = photo # type: ignore # Keep a reference to the image to prevent garbage collection
    label.config(width=80, height=20) # Set the size of the label
    label.pack(side="left", padx=5, pady=5)
    command_button = tk.Button(button_frames[i//3], text=command["text"], command=lambda c=command["text"]: send_message(c))
    command_button.pack(side="left", padx=5, pady=5)

# Creation of the label to display the sent message
message_label = tk.Label(window, text="")
message_label.pack()

# Creation of the label to display the status of the message
status_label = tk.Label(window, text="")
status_label.pack()

# Call the check_config_file function to start checking the config file
# check_config_file()

# Start the main loop of the GUI
window.mainloop()