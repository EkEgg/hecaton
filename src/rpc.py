import rpyc
import json
from dto_data_types import MessageDto
from input import ProtocolInput

class ProtocolRpcService(rpyc.Service):

    def __init__(self, input: ProtocolInput):
        self.input = input

    def on_connect(self, conn):
        pass

    def on_disconnect(self, conn):
        pass

    def dispose(self):
        self.input.dispose()

    def exposed_send_message(self, message_json) -> None:
        message = MessageDto(**json.loads(message_json))
        self.input.enqueue_message(message)
