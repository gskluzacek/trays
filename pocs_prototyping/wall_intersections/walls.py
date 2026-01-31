from __future__ import annotations

from typing import Optional, Tuple


class Point:
    """
    Represents a 2D point with x and y coordinates.
    """

    def __init__(self, x, y):
        """
        Initialize a Point.

        :param x: The x-coordinate.
        :param y: The y-coordinate.
        """
        self.x = x
        self.y = y


class Wall:
    def __init__(self, pt_1: Point, pt_2: Point, w_type=None):
        """
        Define a Wall Object representing a straight segment that is either horizontal or vertical.

        :param pt_1:        Point object defining the beginning of the wall.
        :param pt_2:        Point object defining the ending of the wall.
        :param w_type:      Type of wall construction (e.g., finger joint, tab slot).

        Attributes:
        - type:             The construction type of the wall.
        - super_direction:  Orientation of the wall ("vert" for vertical, "horz" for horizontal).
        - pt_1:             Starting point, normalized to be the one with smaller x (for horz) or y (for vert).
        - pt_2:             Ending point, normalized to be the one with larger x (for horz) or y (for vert).
        - inter_walL_list:  List of IntersectionToWall objects associated with this wall.

        The constructor determines the orientation by comparing x and y coordinates.
        It enforces that walls must be strictly horizontal or vertical.
        It also normalizes the points so that pt_1 is always the 'minimum' point
        along the axis of orientation.
        """
        self.type = w_type
        t1, t2 = pt_1, pt_2
        # Determine orientation: if x coordinates are equal, it's a vertical wall.
        if pt_1.x == pt_2.x:
            spr_dir = "vert"
            # Normalize: ensure pt_1 has the smaller y coordinate.
            if pt_1.y > pt_2.y:
                pt_2, pt_1 = pt_1, pt_2
        # If y coordinates are equal, it's a horizontal wall.
        elif pt_1.y == pt_2.y:
            spr_dir = "horz"
            # Normalize: ensure pt_1 has the smaller x coordinate.
            if pt_1.x > pt_2.x:
                pt_2, pt_1 = pt_1, pt_2
        else:
            # Diagonal walls are currently not supported.
            raise ValueError(
                f"the line must be horizontal or vertical - given points ({t1.x}, {t1.y}) and ({t2.x}, {t2.y})."
            )
        self.super_direction = spr_dir
        self.pt_1 = pt_1
        self.pt_2 = pt_2
        self.inter_walL_list = []

    def intersect(self, other: Wall) -> Tuple[Optional[str], Optional[int]]:
        """
        Determine the intersection type between this wall (self) and another wall.
        Assumes self is a horizontal wall and 'other' is a vertical wall for standard calculation.

        :param other:   The vertical wall to check for intersection.
        :return:        A tuple (intersection_type, detail_code).
                        Types: 'cross', 'corner', 'tee', or (None, None) if no intersection.
                        Detail codes (1-4) specify which end or configuration of the intersection is met.

        Intersection Logic:
        - Cross: The vertical wall passes completely through the horizontal wall.
        - Corner: One end of the horizontal wall meets one end of the vertical wall.
        - Tee: One end of a wall meets the body of the other wall.
        """
        horz = self
        horz_y = horz.pt_1.y
        vert = other
        vert_x = vert.pt_1.x

        # Check for Cross Intersection:
        # Vertical wall must span across the horizontal wall's Y level,
        # and Horizontal wall must span across the vertical wall's X position.
        if vert.pt_1.y < horz_y < vert.pt_2.y and horz.pt_1.x < vert_x < horz.pt_2.x:
            return "cross", None

        # Check for Corner Intersections (4 possible configurations):
        # 1: Horz Start meets Vert Start
        elif horz.pt_1.x == vert.pt_1.x and horz.pt_1.y == vert.pt_1.y:
            return "corner", 1
        # 2: Horz Start meets Vert End
        elif horz.pt_1.x == vert.pt_2.x and horz.pt_1.y == vert.pt_2.y:
            return "corner", 2
        # 3: Horz End meets Vert Start
        elif horz.pt_2.x == vert.pt_1.x and horz.pt_2.y == vert.pt_1.y:
            return "corner", 3
        # 4: Horz End meets Vert End
        elif horz.pt_2.x == vert.pt_2.x and horz.pt_2.y == vert.pt_2.y:
            return "corner", 4

        # Check for Tee Intersections (4 possible configurations):
        # 1: Vert Start is on Horz body
        elif vert.pt_1.y == horz_y and horz.pt_1.x < vert_x < horz.pt_2.x:
            return "tee", 1
        # 2: Vert End is on Horz body
        elif vert.pt_2.y == horz_y and horz.pt_1.x < vert_x < horz.pt_2.x:
            return "tee", 2
        # 3: Horz Start is on Vert body
        elif horz.pt_1.x == vert_x and vert.pt_1.y < horz_y < vert.pt_2.y:
            return "tee", 3
        # 4: Horz End is on Vert body
        elif horz.pt_2.x == vert_x and vert.pt_1.y < horz_y < vert.pt_2.y:
            return "tee", 4

        # No intersection found.
        else:
            return None, None


