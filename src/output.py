from dataclasses import dataclass
from queue import Queue, Empty
from dto_data_types import MessageDto
import rpyc
import threading
import json
import time


@dataclass
class NodeIdentification:
    id: int
    host: str
    port: int


class Node:

    def __init__(self, id, host, port):

        self.id = id
        self.host = host
        self.port = port

        self.connection = rpyc.connect(host, port)

        self.outgoing = Queue()
        self.worker_stop_event = threading.Event()

        self.worker_thread = threading.Thread(
            target=Node._work,
            args=(self, self.worker_stop_event, 0.1),
            daemon=True,
        )
        self.worker_thread.start()
    
    def dispose(self):
        self.worker_stop_event.set()
    
    def _work(node: Node, stop_event: threading.Event, poll_interval: float):

        while not stop_event.is_set():
            try:
                message = node.outgoing.get(timeout=poll_interval)
            except Empty:
                continue

            try:
                message_json = json.dumps(message.__dict__)
                node.connection.root.send_message(message_json)
            except Exception:
                node.outgoing.put(message)
                time.sleep(poll_interval)
            finally:
                node.outgoing.task_done()


class ProtocolOutput:

    nodes: dict[int, Node]

    def __init__(self, node_identifications: list[NodeIdentification]):
        nodes = {}
        for node_identification in node_identifications:
            nodes[node_identification.id] = Node(
                id=node_identification.id,
                host=node_identification.host,
                port=node_identification.port
            )
        self.nodes = nodes
    
    def enqueue_message(self, node_id: int, message: MessageDto):
        node = self.nodes[node_id]
        node.outgoing.put(message)

    def broadcast_message(self, message: MessageDto):
        for node in self.nodes.values():
            node.outgoing.put(message)

