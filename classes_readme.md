# BASIC geometry classes

All of the classes within the BASIC geometry classes are generic and support either Integer or Float types.

## Point - of type T

T: Integer and Float types are supported

* Point objects are immutable
* supports rich comparisons

### attributes

* **x**
* **y**

### properties

* **coords**: tuple of x,y

### instance methods

* **orientation**: of self (P1), P2, P3
* **is_orthogonal**: with self (p1), P2
* **is_between**: endpoints of self (P1), line(P1, P2)

### subclasses of Point

* SegmentPoint

## Line - of type T

T: Integer and Float types are supported

* supports rich comparisons _(though not sure how much comparisons other than == and != are useful)_
* orientation is set when the line is created

### attributes

* **p1**
* **p2**
* **orientation**: LineOrientation - HORZ | VERT | NONE

### properties

* **normalize**: tuple P1, P2 where P1 < P2
* **is_horizontal**
* **is_vertical**
* **start_end**: tuple with P1, P2

### instance methods

* **point_from_line**: self(L1) and value (V) - returns a point (Point(V, L1.p1.y) or Point(L1.p1.x, V)) that is on the
  line
  L1
* **wall_inside_path**: self(wall-line), path-line - returns a list of points from the wall-line that are strictly
  inside
  the path-line
* **is_overlapping**: with self (L1), L2 - checks if L1 strictly overlaps L2
* **is_collinear**: with self (L1), L2

### static methods

* **of_orientation**: from sequence of Lines with LineOrientation - returns a list of Lines with the given orientation

### subclasses of Line

* PathLine
* FinalPathLine
* WallLine
* SegmentLine

## Path - of type T

T: Integer and Float types are supported

* a path has a list of point of type T
* the BASIC path does not support path orientation - see the PathOrientationMixin class below
* most (if not all) usage of the Path class is through the TypedBasePath, FinalizableTypedBasePath and their subclasses

### attributes

* **points**

### properties

* **len**: _- TO BE IMPLEMENTED -_
* **points_as_tuples**: returns a list of tuples of the points

### instance methods

* **add_point**: self(path), Point(P1) - adds the point P1 to the path

### subclasses of Path

* TypedBasePath
* SegmentPath - indirectly via TypedBasePath
* FinalizableTypedBasePath - indirectly via TypedBasePath
* BasePath - indirectly via FinalizableTypedBasePath
* FinalBasePath - indirectly via FinalizableTypedBasePath

## PathOrientationMixin

A _mixin_ class that adds the following to a **Path** subclass:

* **orientation**: the path's orientation attribute: PathOrientation - CW | CCW | COL | NONE
* **set_orientation** method to set the orientation attribute. can only be called once all points are added to the path

### users of PathOrientationMixin

* BasePath
* FinalBasePath

---

# Augmentations to the BASIC geometry classes

There are 2 _abstract_ classes that augment the BASIC Path class

* TypedBasePath - directly subclasses the Path class
* FinalizableTypedBasePath - indirectly subclasses the Path class through the TypedBasePath class
* both of theses classes are Integer only types
* they both add support for a path to have a list of lines that are created from the path's points
* when subclassing these abstract classes, you must specify the type of the Line class to use

## TypedBasePath

Abstract subclass of Path of type Integer that adds support for the lines attribute of type TLine

* the TypedBasePath class does not have a finalize method - see FinalizableTypedBasePath instead

### attributes

* **point** - inherited from Path
* **lines** - list of TLine objects

### properties

* **len** - inherited from Path (TBD)
* **points_as_tuples** - inherited from Path
* **horizontal** - list of horizontal lines
* **vertical** - list of vertical lines

### instance methods

* **add_point** - inherited from Path

### subclasses of Path

* SegmentPath
* FinalizableTypedBasePath

## FinalizableTypedBasePath

Abstract subclass of TypedBasePath that adds a finalize method

* subclasses of the FinalizableTypedBasePath class must provide a _make_line method
* the _make_line method must take 2 Point objects as arguments and return a Line object of type TLine

### attributes

* **point** - inherited from Path
* **lines** - list of TLine objects

### properties

* **len** - inherited from Path (TBD)
* **points_as_tuples** - inherited from Path
* **horizontal** - list of horizontal lines
* **vertical** - list of vertical lines

