from __future__ import annotations

from enum import Enum, IntEnum


class JointType(Enum):
    FS = "finger-space"
    TS = "tab-slot"
    CR = "cross"
    SM = "smooth"
    NONE = "none"


class WallType(IntEnum):
    def __new__(cls, value: int, label: str):
        obj = int.__new__(cls, value)  # create the enum member as an int
        obj._value_ = value
        obj._label_ = label
        return obj

    NONE = (0, "none")
    INTERIOR = (1, "interior")
    EXTERIOR = (2, "exterior")
    COMBO = (3, "combo")

    @property
    def label(self) -> str:
        return self._label_
