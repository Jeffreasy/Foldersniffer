import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from datetime import datetime
from queue import Queue
from threading import Thread

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, callback, queue_size=100):
        self.callback = callback
        self.queue = Queue(maxsize=queue_size)
        self.worker = Thread(target=self._process_queue)
        self.worker.daemon = True
        self.worker.start()

        # Dictionary to store previous file states
        self.previous_file_states = {}

    def on_any_event(self, event):
        if event.is_directory:
            return
        elif event.event_type in ['created', 'modified', 'deleted']:
            try:
                self.queue.put_nowait((event.event_type, event.src_path))
            except Queue.Full:
                pass  # Optionally, log this occurrence

    def _process_queue(self):
        while True:
            event_type, src_path = self.queue.get()
            file_info = self.get_file_info(event_type, src_path)
            self.callback(event_type, file_info)
            self.queue.task_done()

    def get_file_info(self, event_type, src_path):
        file_info = {
            'path': src_path,
            'type': 'file',
            'event_type': event_type,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        if event_type != 'deleted':
            try:
                current_state = {
                    'size': os.path.getsize(src_path),
                    'last_modified': os.path.getmtime(src_path),
                    'created': os.path.getctime(src_path),
                    'extension': os.path.splitext(src_path)[1].lower(),
                    'permissions': oct(os.stat(src_path).st_mode)[-3:]
                }

                if event_type == 'modified':
                    previous_state = self.previous_file_states.get(src_path, {})
                    modification_type = self.detect_modification_type(previous_state, current_state)
                    file_info['modification_type'] = modification_type

                # Update previous state
                self.previous_file_states[src_path] = current_state

                file_info.update(current_state)
                file_info['last_modified'] = time.ctime(file_info['last_modified'])
                file_info['created'] = time.ctime(file_info['created'])

            except OSError:
                # File might have been deleted or moved
                pass
        else:
            # Remove from previous states if deleted
            if src_path in self.previous_file_states:
                del self.previous_file_states[src_path]

        return file_info

    def detect_modification_type(self, previous_state, current_state):
        if not previous_state:
            return 'unknown modified'

        if previous_state['size'] != current_state['size']:
            return 'content modified'
        if previous_state['last_modified'] != current_state['last_modified']:
            return 'metadata modified'
        if previous_state['permissions'] != current_state['permissions']:
            return 'permission changed'
        
        return 'unknown modified'

class FileMonitor:
    def __init__(self, directory, callback):
        self.observer = Observer()
        event_handler = FileChangeHandler(callback)
        self.observer.schedule(event_handler, directory, recursive=True)

    def start(self):
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()
