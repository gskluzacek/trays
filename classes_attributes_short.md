# Point

- x
- y

# SegmentPoint (Point)

- x: int
- y: int
- line: FinalPathLine

# Line

- p1: Point of type T
- p2: Point of type T
- orientation: LineOrientation

# PathLine (Line)

- p1: Integer Point
- p2: Integer Point
- orientation: LineOrientation
- line_breaks: List of Integer Points

# FinalPathLine (Line)

- p1: Integer Point
- p2: Integer Point
- orientation: LineOrientation
- joint_type: JointType

# WallLine (Line)

- p1: Integer Point
- p2: Integer Point
- orientation: LineOrientation
- wall_type: WallType
- segment_path: SegmentPath

# SegmentLine (Line)

- p1: Integer Point
- p2: Integer Point
- orientation: LineOrientation
- joint_type: JointType

# Path

- points: List of Points of type T

# PathOrientationMixin (for subclasses of Path)

- (*) points: List of Points of type T
- orientation: PathOrientation

# TypedBasePath (Path)

- points: List of Integer Points
- lines: list of Line objects of type Tline

# FinalizableTypedBasePath (TypedBasePath) - Abstract Class (*)

- points: List of Integer Points
- lines: list of Line objects of type Tline

_note: this abstract class adds the finalize method to the TypedBasePath class and the _make_line abstract method._

# BasePath (FinalizableTypedBasePath, PathOrientationMixin)

- points: List of Integer Points
- lines: list of Line objects of type PathLine
- orientation: PathOrientation

# FinalBasePath (FinalizableTypedBasePath, PathOrientationMixin)

- points: List of Integer Points
- lines: list of Line objects of type FinalPathLine
- orientation: PathOrientation

# SegmentPath (TypedBasePath)

- points: List of Integer Points
- lines: list of Line objects of type PathLine
