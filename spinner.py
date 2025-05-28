import itertools
import threading
import sys
import time
from contextlib import contextmanager  # Добавляем этот импорт

class Spinner:
    def __init__(self):
        self.spinner = itertools.cycle(['-', '/', '|', '\\'])
        self.stop_event = threading.Event()

    def spin(self):
        while not self.stop_event.is_set():
            sys.stdout.write(next(self.spinner))
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')

    def start(self, message=""):
        print(f"{message} ", end='')
        self.thread = threading.Thread(target=self.spin)
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()
        sys.stdout.write(' \b')
        sys.stdout.flush()

@contextmanager
def spinner_context(message=""):
    spinner = Spinner()
    spinner.start(message)
    try:
        yield
    finally:
        spinner.stop()
