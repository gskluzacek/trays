from tray.geometry.types.geometric import PathOrientation
from tray.geometry.basic.point import Point
from tray.geometry.typed_base_path import FinalizableTypedBasePath
from tray.geometry.base.path_line import PathLine
from tray.geometry.basic.path_oriented_mixin import PathOrientationMixin


class BasePath(PathOrientationMixin, FinalizableTypedBasePath[PathLine]):
    def __init__(self, start_point: Point[int] | None = None, orientation: PathOrientation = PathOrientation.NONE):
        super().__init__(start_point, orientation=orientation)
        # NOTE: Path.lines does not get populated until finalize() is called.
        # self.path_lines: list[PathLine] = []

    def _make_line(self, p1: Point[int], p2: Point[int]) -> PathLine:
        return PathLine(p1, p2)