class Intersection:
    """
    Represents an intersection point between two walls.
    """

    def __init__(self):
        """
        Initialize an Intersection.

        Attributes:
        - type: The type of intersection ('cross', 'corner', 'tee').
        - pt:   The Point where the intersection occurs.
        - inter_walL_dict: Maps 'horz' and 'vert' keys to the respective Wall objects.
        """
        self.type = None
        self.pt = None
        self.inter_walL_dict = {"horz": None, "vert": None}


class IntersectionToWall:
    """
    A mapping class that links an intersection to a specific wall,
    potentially holding attributes specific to that wall's participation in the intersection.
    """

    def __init__(self):
        """
        Initialize an IntersectionToWall object.
        """
        self.super_direction = None  # Direction of the wall in this context
        self.attrib = None  # Additional attributes or properties
        self.wall = None  # The Wall object
        self.intersection = None  # The Intersection object


def main():
    """
    Main function to demonstrate and test wall intersection logic.
    """
    # Test case: Cross intersection
    # wh1: horizontal (0,5) to (10,5)
    # wv2: vertical (5,0) to (5,10)
    wh1 = Wall(Point(0, 5), Point(10, 5))
    wv2 = Wall(Point(5, 0), Point(5, 10))
    inter, nbr = wh1.intersect(wv2)
    # Expected: ('cross', None)

    # Test cases: Corner intersections
    # Bottom-left corner
    wh1 = Wall(Point(0, 0), Point(10, 0))
    wv2 = Wall(Point(0, 0), Point(0, 10))
    inter, nbr = wh1.intersect(wv2)
    # Expected: ('corner', 1)

    # Bottom-right corner
    wh1 = Wall(Point(0, 0), Point(10, 0))
    wv2 = Wall(Point(10, 0), Point(10, 10))
    inter, nbr = wh1.intersect(wv2)
    # Expected: ('corner', 3)

    # Top-left corner
    wh1 = Wall(Point(0, 10), Point(10, 10))
    wv2 = Wall(Point(0, 0), Point(0, 10))
    inter, nbr = wh1.intersect(wv2)
    # Expected: ('corner', 2)

    # Top-right corner
    wh1 = Wall(Point(0, 10), Point(10, 10))
    wv2 = Wall(Point(10, 0), Point(10, 10))
    inter, nbr = wh1.intersect(wv2)
    # Expected: ('corner', 4)

    # Test cases: Tee intersections
    # Vertical wall starts on horizontal wall (bottom tee)
    wh1 = Wall(Point(0, 5), Point(10, 5))
    wv2 = Wall(Point(0, 0), Point(0, 10))  # This is actually a corner if at start/end,
    # but here the logic is tested.
    # Wait, (0,0)-(0,10) with (0,5)-(10,5) is a tee.
    # horz_x: 0, 10; vert_x: 0.
    # horz_y: 5; vert_y: 0, 10.
    # horz.pt_1.x == vert_x (0 == 0) and vert.pt_1.y < horz_y < vert.pt_2.y (0 < 5 < 10)
    # Matches case 3: "tee", 3
    inter, nbr = wh1.intersect(wv2)

    # Vertical wall ends on horizontal wall (top tee)
    wh1 = Wall(Point(0, 5), Point(10, 5))
    wv2 = Wall(Point(10, 0), Point(10, 10))
    inter, nbr = wh1.intersect(wv2)
    # Matches case 4: "tee", 4

    # Horizontal wall starts on vertical wall (left tee)
    wh1 = Wall(Point(0, 0), Point(10, 0))
    wv2 = Wall(Point(5, 0), Point(5, 10))
    inter, nbr = wh1.intersect(wv2)
    # Matches case 1: "tee", 1

    # Horizontal wall ends on vertical wall (right tee)
    wh1 = Wall(Point(0, 10), Point(10, 10))
    wv2 = Wall(Point(5, 0), Point(5, 10))
    inter, nbr = wh1.intersect(wv2)
    # Matches case 2: "tee", 2

    print("Intersections tested.")


if __name__ == "__main__":
    main()
