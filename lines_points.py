"""
Here’s a concise analysis of lines_points.py focusing on behavior, correctness, and pitfalls.
It implements a point-in-polygon test using ray casting:
• Point.orientation computes the orientation of three points (cw/ccw/col).
• Line.intersect checks whether two line segments intersect (with collinearity checks).
• inside casts a horizontal ray from the test point to the right and counts intersections with polygon edges;
  odd count => inside. It also handles the “point lies on edge” case.

Key observations and issues:
• Line.intersect has two incorrect collinearity checks:
◦ elif o3 == 0 and elif o4 == 0 should compare to "col" (string), not 0. As written, those branches never trigger,
  so some edge cases are missed.
• Line.slope will raise ZeroDivisionError for vertical lines. It’s not used elsewhere, but it’s unsafe as written.
• inside builds the “ray to the right” using max_x = max([pt.x for pt in poly]) + 10. This works but is arbitrary;
  if coordinates are huge or if p is outside far to the right, it could miss intersections. A more robust ray is
  to use float("inf") conceptually or max_x + 1 with a guarantee you only need “beyond polygon bounds” and that
  p.x is left of it.
• The polygon is expected to be closed (poly.append(poly[0])). If the caller forgets, the last edge won’t be
  checked. There’s no guard for that.
• inside prints debug output (print(count) and “on segment”). That changes behavior in library usage and
  makes testing noisy.
• INT_MAX is unused; comment suggests it was intended for ray length.

Behavior summary:
• For typical polygons with the closing point appended, it should return True for interior points and False for
  exterior ones, with some inaccuracies near collinear edge cases because of the o3/o4 bug.
"""
from typing import List


# Define Infinite (Using INT_MAX
# caused overflow problems)
INT_MAX = 10000


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"[{self.x}, {self.y}]"

    def orientation(self, p2, p3):
        p1 = self
        val = ((p2.y - p1.y) * (p3.x - p2.x)) - ((p2.x - p1.x) * (p3.y - p2.y))

        if val > 0:
            return "cw"
        elif val < 0:
            return "ccw"
        else:
            return "col"


class Line:
    def __init__(self, p: Point, q: Point):
        self.p = p
        self.q = q

    def slope(
        self,
    ):
        return (self.q.y - self.p.y) / (self.q.x - self.p.x)

    def on_segment(self, r):
        """
        entry condition:
        points p & q make up the line (self)
        point r (a point) must be collinear with p, q
        that is points p, q and r must be collinear

        return true if rx is between px & py AND
            ry is between py and qy
        """
        p = self.p
        q = self.q
        if (
            (r.x <= max(p.x, q.x))
            and (r.x >= min(p.x, q.x))
            and (r.y <= max(p.y, q.y))
            and (r.y >= min(p.y, q.y))
        ):
            return True
        return False

    def intersect(self, other):
        p1 = self.p
        q1 = self.q
        p2 = other.p
        q2 = other.q

        o1 = p1.orientation(q1, p2)
        o2 = p1.orientation(q1, q2)
        o3 = p2.orientation(q2, p1)
        o4 = p2.orientation(q2, q1)

        if o1 != o2 and o3 != o4:
            return True
        elif o1 == "col" and self.on_segment(p2):
            return True
        elif o2 == "col" and self.on_segment(q2):
            return True
        elif o3 == 0 and other.on_segment(p1):
            return True
        elif o4 == 0 and other.on_segment(q1):
            return True
        else:
            return False


def inside(poly: List[Point], p: Point):
    if len(poly) < 3:
        raise Exception(
            f"the min number of points that can define a polygon is 3, you only passed {len(poly)}"
        )

    max_x = max([pt.x for pt in poly]) + 10
    max_rt = Point(max_x, p.y)
    line1 = Line(p, max_rt)

    count = 0
    for i, p1 in enumerate(poly[:-1], 1):
        p2 = poly[i]
        line2 = Line(p1, p2)
        if line1.intersect(line2):
            if p1.orientation(p, p2) == "col":
                on_seg = line1.on_segment(p)
                if on_seg:
                    print("on segment")
                else:
                    print("not on segment")
                return on_seg
            count += 1
    print(count)
    return count % 2 == 1


def main():
    poly: List[Point] = [
        Point(0, 0),
        Point(3, 0),
        Point(3, 4),
        Point(6, 4),
        Point(6, 2),
        Point(8, 2),
        Point(8, 0),
        Point(10, 0),
        Point(10, 3),
        Point(7, 3),
        Point(7, 6),
        Point(9, 6),
        Point(9, 4),
        Point(10, 4),
        Point(10, 10),
        Point(7, 10),
        Point(7, 8),
        Point(8, 8),
        Point(8, 9),
        Point(9, 9),
        Point(9, 7),
        Point(6, 7),
        Point(6, 10),
        Point(0, 10),
    ]
    poly.append(poly[0])

    check = [
        Point(2, 3),
        Point(4, 5),
        Point(8, 5),
        Point(8.5, 8.5),
        Point(6.5, 8.5),
        Point(1, 8.5),
    ]

    for point in check:
        v = inside(poly, point)
        print(point, v)


if __name__ == "__main__":
    main()