### instance methods

* **add_point** - inherited from Path
* **finalize** - creates the lines attribute from the points attribute

### subclasses of Path

* BasePath
* FinalBasePath

---

# Classes derived from the BASIC & Augmented geometry classes

## SegmentPoint

SegmentPoint is a subclass of the Point class.

* adds a reference from the point back to the FinalPathLine object that it belongs to.
* SegmentPoint is an Integer only type
* SegmentPoint objects are _only_ created by the FinalPathLine.points_from_line method called in the
  _generate_wall_segments method of the FinalPathLine class
* the list of generated SegmentPoints is sorted and then the line of the first SegmentPoint is used to determine the
  type of the first joint to be assigned
* the list of SegmentPoints objects are converted to Point objects, combined with the wall's P1 and P2 points and
  assigned to the wall's segment_path.points.
* the SegmentPoint objects go out of scope and are garbage collected once _generate_wall_segments exits.

### attributes

* **x** - inherited from Point
* **y** - inherited from Point
* **line**: points to the FinalPathLine object which the point belongs to

### properties

* **coords**  - inherited from Point
* **to_point**: regular Point object with the same x and y values

### instance methods

* **orientation**  - inherited from Point
* **is_orthogonal**  - inherited from Point
* **is_between**  - inherited from Point

## PathLine

PathLine is a subclass of the Line class.

* used to define the initial path of the tray as given by the inputs
* it adds a list of line_breaks (list of Integer Point objects) to the Line object
* as well as an add_break method.

### attributes

* **p1**  - inherited from Line
* **p2**  - inherited from Line
* **orientation**  - inherited from Line
* **line_breaks** - list of Integer Point objects where the Path needs to be broken into separate lines when generating
  the FinalPathLine objects

### properties

* **normalize**  - inherited from Line
* **is_horizontal**  - inherited from Line
* **is_vertical**  - inherited from Line
* **start_end**  - inherited from Line

### instance methods

* **point_from_line**  - inherited from Line
* **wall_inside_path**  - inherited from Line
* **is_overlapping**   - inherited from Line
* **is_collinear**  - inherited from Line
* **add_break**  - adds a point to the line_breaks list

### static methods

* **of_orientation**  - inherited from Line

## FinalPathLine

FinalPathLine is a subclass of the Line class.

* used to define the final path of the tray after taking into account external and combo walls that overlap the path

### attributes

* **p1**  - inherited from Line
* **p2**  - inherited from Line
* **orientation**  - inherited from Line
* **joint_type** - the type of joint to be assigned to the path line. _The logic to set is currently pending._

### properties

* **normalize**  - inherited from Line
* **is_horizontal**  - inherited from Line
* **is_vertical**  - inherited from Line
* **start_end**  - inherited from Line
* **points_from_line**: returns a tuple-2 of SegmentPoints representing P1 and P2 of the FinalPathLine object passed in.

### instance methods

* **point_from_line**  - inherited from Line
* **wall_inside_path**  - inherited from Line
* **is_overlapping**  - inherited from Line
* **is_collinear**  - inherited from Line

### static methods

* **of_orientation**  - inherited from Line

## WallLine

WallLine is a subclass of the Line class.

* used to define the placement of the walls of the base of the tray
* uses integer P1 and P2 points to define the wall's indexed endpoints

### attributes

* **p1**  - inherited from Line
* **p2**  - inherited from Line
* **orientation**  - inherited from Line
* **wall_type**: WallType - NONE | COMBO | INTERIOR | EXTERNAL
* **segment_path**: SegmentPath - the path the defines the bottom portion of the wall

### properties

* **normalize**  - inherited from Line
* **is_horizontal**  - inherited from Line
* **is_vertical**  - inherited from Line
* **start_end**  - inherited from Line

### instance methods

* **point_from_line**  - inherited from Line
* **wall_inside_path**  - inherited from Line
* **is_overlapping**  - inherited from Line
* **is_collinear**  - inherited from Line
* **classify_wall**: sets the wall_type attribute by checking if the wall and path are/are not collinear, and comparing
  the wall's endpoints to the path's endpoints.

### static methods

* **of_orientation**  - inherited from Line

## SegmentLine

