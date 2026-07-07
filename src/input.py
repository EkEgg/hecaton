import time
from queue import Queue, Empty
from dto_data_types import MessageDto
import threading
from protocol import ProtocolCore


class ProtocolInput:

    def __init__(self, core: ProtocolCore):

        self.core = core

        self.incoming = Queue[MessageDto]()

        self.stop_worker_event = threading.Event()
        self.thread = threading.Thread(
            target=ProtocolInput._work,
            args=(self, self.stop_worker_event, 0.1),
            daemon=True,
        )
        self.thread.start()

    def dispose(self):
        self.stop_worker_event.set()
    
    def enqueue_message(self, message: MessageDto):
        self.incoming.put(message)

    def _work(self, stop_event: threading.Event, poll_interval: float):
        while not stop_event.is_set():
            try:
                message = self.incoming.get(timeout=poll_interval)
            except Empty:
                continue
            try:
                with self.core.lock:
                    self.core.handle_message(message)
            except Exception:
                self.incoming.put(message)
                time.sleep(poll_interval)
            finally:
                self.incoming.task_done()
