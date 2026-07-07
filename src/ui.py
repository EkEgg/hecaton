from abc import ABC, ABCMeta, abstractmethod
from PyQt6.QtCore import pyqtSignal, QObject


class ProtocolUi(ABC):

    insert_signal: pyqtSignal
    delete_signal: pyqtSignal

    @abstractmethod
    def signal_insert(self, pos: int, char: str):
        pass

    @abstractmethod
    def signal_delete(self, pos: int):
        pass


class QObjectProtocolUiMetaclass(type(QObject), ABCMeta):
    pass


class ProtocolPyQtUi(QObject, metaclass=QObjectProtocolUiMetaclass):

    insert_signal = pyqtSignal(int, str)
    delete_signal = pyqtSignal(int)

    def signal_insert(self, pos: int, char: str):
        self.insert_signal.emit(pos, char)

    def signal_delete(self, pos: int):
        self.delete_signal.emite(pos)
