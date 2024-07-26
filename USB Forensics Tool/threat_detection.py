# threat_detection.py
import pandas as pd # type: ignore

def detect_anomalies(file_activity_log, usb_device_log):
    file_df = pd.read_csv(file_activity_log)
    device_df = pd.read_csv(usb_device_log)

    # Example: Check for large file creations or deletions
    suspicious_files = file_df[(file_df['Activity Type'] == 'Created') & (file_df['Path'].str.contains('.exe|.dll'))]

    # Example: Detect unauthorized devices (you can define your own list of allowed devices)
    allowed_vendors = ['0x1234']  # Example Vendor ID
    suspicious_devices = device_df[~device_df['Vendor ID'].isin(allowed_vendors)]

    return suspicious_files, suspicious_devices
