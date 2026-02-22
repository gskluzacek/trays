from tray.geometry.basic.point import Point
from tray.geometry.basic.path import Path


class BasePoint(Point):
    def __init__(
        self,
        x,
        y,
    ):
        super().__init__(x, y)
        self._has_wall_ind = False


def main():
    wp1 = BasePoint(0, 0)
    wp2 = BasePoint(10, 0)
    wp3 = BasePoint(10, 10)
    wp4 = BasePoint(0, 10)

    p = Path()
    p.add_point(wp1)
    p.add_point(wp2)
    p.add_point(wp3)
    p.add_point(wp4)

    for line in p.lines:
        print(line)


if __name__ == "__main__":
    main()
