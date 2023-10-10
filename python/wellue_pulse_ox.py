import platform
from time import time
import numpy as np
import pygatt

CHUNK_SIZE = 5

class WelluePulseOx:
    def __init__(self, callback=None, time_func=time, name=None):
        self.address = None
        self.name = name
        self.callback = callback
        self.time_func = time_func

        if platform.system() == "Linux":
            self.backend = 'gatt'
        else:
            self.backend = 'bgapi'

    def connect(self):
        self.adapter = pygatt.GATTToolBackend(self.interface) if self.backend == 'gatt' else pygatt.BGAPIBackend()
        self.adapter.start()

        self.address = self.find_device_address(self.name)
        if not self.address:
            raise ValueError(f"Can't find Device {self.name}. Have you disconnected it from the other device?")

        print(f"Connecting to {self.name} with address {self.address}...")
        self.device = self.adapter.connect(self.address, address_type=pygatt.BLEAddressType.random, timeout=10)

        self._subscribe()
        print('Connected')

    def find_device_address(self, name=None):
        devices = {device['name']: device['address']
                   for device in self.adapter.scan(timeout=10.5)}
        return devices.get(name, None)

    def start(self):
        self._init_sample()
        print('Start streaming')

    def stop(self):
        print('Stop streaming')

    def disconnect(self):
        self.device.disconnect()
        self.adapter.stop()
        print('Disconnected')

    def _subscribe(self):
        self.device.subscribe("6E400003-B5A3-F393-E0A9-E50E24DCCA9E", callback=self._handle_data)
    
    def _init_sample(self):
        """initialize array to store the samples"""
        self.data = np.zeros((1, CHUNK_SIZE))

    def _handle_data(self, handle, data):
        timestamp = self.time_func()  # TODO: use the timestamp from the device

        # Check if data starts with the header and has the correct length
        if data.startswith(b'\xaaU\x0f\x07\x02') and len(data) >= 11:
            pleth_data = data[5:10]  # Skip the first 5 bytes and omit the last byte
            # Convert bytes to integers and print them as a list
            pleth_data_as_int = [int(b) for b in pleth_data]
            with open("pleth_data.txt", "a") as f:
                for i, b in enumerate(pleth_data_as_int):
                    if b > 127:
                        b = b - 128  # the first bit marks the R wave
                    f.write(f"{b} ")
                    self.data[0, i] = b

            self.callback(self.data)
            self._init_sample()
        
        # with open("packets.txt", "a") as f:
        #     raw_data = repr(data)[12:-2]
        #     f.write(f"{raw_data}\n")

        