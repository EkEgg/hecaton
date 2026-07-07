import rpyc
import json
from dto_data_types import MessageDto, WCharDto
from crdt_data_types import WCharId
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
        if message.wchar is not None:
            message.wchar = WCharDto(**message.wchar)
            message.wchar.next_id = WCharId(**message.wchar.next_id)
            message.wchar.prev_id = WCharId(**message.wchar.prev_id)
        if message.wchar_id is not None:
            message.wchar_id = WCharId(**message.wchar_id)
        self.input.enqueue_message(message)
