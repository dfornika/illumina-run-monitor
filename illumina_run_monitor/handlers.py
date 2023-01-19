import json
import logging
import os

import requests

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class JsonLoggingEventHandler(FileSystemEventHandler):
    """Logs all the events captured."""

    def __init__(self, logger=None):
        super().__init__()

        self.logger = logger or logging.root

    def on_moved(self, event):
        super().on_moved(event)

        what = 'directory' if event.is_directory else 'file'
        self.logger.info(json.dumps(
            {
                "event_type": what + "_moved",
                "src_path": os.path.abspath(event.src_path),
                "dest_path": os.path.abspath(event.dest_path),
            }
        ))


    def on_created(self, event):
        super().on_created(event)

        what = 'directory' if event.is_directory else 'file'
        self.logger.info(json.dumps(
            {
                "event_type": what + "_created",
                "path": os.path.abspath(event.src_path),
            }
        ))


    def on_deleted(self, event):
        super().on_deleted(event)

        what = 'directory' if event.is_directory else 'file'
        self.logger.info(json.dumps(
            {
                "event_type": what + "_deleted",
                "path": os.path.abspath(event.src_path),
            }
        ))


    def on_modified(self, event):
        super().on_modified(event)

        what = 'directory' if event.is_directory else 'file'
        if what == 'file':
            self.logger.info(json.dumps(
                {
                    "event_type": "file_modified",
                    "path": os.path.abspath(event.src_path),
                }
            ))
        elif what == 'directory':
            pass


class HttpPostingEventHandler(FileSystemEventHandler):
    """POSTs all the events captured to the specified endpoint"""

    def __init__(self, endpoint):
        super().__init__()

        self.endpoint = endpoint

    def on_moved(self, event):
        super().on_moved(event)

        what = 'directory' if event.is_directory else 'file'
        post_data = {
            "event_type": what + "_moved",
            "src_path": os.path.abspath(event.src_path),
            "dest_path": os.path.abspath(event.dest_path),
        }
        requests.post(self.endpoint, json=post_data)

    def on_created(self, event):
        super().on_created(event)

        what = 'directory' if event.is_directory else 'file'
        post_data = {
            "event_type": what + "_created",
            "path": os.path.abspath(event.src_path),
        }
        requests.post(self.endpoint, json=post_data)

    def on_deleted(self, event):
        super().on_deleted(event)

        what = 'directory' if event.is_directory else 'file'
        post_data = {
            "event_type": what + "_deleted",
            "path": os.path.abspath(event.src_path),
        }
        requests.post(self.endpoint, json=post_data)

    def on_modified(self, event):
        super().on_modified(event)

        what = 'directory' if event.is_directory else 'file'
        if what == 'file':
            post_data = {
                "event_type": "file_modified",
                "path": os.path.abspath(event.src_path),
            }
            requests.post(self.endpoint, json=post_data)
        elif what == 'directory':
            pass
