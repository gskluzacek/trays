# quick summary

looks like `main_5/main5.py` was the last working version and that the development for `main6.py` was in progress.
However it was not finished and is not in a working state.

## restarted development (again, lol)

`insider_diameter_test.py`: mainly used `main_5/main5.py` as a starting point as it was working, but did look at
`main6.py`
where improvements were made.

In January 2026, I started looking at the code again, but am taking a new approach of:

1. taking the column widths and row heights inputs as Inside Dimensions (id-dims)
2. previously the inputs were Center-To-Center Dimensions (c2c-dims)
3. we now convert the id-dims to c2c-dims
4. then from the c2c-dims we calculate the c2c-points
5. simplified the number of classes being used for points, lines and paths by using generics. this allows the same
   classes to be used for index points and cartesian-coordinate points.
6. attempting to move away from using the concept of aggregate points and instead use c2c-points only and derive the 8
   material-points (mat-points) as needed.

### definitions

- mat-point: Material Point, a point on the material used to define the walls of the compartment. There are 8 points:
    - top-left - exterior point
    - bottom-left - exterior point
    - top-right - exterior point
    - bottom-right - exterior point
    - top-center - interior point
    - bottom-center - interior point
    - left-center - interior point
    - right-center - interior point
- id-dim: Inside Dimension, the dimensions of the compartment, not including its walls.
- c2c-dim: Center-To-Center Dimension, the dimensions of the compartment from the center of each wall. Basically, the
  id-dim plus the wall thickness.
- c2c-point: Center-To-Center Point, typically the point where the center of a vertical wall intersects with the center
  of a horizontal wall.
    - The four exterior points and four interior points where the walls intersect can be derived from the c2c-point.
    - Typically, this is useful when two walls intersect, but the c2c-point can be used to determine these 8 points of
      the beginning/end of any wall, even if it does not intersect with another wall.

## Turtle Graphics

there are a few python modules that I wrote that have something to do with Turtle Graphics.

* my_turtle.py: this must have been a first attempt at using Turtle Graphics to output SVG files. Not very good or
  useful.
* my_turtle_2.py: this is a much better attempt, that has 2 example usages: main() and main1()
* svg_turtles.py: this code is based on my_turtle_2.py puts it into a module that can be imported and used by other
  modules. Though nothing currently does.

## kerf compensation

The concept of kerf compensation is important when cutting materials with cutting tool. The kerf is the width of the
cut, and it affects the final dimensions of the cut piece. To compensate for the kerf, the dimensions of the cut piece
need to be adjusted by adding the kerf width to the desired dimensions. This ensures that the final cut piece will be
the correct size.

for a path for a closed polygon, we need to determine the orientations (clockwise or counter-clockwise) of the ordered
points.

Additionally, if there are multiple paths nested inside one another (max depth of 1 as there cannot be any "islands"
only "holes", i.e., the whole of the part must be all connected), we need to determine if the polygon defined by the
path is an included part or excluded part of the overall cut piece.

steps to calculate the kerf compensated dimensions:

for each path:

1. determine if the orientation of the path is clockwise or counter-clockwise.
2. for each edge of the path, determine if the direction of the edge is north, south, east or west.
3. determine if the contour type of the path is an exterior contour (included part) or interior contour (excluded part)
   of the overall piece.
4. based on the orientation, edge direction and contour type, we can determine which axis (x or y) needs to be adjusted
   and whether the adjustment is positive or negative.

### path orientation

see the Path.set_orientation() method and the Point.orientation() method in inside_dimensions.py.

### edge direction

The directed edge has 2 points, P1, the starting point and P2, the ending point.

if the y-coordinate of the points are the same
if the x-coordinates are increasing (P2.x > P1.X) then the edge is north (N)
if the x-coordinates are decreasing (P2.x < P1.X) then the edge is south (S)
if the x-coordinates are the same
if the y-coordinates are increasing (P2.y > P1.Y) then the edge is east (E)
if the y-coordinates are decreasing (P2.y < P1.Y) then the edge is west (W)

### path contour type

1. pick a test point by taking the midpoint of an edge of the path.
2. adjust the midpoint so that it is inside the polygon formed by the path. use the orientation and direction of the
   edge to determine how to adjust the midpoint (x or y axis and positive or negative amount) so that it is inside the
   polygon.
3. for each path (other than the path being tested), determine if the test point is inside or outside the polygon formed
   by the path. ** need an algorithm to do this **
4. if the test point falls inside an even number of paths then it is an exterior contour, otherwise it is an interior
   contour.
5. this tells us if we need to if the kerf compensation adjustment needs to be outward (exterior contour) or inward (
   interior contour) of each edge of the path.

### lookup table

** really need to double-check these table **

| orientation | edge direction | contour type | inward axis | inward sign | outward axis | outward sign |
|-------------|----------------|--------------|-------------|-------------|--------------|--------------|
| CCW         | N              | exterior     | x           | -           | x            | +            |
| CCW         | S              | exterior     | x           | +           | x            | -            |
| CCW         | E              | exterior     | y           | -           | y            | +            |
| CCW         | W              | exterior     | y           | +           | y            | -            |

