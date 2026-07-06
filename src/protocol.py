from dto_data_types import MessageDto
from output import ProtocolOutput


class ProtocolCore:
    
    def __init__(self, output: ProtocolOutput):

        self.output = output
        node_count = len(output.nodes) + 1
        self.clock_vector = [0] * node_count

    def handle_messsage(self, message: MessageDto):
        if message.class_name == "INSERT":
            self._handle_insert(message)
        if message.class_name == "DELETE":
            self._handle_delete(message)

    def _handle_insert(message: MessageDto):
        print(message)

    def _handle_delete(message: MessageDto):
        print(message)