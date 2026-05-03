# Process of Constructing a Tray

## Overview

1. Create a Tray object.
2. Define the tray's base.
3. Add walls to the tray's base.
4. Add interior walls to the tray.
5. Validate the tray's walls
6. Classify the walls and add line breaks to the tray base's lines.
7. Create the trays's final base path by splitting the tray's base lines on the line breaks from step 6.
8. Generate the tray's walls segments paths.
9. Generate the tray's walls intersections.

## Step Details

### Step 1 - Create a Tray object

A `Tray` object is created with a list of column widths, a list of row heights, and the thickness of the
material used to construct the tray.

### Step 2 - Define the tray's base

We use the Tray class's `start_base`, `extend_base`, and `end_base` methods to define the list of `Point`
objects that form the path of the tray's base.

1. The tray's base contains a list of Line objects as well as a list of Point objects.
2. These tray methods perform various validations to ensure the path of the tray's base
   is constructed in a consistent manner and with the correct constraints applied.
3. `start_base` creates a Point object at the given coordinates, and then creates a Path object and initializes it
   with the starting point.
4. `extend_base` creates a Point object at the given coordinates and appends it tot the Path object's list of
   points.
5. `end_base` sets the Path object's orientation (clockwise or counterclockwise) and creates the list of Line
   objects from the path's points.

### Step 3 - Add walls to the tray's base

Next walls are added to the tray's base.

1. this is done either by calling the Tray class's `auto_generate_exterior_base_walls` method, which will add a wall
   for each edge of the tray's base.

2. or by calling the Tray class's `add_wall` method for each wall to be added.
    1. the method takes two tuples of coordinates as its parameters
    2. it validates the parameters & creates Point objects from the tuples
    3. it then creates and adds a Line object to tray's list of walls.

### Step 4 - Add interior walls to the tray

Any interior walls must be addded by calling `add_wall`

### Step 5 - Validate the tray's walls

Wall objects are then valiated to ensure there are no overlapping walls.

### Step 6 - Classify the walls and add line breaks to the tray base's lines

The Tray class's `classify_index_walls` is called

1. it determines if a given wall is an INERIOR (1), EXTERIOR (2) or COMBO (3) wall type.
    1. the given wall is compared to all the lines of the tray's base
    2. for each line (of the tray's base), `classify_wall` is called which returns the wall type when compared to
       the give line.
    3. the max wall type of all comparisons is the final wall type.

2. when it also detects and adds line breaks (Point objects) to the each of the Tray Base's Line objects.
    1. if the comparison between a given wall and a line is CONBO or EXTERIOR
    2. then we check if the wall has any overlap with the line.
    3. there could be 0, 1 or 2 points the wall that overlap with the line.
    4. for this purpose, we do not consider there to be overlap if only 1 endpoint of the wall exactly touches 1
       endpoint of the line.
    5. overlaping points are added to the line's list of line breaks.

### Step 7 - Create the trays's final base path

The Tray class's `split_path_lines` method is called. it:

1. creates a FinalBasePath object
2. loops over the tray base's lines
3. for each line it
    1. adds the line's first point to the FinalBasePath's list of points
    2. adds the line's line break points to the FinalBasePath's list of points
4. once the points from all lines have been added to the list of points
    1. FinalBasePath's path orientation is set
    2. and FinalBasePath's path lines are created from the points.

### Step 8 - Generate the tray's walls segments paths

Call `generate_walls_segments`

1. loops over the tray's walls
2. for the each wall, the following 3 steps are performed:
    1. collect the list of final path line endpoints that overlap with the wall's endpoints.
        1. it loops over the tray's base final path lines
        2. for the given wall, it checks if the current final path line overlaps with the wall.
        3. if it does, the final path line's endpoints that are strictly between the wall's endpoints are added to a
           list.
    2. bulid and assign the list of points to the wall's segment path points list.
        1. it sorts the list of points collected in step 1 accoring the the order of the wall's endpoints.
        2. it then adds the wall's endpoints to the list of points at the beginning and end of the list.
    3. build and assign the list of segment lines to the wall's segment path lines list.
        1. determines `WallType` of the wall's **first** segment path line.
        2. using the fisrt segment path line's WallType, it creates the list of segement path lines from the
           list of segment points assigning each segment path line the appropriate WallType.

### Step 9 - Generate the tray's walls intersections

Each wall and segment line has its own list of intersection. Walls neeed to know about every type of intersection,
while segment lines only need to know about the CROSS intersection type.

1. Create a cartesian product of the horizontal and vertical walls then iterate over each pair of walls
2. for each pair of walls (one horizontal and one vertical)
    1. check if the walls intersect
    2. if an intersection is found add it to both the3 horizontal and vertical wall's intersection lists.
    3. if the `IntrxnType` is `CROSS` then find the horizontal and vertical wall's segment lines that contain the
       intersection point
        1. for each of the wall's segment path's lines we check if the intersection point is on the segment line.
        2. the intersection point can either be 1) `OUTSIDE` the segment line, 2) `BETWEEN` the segment line's
           endpoints, 3)
           on the segment line's `P1` endpoint or 4) on the segment line's `P2` endpoint
        3. if the intersection point is BETWEEN, P1 or P2 then add the intersection to the segment line's intersection
           list
