import argparse
import json
import logging

from watchdog.observers import Observer

from .handlers import JsonLoggingEventHandler, HttpPostingEventHandler

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir')
    parser.add_argument('-e', '--endpoint')
    args = parser.parse_args()

    logging.basicConfig(
        format='{"timestamp": "%(asctime)s.%(msecs)03d", "message": %(message)s}',
        datefmt='%Y-%m-%dT%H:%M:%S',
        encoding='utf-8',
        level=logging.INFO,
    )

    if args.endpoint is None:
        event_handler = JsonLoggingEventHandler()
    else:
        event_handler = HttpPostingEventHandler(args.endpoint)
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
