from ui import ProtocolUi
from protocol import ProtocolCore
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QPlainTextEdit

class DemoTextEditor(QPlainTextEdit):


    def __init__(self, protocol_core: ProtocolCore, protocol_ui: ProtocolUi, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self._prev_text = self.toPlainText()
        self.document().contentsChange.connect(self._on_contents_change)

        self.protocol_core = protocol_core
        protocol_ui.insert_signal.connect(self._handle_protocol_insert_signal)
        protocol_ui.delete_signal.connect(self._handle_protocol_delete_signal)
    

    @pyqtSlot(int, str)
    def _handle_protocol_insert_signal(self, pos: int, char: str):
        cursor = self.textCursor()
        cursor.setPosition(pos)
        cursor.insertText(char)

    
    @pyqtSlot(int)
    def _handle_protocol_delete_signal(self, pos):
        cursor = self.textCursor()
        cursor.setPosition(pos)
        cursor.deleteChar()


    def _on_contents_change(self, position, chars_removed, chars_added):
        new_text = self.toPlainText()

        if chars_removed:
            print(f"DELETE: {position} to {position + chars_removed}")
            with self.protocol_core.lock:
                self.protocol_core.handle_local_delete(position, chars_removed)

        if chars_added:
            text = new_text[position:position + chars_added]
            print(f"INSERT: {position} gets {text}")
            with self.protocol_core.lock:
                self.protocol_core.handle_local_insert(position, text)

        self._prev_text = new_text



    