import argparse
import json
import logging
import os

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir')
    args = parser.parse_args()

    logging.basicConfig(
        format='{"timestamp": "%(asctime)s.%(msecs)03d", "message": %(message)s}',
        datefmt='%Y-%m-%dT%H:%M:%S',
        encoding='utf-8',
        level=logging.INFO,
    )

    event_handler = JsonLoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, args.dir, recursive=True)
    observer.start()

    try:
        while observer.is_alive():
            observer.join(1)
    except KeyboardInterrupt as e:
        observer.stop()
        observer.join()
        exit()
    finally:
        observer.stop()
        observer.join()

if __name__ == '__main__':
    main()
