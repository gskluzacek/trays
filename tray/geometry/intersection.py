from tray.geometry.basic.point import Point
from tray.geometry.types.tray import IntrxnType


class Intersection:
    def __init__(self, intrxn_pt: Point[int], intrxn_type: IntrxnType):
        self.intrxn_pt = intrxn_pt
        self.intrxn_type = intrxn_type

    def __repr__(self) -> str:
        return f"Intersection({self.intrxn_pt}, {self.intrxn_type})"

    def __str__(self) -> str:
        return f"Intersection type {self.intrxn_type} at {self.intrxn_pt}"
