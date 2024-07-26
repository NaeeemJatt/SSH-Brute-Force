# main.py
from usb_monitor import USBMonitor # type: ignore
from file_activity import FileActivityMonitor
from watchdog.observers import Observer # type: ignore
from threat_detection import detect_anomalies
from report_generator import generate_report
import time
import platform

def get_usb_mount_points():
    system = platform.system()
    if system == 'Windows':
        # Windows example mount points (adjust as needed)
        return ['E:\\', 'F:\\']
    elif system == 'Linux':
        # Linux example mount points (adjust as needed)
        return ['/media/username/usb0', '/mnt/usb0']
    else:
        raise NotImplementedError(f"Unsupported operating system: {system}")

def main():
    usb_log_file = 'usb_device_log.csv'
    file_activity_log_file = 'file_activity_log.csv'
    report_file = 'forensics_report.txt'

    # Initialize USB monitor and detect devices
    usb_monitor = USBMonitor()
    usb_monitor.detect_devices()
    usb_monitor.save_log(usb_log_file)

    # Initialize file activity monitor
    file_monitor = FileActivityMonitor()
    observer = Observer()
    
    # Monitor USB mount points
    usb_mount_points = get_usb_mount_points()
    for mount_point in usb_mount_points:
        observer.schedule(file_monitor, path=mount_point, recursive=True)
    
    observer.start()
    print("Monitoring file activity. Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(10)  # Adjust the sleep time as needed
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
    
    # Save file activity log
    file_monitor.save_log(file_activity_log_file)
    
    # Detect anomalies
    suspicious_files, suspicious_devices = detect_anomalies(file_activity_log_file, usb_log_file)
    
    # Generate report
    generate_report(suspicious_files, suspicious_devices, report_file)
    print(f'Report generated: {report_file}')

if __name__ == '__main__':
    main()
