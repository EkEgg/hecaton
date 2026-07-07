from dto_data_types import MessageDto
from crdt_data_types import WChar, WCharId, WString
from output import ProtocolOutput
from ui import ProtocolUi
from dto_crdt_mapping import dto_wchar_to_crdt_wchar, crdt_wchar_to_dto_wchar
from threading import Lock


class ProtocolCore:
    
    def __init__(self, node_id: int, output: ProtocolOutput, ui: ProtocolUi):
        self.output = output
        self.ui = ui
        self.id = node_id
        self.clock = 0
        self.wstring = WString()
        self.lock = Lock()


    def handle_message(self, message: MessageDto):

        if message.type == "INSERT":
            return self._handle_insert_message(message)
        if message.type == "DELETE":
            return self._handle_delete_message(message)
        
        return True

    def _handle_insert_message(self, message: MessageDto):

        wchar = dto_wchar_to_crdt_wchar(message.wchar)

        if not self.wstring.contains(wchar.prev_id):
            return False
        if not self.wstring.contains(wchar.next_id):
            return False
        
        self.wstring.insert(
            wchar=wchar,
            wchar_prev_id=wchar.prev_id,
            wchar_next_id=wchar.next_id
        )

        insert_visible_pos = self.wstring.visible_index(wchar.id)
        self.ui.signal_insert(insert_visible_pos, wchar.char)

        print(f"Handled remote insert: {wchar.id}")
        print(self.wstring)

        return True

    def _handle_delete_message(self, message: MessageDto):

        wchar_id = message.wchar_id

        if not self.wstring.contains(wchar_id):
            return False
        
        delete_visible_pos = self.wstring.visible_index(wchar_id)

        self.wstring.delete(wchar_id)

        self.ui.signal_delete(delete_visible_pos)

        print(f"Handled remote delete: {wchar_id}")
        print(self.wstring)

        return True
    
    def handle_local_insert(self, pos: int, text: str):

        if len(text) == 0:
            return

        if len(text) > 1:
            for i, char in enumerate(text):
                self.handle_local_insert(pos + i, char)
            return
        
        char = text

        self.clock = self.clock + 1

        prev = self.wstring.get_visible(pos - 1)
        if prev:
            prev_id = prev.id
        else:
            prev_id = self.wstring.BEG_ID

        next = self.wstring.get_visible(pos)
        if next:
            next_id = next.id
        else:
            next_id = self.wstring.END_ID

        wchar = WChar(
            id=WCharId(self.id, self.clock),
            char=char,
            visible=True,
            prev_id=prev_id,
            next_id=next_id
        )

        self.wstring.insert(wchar, prev_id, next_id)
        
        message = MessageDto(
            sender_id=self.id,
            type="INSERT",
            wchar=crdt_wchar_to_dto_wchar(wchar)
        )
        self.output.broadcast_message(message)

        print(f"Handled local insert: {pos} {char}")
        print(self.wstring)
    

    def handle_local_delete(self, pos: int, char_count: int):
        
        if char_count == 0:
            return
        
        if char_count > 1:
            i = char_count - 1
            while i >= 0:
                self.handle_local_delete(pos + i, 1)
                i = i - 1
            return
        
        wchar = self.wstring.get_visible(pos)
        self.wstring.delete(wchar.id)

        message = MessageDto(
            sender_id=self.id,
            type="DELETE",
            wchar_id=wchar.id
        )
        self.output.broadcast_message(message)

        print(f"Handled local delete: {pos}")
        print(self.wstring)
