from __future__ import annotations

from typing import Optional, Tuple


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Wall:
    def __init__(self, pt_1: Point, pt_2: Point, w_type=None):
        """
        Define a Wall Object.

        :param pt_1:        Point object defining the beginning of the wall
        :param pt_2:        Point object defining the ending of the wall
        :param w_type:      type of wall: finger joint, tab slot

        other attributes:
        - super_direction:  vertical or horizontal
        - inter_wall_list:  list of IntersectionToWall objects that the wall contains

        the method will determine the super direction by comparing the 2 x coordinates
            and the 2 y coordinates.
        additionally, the method will ensure that the pt_1 attribute contains the Point
            object that has the smaller x coordinate if it is a horizontal wall or
            the smaller y coordinate if it is a vertical wall. Swapping pt_1 and pt_2
            if necessary.
        """
        self.type = w_type
        t1, t2 = pt_1, pt_2
        # check if the line is horizontal or vertical. If both x coords are equal then vertical
        if pt_1.x == pt_2.x:
            spr_dir = "vert"
            # make sure pt_1 is the point with the smaller y coordinate
            if pt_1.y > pt_2.y:
                pt_2, pt_1 = pt_1, pt_2
        # else if both y coords are equal then horizontal
        elif pt_1.y == pt_2.y:
            spr_dir = "horz"
            # make sure pt_1 is the point with the smaller x coordinate
            if pt_1.x > pt_2.x:
                pt_2, pt_1 = pt_1, pt_2
        else:
            raise ValueError(
                f"the line must be horizontal or vertical - given points ({t1.x}, {t1.y}) and ({t2.x}, {t2.y})."
            )
        self.super_direction = spr_dir
        self.pt_1 = pt_1
        self.pt_2 = pt_2
        self.inter_walL_list = []

    def intersect(self, other: Wall) -> Tuple[Optional[str], Optional[int]]:
        """
        Determine the intersection type if a given vertical wall intersects with a given horizontal wall.

        :param other:   the vertical wall
        :return:        the type of intersection: corner, cross, tee or None if the 2 walls do not intersect

        self is the horizontal wall.
        """
        horz = self
        horz_y = horz.pt_1.y
        vert = other
        vert_x = vert.pt_1.x
        # cross intersection
        if vert.pt_1.y < horz_y < vert.pt_2.y and horz.pt_1.x < vert_x < horz.pt_2.x:
            return "cross", None
        # corner intersection
        elif horz.pt_1.x == vert.pt_1.x and horz.pt_1.y == vert.pt_1.y:
            return "corner", 1
        elif horz.pt_1.x == vert.pt_2.x and horz.pt_1.y == vert.pt_2.y:
            return "corner", 2
        elif horz.pt_2.x == vert.pt_1.x and horz.pt_2.y == vert.pt_1.y:
            return "corner", 3
        elif horz.pt_2.x == vert.pt_2.x and horz.pt_2.y == vert.pt_2.y:
            return "corner", 4
        # tee intersection
        elif vert.pt_1.y == horz_y and horz.pt_1.x < vert_x < horz.pt_2.x:
            return "tee", 1
        elif vert.pt_2.y == horz_y and horz.pt_1.x < vert_x < horz.pt_2.x:
            return "tee", 2
        elif horz.pt_1.x == vert_x and vert.pt_1.y < horz_y < vert.pt_2.y:
            return "tee", 3
        elif horz.pt_2.x == vert_x and vert.pt_1.y < horz_y < vert.pt_2.y:
            return "tee", 4
        # walls do not intersect
        else:
            return None, None

class Intersection:
    def __init__(self):
        self.type = None
        self.pt = None
        self.inter_walL_dict = {'horz': None, 'vert': None}


class IntersectionToWall:
    def __init__(self):
        self.super_direction = None   # ???
        self.attrib = None
        self.wall = None
        self.intersection = None


def main():
    # cross intersection
    wh1 = Wall(Point(0,5), Point(10,5))
    wv2 = Wall(Point(5,0), Point(5,10))
    inter, nbr = wh1.intersect(wv2)

    # corner intersections
    wh1 = Wall(Point(0,0), Point(10,0))
    wv2 = Wall(Point(0,0), Point(0,10))
    inter, nbr = wh1.intersect(wv2)

    wh1 = Wall(Point(0,0), Point(10,0))
    wv2 = Wall(Point(10,0), Point(10,10))
    inter, nbr = wh1.intersect(wv2)

    wh1 = Wall(Point(0,10), Point(10,10))
    wv2 = Wall(Point(0,0), Point(0,10))
    inter, nbr = wh1.intersect(wv2)

    wh1 = Wall(Point(0,10), Point(10,10))
    wv2 = Wall(Point(10,0), Point(10,10))
    inter, nbr = wh1.intersect(wv2)

    # tee intersections
    wh1 = Wall(Point(0,5), Point(10,5))
    wv2 = Wall(Point(0,0), Point(0,10))
    inter, nbr = wh1.intersect(wv2)

    wh1 = Wall(Point(0,5), Point(10,5))
    wv2 = Wall(Point(10,0), Point(10,10))
    inter, nbr = wh1.intersect(wv2)

    wh1 = Wall(Point(0,0), Point(10,0))
    wv2 = Wall(Point(5,0), Point(5,10))
    inter, nbr = wh1.intersect(wv2)

    wh1 = Wall(Point(0,10), Point(10,10))
    wv2 = Wall(Point(5,0), Point(5,10))
    inter, nbr = wh1.intersect(wv2)

    print()


if __name__ == "__main__":
    main()
