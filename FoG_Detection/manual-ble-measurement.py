import numpy as np
import asyncio
from bleak import BleakClient

measurement_characteristic_uuid = '15172001-4947-11e9-8646-d663bd873d93'
short_payload_characteristic_uuid = "15172004-4947-11e9-8646-d663bd873d93"
# 2004 -> short payload
medium_payload_characteristic_uuid = "15172003-4947-11e9-8646-d663bd873d93"
# 2003 -> medium payload

# Define the addresses and labels/names of the three Movella DOT devices
devices = [
    {"address": "d4:22:cd:00:31:7d", "name": "Trunk DOT"},
    {"address": "d4:22:cd:00:31:ed", "name": "Thigh DOT"},
    {"address": "d4:22:cd:00:33:1e", "name": "Shank DOT"}
]

def notification_callback(sender, data, device_name):
    print(f"{device_name}: {encode_free_acceleration(data)}")

def encode_free_acceleration(bytes_):
    # These bytes are grouped according to Movella's BLE specification doc
    data_segments = np.dtype([
        ('timestamp', np.uint32),
        ('x', np.float32),
        ('y', np.float32),
        ('z', np.float32),
        ('zero_padding', np.uint32)
    ])
    formatted_data = np.frombuffer(bytes_, dtype=data_segments)
    return formatted_data

def encode_acc_gyro(bytes_):
    # These bytes are grouped according to Movella's BLE specification doc
    data_segments = np.dtype([
        ('timestamp', np.uint32),
        ('acc_x', np.float32),
        ('acc_y', np.float32),
        ('acc_z', np.float32),
        ('zero_padding', np.uint32),
        ('gyro_x', np.float32),
        ('gyro_y', np.float32),
        ('gyro_z', np.float32),
        ('zero_padding', np.uint32)
    ])
    formatted_data = np.frombuffer(bytes_, dtype=data_segments)
    return formatted_data

async def stream_data(device):
    address = device["address"]
    name = device["name"]

    async with BleakClient(address) as client:
        # Check if connection was successful
        print(f"{name} - Client connection: {client.is_connected}")  # prints True or False

        # Subscribe to notifications from the Short Payload Characteristic
        await client.start_notify(short_payload_characteristic_uuid, lambda sender, data: notification_callback(sender, data, name))

        # Set and turn on the Free Acceleration measurement mode
        binary_message = b"\x01\x01\x06"  # last byte is the measurement mode
        await client.write_gatt_char(measurement_characteristic_uuid, binary_message, response=True)

        await asyncio.sleep(10.0)  # How long to stream data for

async def main():
    tasks = [stream_data(device) for device in devices]
    await asyncio.gather(*tasks)

asyncio.run(main())
