# file_activity.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
from datetime import datetime

class FileActivityMonitor(FileSystemEventHandler):
    def __init__(self):
        self.activities = []
        
    def on_modified(self, event):
        self.record_activity('Modified', event.src_path)
        
    def on_created(self, event):
        self.record_activity('Created', event.src_path)
        
    def on_deleted(self, event):
        self.record_activity('Deleted', event.src_path)
        
    def on_moved(self, event):
        self.record_activity('Moved', event.dest_path)
        
    def record_activity(self, activity_type, path):
        self.activities.append({
            'Activity Type': activity_type,
            'Path': path,
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    def save_log(self, log_file):
        df = pd.DataFrame(self.activities)
        df.to_csv(log_file, mode='a', header=False, index=False)