| orientation | edge direction | contour type | inward axis | inward sign | outward axis | outward sign |
|-------------|----------------|--------------|-------------|-------------|--------------|--------------|
| CCW         | N              | interior     | x           | +           | x            | -            |
| CCW         | S              | interior     | x           | -           | x            | +            |
| CCW         | E              | interior     | y           | +           | y            | -            |
| CCW         | W              | interior     | y           | -           | y            | +            |

| orientation | edge direction | contour type | inward axis | inward sign | outward axis | outward sign |
|-------------|----------------|--------------|-------------|-------------|--------------|--------------|
| CW          | N              | exterior     | x           | +           | x            | -            |
| CW          | S              | exterior     | x           | -           | x            | +            |
| CW          | E              | exterior     | y           | +           | y            | -            |
| CW          | W              | exterior     | y           | -           | y            | +            |

| orientation | edge direction | contour type | inward axis | inward sign | outward axis | outward sign |
|-------------|----------------|--------------|-------------|-------------|--------------|--------------|
| CW          | N              | interior     | x           | -           | x            | +            |
| CW          | S              | interior     | x           | +           | x            | -            |
| CW          | E              | interior     | y           | -           | y            | +            |
| CW          | W              | interior     | y           | +           | y            | -            |

## Mating Surfaces clearance adjustment

There are 2 kinds of surfaces

* cut surfaces: **CS** - this is the edge that is left after cutting the part of of the material. the edge (cut surface)
  will have the dimensions of the length of the cut by the thickness of the material. the length of the cut can be
  adjusted to allow a larger gap to make fitting the parts together easier.
* material surfaces **MS** - this is the face of the material. the face of the material cannot be adjusted, so we must
  adjust the dimensions of the cut surface to allow for the material to fit.

We must examine each surface type that is involved in the mate. This will involve at least 1 cut surface.

we need to apply clearance adjustments to mating surfaces using the rules below.

1. a cut surface mating with nothing - no adjustments are needed.
2. one pair of cut surfaces (2 cut surfaces total) mating with each other (1 cut surface on each part)
3. two pairs of cut surfaces (4 cut surfaces total) mating with each other ( 2 cut surfaces on each part)
4. one cut surface mating with one material surface (1 pair)
5. two pairs of: one cut surface mating with one material surface (2 pairs) - (total 2 opposing cut surfaces on the 1st
   part and 2 material surfaces on opposite sides of the 2nd part)

### T1: a cut surface mating with nothing

There is no need to adjust the mating surface clearance.

### T2: one pair of cut surfaces mating with each other

This use case is found when:

1. we have a `cross` intersection: the 2 cut surfaces between the short (length = material thickness) horizontal cuts (
   one on each wall forming the cross intersection)

### T3: two pairs of cut surfaces mating with each other

This use case is found when:

1. we have a `finger` / `space` joint where an exterior wall connects with the base
2. we have a `finger` / `space` joint where two walls meet at a `corner` intersection
3. we have a `tab` / `slot` joint where two walls meet at a `tee` intersection
4. we have a `tab` / `slot` joint where an interior wall connects with the base

### T4: one cut surface mating with one material surface

This use case is found when:

1. we have a `tab` / `slot` joint where two walls meet at a `tee` intersection
2. we have a `tab` / `slot` joint where an interior wall connects with the base

### T5: two pairs of one cut surface mating with one material surface

This use case is found when:

1. we have a `tab` / `slot` joint where two walls meet at a `tee` intersection
2. we have a `tab` / `slot` joint where an interior wall connects with the base
3. we have a `cross` intersection between the long vertical cuts surface and either side of the material surface.

## Or put another way:

### finger / space joints

1. wall corner intersection: T4 & T3
2. exterior wall base connection: T4 & T3

### tab / slot joints

1. wall tee intersection:
    1. wall -a- : T5 & T3
    2. wall -b- : T4 & T3
2. interior wall base connection:
    1. wall: T4 & T3
    2. base: T5 & T3

### dual slot joints

1. wall cross intersection:
    1. wall - upper slot - : T5 & T2
    2. wall - lower slot - : T5, T2 & T4 (???)

## joints, intersections & walls

* finger / space joints
* tab / slot joints
* dual slot joints

* corner intersection
* tee intersection
* cross intersection

* interior wall
* exterior wall
* combination wall (has both an interior portion and an exterior portion)

### usage

1. exterior walls use finger / space joints to connect to the base
2. interior walls use tab / slot joints to connect to the base
3. combination walls use both finger / space joints and tab / slot joints to connect to the base
    1. this can become a little complicated if there are 2 combination walls meeting at a cross intersection
    2. or if there is 1 combination wall meeting an exterior wall at a tee intersection
4. corner intersections between 2 walls use finger / space joints
5. tee intersections between 2 walls use tab / slot joints
6. cross intersections between 2 walls use dual slot joints

## classification of walls

walls can be classified into 3 categories:

* exterior walls
* interior walls
* combination walls

### use cases

1. both the 1st & 2nd points of the wall's line are contained within a path's line - inclusive of the start and end
   points of the path's line.
2. the first point of the wall's line 