SegmentLine is a subclass of the Line class.

* used to define the path of the bottom portion of the wall.
* each segment line will have a different joint type value.
* there is no finalize method, instead segment lines are created in Tray._generate_wall_segments by calling
  SegmentPath.add_segment.

### attributes

* **p1**  - inherited from Line
* **p2**  - inherited from Line
* **orientation**  - inherited from Line
* **joint_type**: JointType - FS | TS | CR | SM | NONE - the type of joint to be assigned to the wall segment.

### properties

* **normalize**  - inherited from Line
* **is_horizontal**  - inherited from Line
* **is_vertical**  - inherited from Line
* **start_end**  - inherited from Line

### instance methods

* **point_from_line**  - inherited from Line
* **wall_inside_path**  - inherited from Line
* **is_overlapping**  - inherited from Line
* **is_collinear**  - inherited from Line

### static methods

* **of_orientation**  - inherited from Line

## BasePath

BasePath is an indirect subclass of the Path class, but directly inherits from the FinalizableTypedBasePath and
PathOrientationMixin classes.

* the BasePath class is used to define the path of the tray using a list of Point objects passed as inputs.
* each instance of the BasePath class will be in conjunction with its PathLine objects' line_breaks to create a
  FinalPathLine
  object.

### attributes

* **points** - inherited from Path
* **lines**: list of PathLine objects - inherited from TypedBasePath (via FinalizableTypedBasePath)
* **orientation**: PathOrientation - inherited from PathOrientationMixin

### properties

* **len** - inherited from Path
* **points_as_tuples** - inherited from Path
* **horizontal** - inherited from TypedBasePath
* **vertical** - inherited from TypedBasePath

### instance methods

* **add_point** - inherited from Path
* **set_orientation** - inherited from PathOrientationMixin
* **finalize** - inherited from FinalizableTypedBasePath

### private methods

* **_make_line**: returns a PathLine object from the 2 given points - abstract method inherited from
  FinalizableTypedBasePath and implemented in BasePath.

## FinalBasePath

FinalBasePath is an indirect subclass of the Path class, but directly inherits from the FinalizableTypedBasePath and
PathOrientationMixin classes.

* the FinalBasePath class is used to define the final path of the tray from the BasePath objects, their PathLine objects
  and their list of line_breaks Point objects.

### attributes

* **points** - inherited from Path
* **lines**: list of FinalPathLine objects - inherited from TypedBasePath (via FinalizableTypedBasePath)
* **orientation**: PathOrientation - inherited from PathOrientationMixin

### properties

* **len** - inherited from Path
* **points_as_tuples** - inherited from Path
* **horizontal** - inherited from TypedBasePath
* **vertical** - inherited from TypedBasePath

### instance methods

* **add_point** - inherited from Path
* **set_orientation** - inherited from PathOrientationMixin
* **finalize** - inherited from FinalizableTypedBasePath

### private methods

* **_make_line**: returns a FinalPathLine object from the 2 given points - abstract method inherited from
  FinalizableTypedBasePath and implemented in FinalBasePath.

## SegmentPath

SegmentPath is an indirect subclass of the Path class, but directly inherits from the TypedBasePath class.

* Each WallLine object has a SegmentPath object that defines the list of integer Point object which form of the bottom
  portion of the wall.
* in the Tray._generate_wall_segments method, we create SegmentPoint object when the endpoint of a FinalPathLine is
  between a WallLine's endpoints.
* the list of SegmentPoint objects are sorted, then the first one is used to lookup it's corresponding FinalPathLine
  object.
* This FinalPathLine object is compared to the WallLine object and determines the starting JointType.

### attributes

* **points** - inherited from Path
* **lines**: list of SegmentLine objects - inherited from TypedBasePath

### properties

* **len** - inherited from Path
* **points_as_tuples** - inherited from Path
* **horizontal** - inherited from TypedBasePath
* **vertical** - inherited from TypedBasePath

### instance methods

* **add_point** - inherited from Path
* **set_orientation** - inherited from PathOrientationMixin
* **add_segment**: Creates and adds a SegmentLine object to the lines attribute by taking 2 points and a joint type.

---

# Tray Class

the Tray class uses composition of the classes derived from geometry classes to create a tray

---

