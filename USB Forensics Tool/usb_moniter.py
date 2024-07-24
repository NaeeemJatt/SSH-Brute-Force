# usb_monitor.py
import usb.core
import usb.util
import pandas as pd
from datetime import datetime

class USBMonitor:
    def __init__(self):
        self.devices = []

    def detect_devices(self):
        self.devices = []
        for device in usb.core.find(find_all=True):
            device_info = {
                'Vendor ID': hex(device.idVendor),
                'Product ID': hex(device.idProduct),
                'Serial Number': usb.util.get_string(device, 256, device.iSerialNumber) if device.iSerialNumber else 'N/A',
                'Manufacturer': usb.util.get_string(device, 256, device.iManufacturer) if device.iManufacturer else 'N/A',
                'Product': usb.util.get_string(device, 256, device.iProduct) if device.iProduct else 'N/A',
                'Date Detected': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            self.devices.append(device_info)

    def save_log(self, log_file):
        df = pd.DataFrame(self.devices)
        df.to_csv(log_file, mode='a', header=False, index=False)
