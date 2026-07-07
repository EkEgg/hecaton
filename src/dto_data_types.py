from dataclasses import dataclass
from crdt_data_types import WCharId

@dataclass
class MessageDto:
    sender_id: int
    type: str
    wchar: WCharDto | None = None
    wchar_id: WCharId | None = None


@dataclass
class WCharDto:
    id: WCharId
    char: str
    prev_id: WCharId
    next_id: WCharId
