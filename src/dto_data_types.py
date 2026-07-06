from dataclasses import dataclass

@dataclass
class MessageDto:
    sender_id: int
    clock_vector: list[int]
    class_name: str
    wchar: WCharDto | None

@dataclass
class WCharDto:
    author_id: int
    author_clock: int
    char: str
    previous_author_id: int
    previous_author_clock: int
    next_author_id: int
    next_author_clock: int
