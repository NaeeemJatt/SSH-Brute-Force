# report_generator.py
import pandas as pd # type: ignore

def generate_report(suspicious_files, suspicious_devices, report_file):
    with open(report_file, 'w') as f:
        f.write('--- Suspicious File Activities ---\n')
        if not suspicious_files.empty:
            f.write(suspicious_files.to_string(index=False))
        else:
            f.write('No suspicious file activities detected.\n')
        
        f.write('\n--- Suspicious USB Devices ---\n')
        if not suspicious_devices.empty:
            f.write(suspicious_devices.to_string(index=False))
        else:
            f.write('No suspicious USB devices detected.\n')
