from dto_data_types import WCharDto
from crdt_data_types import WChar, WCharId


def dto_wchar_to_crdt_wchar(wchar: WCharDto):
    return WChar(
        id=wchar.id,
        char=wchar.char,
        visible=True,
        prev_id=wchar.prev_id,
        next_id=wchar.next_id
    )


def crdt_wchar_to_dto_wchar(wchar: WChar):
    return WCharDto(
        id=wchar.id,
        char=wchar.char,
        prev_id=wchar.prev_id,
        next_id=wchar.next_id
    )
