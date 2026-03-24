from __future__ import annotations

from enum import Enum, IntEnum


class JointType(Enum):
    FS = "finger-space"
    TS = "tab-slot"
    CR = "cross"  # AKA dual-slot
    SM = "smooth"  # AKA no joint - the edge is smooth
    NONE = "none"  # not defined


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


class IntrxnType(Enum):
    NONE = "none"
    CORNER_LT = "corner-left_top"
    CORNER_LB = "corner-left_bottom"
    CORNER_RT = "corner-right_top"
    CORNER_RB = "corner-right_bottom"
    TEE_L = "tee-left"
    TEE_R = "tee-right"
    TEE_T = "tee-top"
    TEE_B = "tee-bottom"
    CROSS = "cross"
