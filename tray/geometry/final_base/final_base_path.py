from tray.geometry.basic.point import Point
from tray.geometry.typed_base_path import FinalizableTypedBasePath
from tray.geometry.final_base.final_path_line import FinalPathLine
from tray.geometry.basic.path_oriented_mixin import PathOrientationMixin


class FinalBasePath(PathOrientationMixin, FinalizableTypedBasePath[FinalPathLine]):
    def __init__(self, start_point: Point[int] | None = None):
        super().__init__(start_point)
        # NOTE: Path.lines does not get populated until finalize() is called.
        # self.path_lines: list[FinalPathLine] = []

    def _make_line(self, p1: Point[int], p2: Point[int]) -> FinalPathLine:
        return FinalPathLine(p1, p2)
