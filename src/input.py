import time
from queue import Queue, Empty
from dto_data_types import MessageDto
import threading
from protocol import ProtocolCore


class ProtocolInput:

    def __init__(self, core: ProtocolCore):

        self.core = core

        self.incoming = Queue[MessageDto]()

        self.new_message_event = threading.Event()
        self.stop_worker_event = threading.Event()
        self.thread = threading.Thread(
            target=ProtocolInput._work,
            args=(self, self.stop_worker_event, 0.1),
            daemon=True,
        )
        self.thread.start()

    def dispose(self):
        self.stop_worker_event.set()
        self.new_message_event.set()
    
    def enqueue_message(self, message: MessageDto):
        self.incoming.put(message)
        self.new_message_event.set()

    def _work(self, stop_event: threading.Event, poll_interval: float):
        while True:

            self.new_message_event.wait()
            self.new_message_event.clear()

            if stop_event.is_set():
                break

            message = self.incoming.get(timeout=poll_interval)
            print(f"Received message: {message}")
            with self.core.lock:
                self.core.handle_message(message)
                self.incoming.task_done()
