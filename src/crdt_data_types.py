from dataclasses import dataclass


@dataclass
class WCharId:
    author: int
    clock: int

@dataclass
class WChar:
    id: WCharId
    char: str
    visible: bool
    previous_id: WCharId | None
    next_id: WCharId | None
