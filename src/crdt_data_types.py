from dataclasses import dataclass
from itertools import islice


@dataclass
class WCharId:
    author: int
    clock: int

    def __lt__(self, other):
        if not isinstance(other, WCharId):
            return super().__lt__(other)
        if self.author < other.author:
            return True
        if self.author > other.author:
            return False
        return self.clock < other.clock


@dataclass
class WChar:
    id: WCharId
    char: str
    visible: bool
    prev_id: WCharId | None
    next_id: WCharId | None

class WString:

    BEG_ID = WCharId(-1, 0)
    END_ID = WCharId(-1, 1)


    def __init__(self):

        beg = WChar(
            id=WString.BEG_ID,
            char="",
            visible=False,
            prev_id=None,
            next_id=None
        )

        end = WChar(
            id=WString.END_ID,
            char="",
            visible=False,
            prev_id=None,
            next_id=None
        )

        beg.next_id = end.id
        end.prev_id = beg.id

        self.wchars: list[WChar] = [beg, end]


    def index(self, id: WCharId) -> int:
        return [i for i, c in enumerate(self.wchars) if c.id == id][0]


    def visible_index(self, id: WChar) -> int:
        return [i for i, vc in enumerate([c for c in self.wchars if c.visible]) if vc.id == id][0]


    def get(self, id: WCharId) -> WChar:
        return [c for c in self.wchars if c.id == id][0]
    

    def get_visible(self, i: int) -> WChar | None:
        if i < 0:
            return None
        visible = [c for c in self.wchars if c.visible]
        if i >= len(visible):
            return None
        return visible[i]


    def contains(self, id: WCharId) -> bool:
        return any(c.id == id for c in self.wchars)
    

    def insert(self, wchar: WChar, wchar_prev_id: WCharId, wchar_next_id: WCharId) -> None:

        prev_i = self.index(wchar_prev_id)
        next_i = self.index(wchar_next_id)

        if next_i - prev_i == 1:
            self.wchars.insert(next_i, wchar)
            return
        
        i = prev_i + 1
        while i < next_i:

            wchar_i = self.wchars[i]
            wchar_i_prev_i = self.index(wchar_i.prev_id)
            wchar_i_next_i = self.index(wchar_i.next_id)

            if wchar_i_prev_i > prev_i:
                i = i + 1
                continue
            if wchar_i_next_i < next_i:
                i = i + 1
                continue

            if not wchar_i.id < wchar.id:
                break

            i = i + 1
        
        wchar_i = self.wchars[i]
        wchar_i_m1 = self.wchars[i-1]
        
        print("========")
        print(f"{wchar_prev_id=} {wchar_next_id=}")
        print(f"{i=} {wchar_i.id=} {wchar_i_m1.id=}")

        self.insert(
            wchar=wchar,
            wchar_prev_id=wchar_i_m1.id,
            wchar_next_id=wchar_i.id
        )
    

    def delete(self, id: WCharId) -> None:
        wchar = self.get(id)
        wchar.visible = False
    

    def __str__(self) -> str:

        def rep_wchar(wchar: WChar):
            if not wchar.visible:
                return "   "
            return f"[{wchar.char}]"

        wchar_reps = list(map(rep_wchar, self.wchars))
        return "".join(wchar_reps)
