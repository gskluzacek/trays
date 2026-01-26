# quick summary

looks like `main5.py` was the last working version and that the development for `main6.py` was in progress. However it was not finished and is not in a working state.

## restarted development (again, lol)

`insider_diameter_test.py`: mainly used `main5.py` as a starting point as it was working, but did look at `main6.py` where improvements were made.

In January 2026, I started looking at the code again, but am taking a new approach of:
1. taking the column widths and row heights inputs as Inside Dimensions (id-dims)
2. previously the inputs were Center-To-Center Dimensions (c2c-dims)
3. we now convert the id-dims to c2c-dims
4. then from the c2c-dims we calculate the c2c-points
5. simplified the number of classes being used for points, lines and paths by using generics. this allows the same classes to be used for index points and cartesian-coordinate points.
6. attempting to move away from using the concept of aggregate points and instead use c2c-points only and derive the 8 material-points (mat-points) as needed. 

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
- c2c-dim: Center-To-Center Dimension, the dimensions of the compartment from the center of each wall. Basically, the id-dim plus the wall thickness.
- c2c-point: Center-To-Center Point, typically the point where the center of a vertical wall intersects with the center of a horizontal wall.
  - The four exterior points and four interior points where the walls intersect can be derived from the c2c-point.
  - Typically, this is useful when two walls intersect, but the c2c-point can be used to determine these 8 points of the beginning/end of any wall, even if it does not intersect with another wall.
