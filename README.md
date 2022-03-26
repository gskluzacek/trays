# Tray - a Work In Progress

This is the Trays project... 

It was born becuase my wife asked for a new silverware draw TRAY and I had a laser cutter AND I was tiered of modeling in Fusin 360 everytime I wanted to change something.

## Defining a tray is meant to be "simple"

1. The first step is to define the overall parameters
2. Then define the path of the base (most likely a rectangle) 
3. Then define the locations of the walls.  

### Overall Parameters

For example (all measurements are in milimeters)

* mat_thick=3,
* fngr_len=20.0,
* spc_len=10.0,
* min_be_len=10.0,
* col_widths=[50, 50, 50, 50, 100],
* row_heights=[125, 50, 100],
* min_tbslt_len=50,
* max_tbslt_bt_xs=2,
* wall_tbslt_dist=10,
* depth=50,

The above says that I'm building the tray out of 3 mm material.

For the edge joints on the base, to use a finger length of 20 mm and a space length of 10. The minimum amount of sapce at the beginning and ending of an edge joint is 10 mm.

For joints on the interior of the base, the minimum tab/slot length is 50 mm with a 2 tabs/slots between intersections. Tabs/slots should start 10 mm away from walls.

The wall of the tray should be 50 mm tall.

Finally, the tray will have 5 columns and 3 rows. With the columns having the following width: 50 mm, 50 mm, 50 mm, 50 mm and 100 mm. And the rows will have a hight of 125 mm, 50 mm and 100 mm.

### Base Path

Instead of defining the dimensions of base of the tray in terms of absolute lengths (i.e., in milimeters), you specify the path in terms column and row coordinates.

For example, with the columns and row widths/heights given above, we would specify the path that forms the outline of the base as:

start at point 0, 0 then draw a horizontal line to point 5,0 then draw a vertical line to point 5, 5, then a horizontal line to point 0, 5 and then finally close the path of the polygon.

* base.start_path(0, 0)
* base.extend_path(5, 0)
* base.extend_path(5, 5)
* base.extend_path(0, 5)
* base.end_path()

This lets us form a closed polygon of any shape to be as for the base.

### Wall Locations

The location for the walls of the tray are defined in a similar manner as the path for the base. The system autmatically creates all exterior walls based on the path of the base so the user does not need to specify these.

Continuing with our example above. We want 4 compartments that are 125 long and 50 mm wide. These 4 compartments start from the upper left and use 4 out the 5 columns that we specified. The last remaining compartment along the top edge will be 300 mm long and 100 mm wide. We will use three vertical walls of 125 and one vertical wall of 300 mm to form these compartments. 

* base.add_wall((1, 0), (1, 1))
* base.add_wall((2, 0), (2, 1))
* base.add_wall((3, 0), (3, 1))
* base.add_wall((4, 0), (4, 3))

Next we will add our horizntal walls that will form the remaining 2 compartments. The first horizontal wall will be 200 mm wide and will form the bottom wall of our  four 50 mm x 125 mm compartments. The second horizontal wall will form our remaining 2 compartments. The upper one being 200 mm wide by 50 mm tall and the other being 200 mm wide and 100 mm tall.

* base.add_wall((0, 1), (4, 1))
* base.add_wall((0, 2), (4, 2))

The resulting tray would look approximately something like this (I will upload the generated SVG image once I complete the program).

```
|--------|--------|--------|--------|----------------|
|        |        |        |        |                |
|        |        |        |        |                |
|        |        |        |        |                |
|        |        |        |        |                |
|        |        |        |        |                |
|        |        |        |        |                |
|        |        |        |        |                |
|        |        |        |        |                |
|--------|--------|--------|--------|                |
|                                   |                |
|                                   |                |
|                                   |                |
|-----------------------------------|                |
|                                   |                |
|                                   |                |
|                                   |                |
|                                   |                |
|                                   |                |
|                                   |                |
|-----------------------------------|----------------|
```
