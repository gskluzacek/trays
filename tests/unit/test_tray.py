import pytest
from tray.tray import Tray
from tray.geometry.final_base.final_path_line import FinalPathLine
from tray.geometry.basic.point import Point
from tray.geometry.types.geometric import PathOrientation
from tray.geometry.wall_line import WallLine
from tray.geometry.types.tray import WallType, JointType, IntrxnType


def test_tray_init():
    material_thickness = 1.5
    inside_dim_cols = [10.0, 20.0]
    inside_dim_rows = [30.0, 40.0]
    tray = Tray(material_thickness, inside_dim_cols, inside_dim_rows)

    assert tray.material_thickness == 1.5
    assert tray.inside_dim_cols == [10.0, 20.0]
    assert tray.inside_dim_rows == [30.0, 40.0]
    assert tray.index_paths == []
    assert tray.index_walls == []
    assert tray.center_to_center_dim_cols == []
    assert tray.center_to_center_dim_rows == []
    assert tray.center_to_center_points == []
    assert tray.center_to_center_paths == []
    assert tray.center_to_center_walls == []


def test_calc_center_to_center_dims():
    tray = Tray(2.0, [10.0, 20.0], [30.0, 40.0])
    tray.calc_center_to_center_dims()

    assert tray.center_to_center_dim_cols == [12.0, 22.0]
    assert tray.center_to_center_dim_rows == [32.0, 42.0]


def test_calc_center_to_center_points():
    # thickness 2.0 -> adjustment 1.0
    # cols [10, 20] -> c2c_cols [12, 22]
    # rows [30, 40] -> c2c_rows [32, 42]
    # x_coords: [1.0, 1.0+12.0=13.0, 13.0+22.0=35.0]
    # y_coords: [1.0, 1.0+32.0=33.0, 33.0+42.0=75.0]
    tray = Tray(2.0, [10.0, 20.0], [30.0, 40.0])
    tray.calc_center_to_center_dims()
    tray.calc_center_to_center_points()

    expected_x = [1.0, 13.0, 35.0]
    expected_y = [1.0, 33.0, 75.0]

    assert len(tray.center_to_center_points) == 3
    for r, y in enumerate(expected_y):
        assert len(tray.center_to_center_points[r]) == 3
        for c, x in enumerate(expected_x):
            pt = tray.center_to_center_points[r][c]
            assert pt.x == x
            assert pt.y == y


def test_base_management():
    tray = Tray(1.0, [10.0], [10.0])

    # Start a base at (0,0)
    tray.start_base(0, 0)
    assert len(tray.index_paths) == 1
    assert tray.index_paths[0].points[0].coords == (0, 0)

    # Extend to (1,0), (1,1), (0,1)
    tray.extend_base(1, 0)
    tray.extend_base(1, 1)
    tray.extend_base(0, 1)

    assert len(tray.index_paths[0].points) == 4
    assert [p.coords for p in tray.index_paths[0].points] == [(0, 0), (1, 0), (1, 1), (0, 1)]

    # End base
    tray.end_base()
    assert tray.index_paths[0].orientation == PathOrientation.CW
    assert len(tray.index_paths[0].lines) == 4


def test_calc_center_to_center_paths():
    tray = Tray(2.0, [10.0], [10.0])  # adjustment 1.0, c2c 12.0
    # x_coords: [1.0, 13.0]
    # y_coords: [1.0, 13.0]
    tray.calc_center_to_center_dims()
    tray.calc_center_to_center_points()

    tray.start_base(0, 0)
    tray.extend_base(1, 0)
    tray.extend_base(1, 1)
    tray.extend_base(0, 1)  # added to make it a rectangle
    tray.end_base()

    tray.calc_center_to_center_paths()

    assert len(tray.center_to_center_paths) == 1
    c2c_path = tray.center_to_center_paths[0]
    # Path does not have orientation anymore, orientation is in BasePath
    assert tray.index_paths[0].orientation == PathOrientation.CW
    assert [p.coords for p in c2c_path.points] == [(1.0, 1.0), (13.0, 1.0), (13.0, 13.0), (1.0, 13.0)]


def test_add_wall_and_calc_center_to_center_walls():
    tray = Tray(2.0, [10.0], [10.0])  # adjustment 1.0, c2c 12.0
    tray.calc_center_to_center_dims()
    tray.calc_center_to_center_points()

    tray.add_wall((0, 0), (1, 0))
    assert len(tray.index_walls) == 1
    assert tray.index_walls[0].p1.coords == (0, 0)
    assert tray.index_walls[0].p2.coords == (1, 0)

    tray.calc_center_to_center_walls()
    assert len(tray.center_to_center_walls) == 1
    assert tray.center_to_center_walls[0].p1.coords == (1.0, 1.0)
    assert tray.center_to_center_walls[0].p2.coords == (13.0, 1.0)


def test_auto_generate_exterior_base_walls():
    tray = Tray(2.0, [10.0], [10.0])
    tray.start_base(0, 0)
    tray.extend_base(1, 0)
    tray.extend_base(1, 1)
    tray.extend_base(0, 1)
    tray.end_base()

    tray.auto_generate_exterior_base_walls()

    assert len(tray.index_walls) == 4
    # cyclic_n_tuples(points, 2, 0) yields (p0, p1), (p1, p2), (p2, p3), (p3, p0)
    expected_coords = [((0, 0), (1, 0)), ((1, 0), (1, 1)), ((1, 1), (0, 1)), ((0, 1), (0, 0))]
    for i, (p1_coords, p2_coords) in enumerate(expected_coords):
        assert tray.index_walls[i].p1.coords == p1_coords
        assert tray.index_walls[i].p2.coords == p2_coords


def test_ndx_walls_as_tuples():
    tray = Tray(2.0, [10.0], [10.0])
    tray.add_wall((0, 0), (1, 0))

    tuples = list(tray.ndx_walls_as_tuples)
    assert tuples == [(0, 0, 1, 0)]


def test_start_base_validation_x_max():
    tray = Tray(1.0, [10.0, 10.0], [10.0, 10.0])
    with pytest.raises(ValueError, match="the index starting point must be within the bounds"):
        tray.start_base(3, 0)


def test_start_base_validation_y_max():
    tray = Tray(1.0, [10.0, 10.0], [10.0, 10.0])
    with pytest.raises(ValueError, match="the index starting point must be within the bounds"):
        tray.start_base(0, 3)


def test_start_base_validation_negative():
    tray = Tray(1.0, [10.0, 10.0], [10.0, 10.0])
    with pytest.raises(ValueError, match="the index starting point must be within the bounds"):
        tray.start_base(-1, 0)


def test_extend_base_validation_bounds():
    tray = Tray(1.0, [10.0, 10.0], [10.0, 10.0])
    tray.start_base(0, 0)
    with pytest.raises(ValueError, match="the index point being added must be within the bounds"):
        tray.extend_base(3, 0)


def test_extend_base_validation_duplicate():
    tray = Tray(1.0, [10.0, 10.0], [10.0, 10.0])
    tray.start_base(0, 0)
    with pytest.raises(ValueError, match="cannot add the same point twice"):
        tray.extend_base(0, 0)


def test_extend_base_validation_collinear():
    tray = Tray(1.0, [10.0, 10.0], [10.0, 10.0])
    tray.start_base(0, 0)
    with pytest.raises(ValueError, match="the point being added must have either the same x or y coordinate"):
        tray.extend_base(1, 1)


def test_end_base_validation_min_points():
    tray = Tray(1.0, [10.0, 10.0], [10.0, 10.0])
    tray.start_base(0, 0)

    with pytest.raises(ValueError, match="the number of points in the base path must be at least 4"):
        tray.end_base()


def test_end_base_validation_min_points_3():
    tray = Tray(1.0, [10.0, 10.0], [10.0, 10.0])
    tray.start_base(0, 0)
    tray.extend_base(2, 0)
    tray.extend_base(2, 2)
    # 3 points total now.

    with pytest.raises(ValueError, match="the number of points in the base path must be at least 4"):
        tray.end_base()


def test_end_base_validation_success():
    tray = Tray(1.0, [10.0, 10.0], [10.0, 10.0])
    tray.start_base(0, 0)
    tray.extend_base(2, 0)
    tray.extend_base(2, 2)
    tray.extend_base(0, 2)
    tray.end_base()  # Should pass.


def test_end_base_validation_overlap():
    # Let's try to create a "C" shape that overlaps itself.
    # (0,0) -> (3,0) -> (3,3) -> (0,3) -> (0,1) -> (2,1) -> (2,2) -> (0,2)
    # Lines: (0,0)-(3,0), (3,0)-(3,3), (3,3)-(0,3), (0,3)-(0,1), (0,1)-(2,1), (2,1)-(2,2), (2,2)-(0,2), (0,2)-(0,0)
    # (0,3)-(0,1) and (0,2)-(0,0) overlap!
    tray3 = Tray(1.0, [10.0, 10.0, 10.0], [10.0, 10.0, 10.0])
    tray3.start_base(0, 0)
    tray3.extend_base(3, 0)
    tray3.extend_base(3, 3)
    tray3.extend_base(0, 3)
    tray3.extend_base(0, 1)
    tray3.extend_base(2, 1)
    tray3.extend_base(2, 2)
    tray3.extend_base(0, 2)
    with pytest.raises(ValueError, match="lines cannot overlap - Line 1"):
        tray3.end_base()


def test_end_base_consecutive_orientation_validation():
    tray = Tray(1.0, [10.0, 10.0], [10.0, 10.0])
    tray.start_base(0, 0)
    # We need to bypass extend_base validation to test end_base's check for consecutive lines with same orientation
    # Actually Tray.extend_base already checks for orthogonality, but it doesn't check if it's the SAME orientation
    # as the previous line.
    # Wait, Tray.extend_base:
    # if not index_pt.is_orthogonal(prev_index_pt): ...
    # Path.add_point doesn't check orientation.
    # Let's see if we can add (0,0) -> (1,0) -> (2,0).
    # (1,0) is orthogonal to (0,0).
    # (2,0) is orthogonal to (1,0).
    # This is allowed by extend_base!
    tray.start_base(0, 0)
    tray.extend_base(1, 0)
    tray.extend_base(2, 0)  # Allowed by extend_base
    tray.extend_base(2, 1)
    tray.extend_base(2, 2)
    tray.extend_base(0, 2)
    with pytest.raises(ValueError, match="consecutive lines in the base path cannot have the same orientation"):
        tray.end_base()


def test_end_base_odd_points():
    # It's hard to get an odd number of points with orthogonality and end_base not adding closing point
    # unless we manually manipulate the path points (which we shouldn't)
    # or if start point == end point but they are consecutive? (already blocked by extend_base)
    # Wait, Tray.end_base checks len(self.index_paths[-1].points) % 2 == 1
    # If I have (0,0) -> (1,0) -> (1,1) -> (2,1) -> (2,2) -> (0,2) -- 6 points.
    # To get 5 points: (0,0) -> (1,0) -> (1,1) -> (0,1) -> (0,0) -- but wait, extend_base blocks (0,0) twice if consecutive.
    # But it doesn't block (0,0) if it's NOT consecutive.
    tray = Tray(1.0, [10.0, 10.0], [10.0, 10.0])
    tray.start_base(0, 0)
    tray.extend_base(1, 0)
    tray.extend_base(1, 1)
    tray.extend_base(0, 1)
    tray.extend_base(0, 0)  # 5 points
    with pytest.raises(ValueError, match="the number of points in the base path must be even"):
        tray.end_base()


def test_add_wall_validation():
    tray = Tray(1.0, [10.0], [10.0])
    with pytest.raises(ValueError, match="the line's starting and ending index points must be within the bounds"):
        tray.add_wall((0, 0), (2, 0))
    with pytest.raises(ValueError, match="the line's starting and ending index points must be within the bounds"):
        tray.add_wall((-1, 0), (1, 0))


def test_finalize_walls_validation():
    tray = Tray(1.0, [10.0, 10.0], [10.0, 10.0])
    tray.add_wall((0, 1), (2, 1))
    tray.add_wall((1, 1), (1, 2))  # Not overlapping, just intersecting.
    tray.finalize_walls()  # Should pass.

    tray.add_wall((0, 1), (1, 1))  # Overlaps with (0,1)-(2,1)
    with pytest.raises(ValueError, match="lines cannot overlap - Line 1"):
        tray.finalize_walls()


def test_classify_index_walls_errors():
    material_thickness = 5.0
    inside_dim_cols = [100.0, 100.0, 100.0]
    inside_dim_rows = [100.0, 100.0, 100.0]

    # 1. No wall type found (no paths)
    tray_no_path = Tray(material_thickness, inside_dim_cols, inside_dim_rows)
    tray_no_path.add_wall((0, 0), (1, 0))
    with pytest.raises(ValueError, match="no wall type found for this wall"):
        tray_no_path.classify_index_walls()

    # 2. Wall type cannot be both combo and exterior
    tray_conflict = Tray(material_thickness, inside_dim_cols, inside_dim_rows)
    # Path 1: Boundary path
    tray_conflict.start_base(0, 0)
    tray_conflict.extend_base(3, 0)
    tray_conflict.extend_base(3, 3)
    tray_conflict.extend_base(0, 3)
    tray_conflict.end_base()
    # Path 2: Segment (0,0)-(1,0)
    tray_conflict.start_base(0, 0)
    tray_conflict.extend_base(1, 0)
    tray_conflict.extend_base(1, 1)
    tray_conflict.extend_base(3, 1)
    tray_conflict.extend_base(3, 3)
    tray_conflict.extend_base(0, 3)
    tray_conflict.end_base()
    # Wall (0,0)-(2,0)
    # Against Path 1 (0,0)-(3,0): EXTERIOR (within)
    # Against Path 2 (0,0)-(1,0): COMBO (contains)
    tray_conflict.add_wall((0, 0), (2, 0))
    with pytest.raises(ValueError, match="wall type cannot be both combo and exterior"):
        tray_conflict.classify_index_walls()

    # 3. More than one exterior wall type found
    tray_multi_ext = Tray(material_thickness, inside_dim_cols, inside_dim_rows)
    tray_multi_ext.start_base(0, 0)
    tray_multi_ext.extend_base(3, 0)
    tray_multi_ext.extend_base(3, 3)
    tray_multi_ext.extend_base(0, 3)
    tray_multi_ext.end_base()

    tray_multi_ext.start_base(0, 0)
    tray_multi_ext.extend_base(3, 0)
    tray_multi_ext.extend_base(3, 1)
    tray_multi_ext.extend_base(1, 1)
    tray_multi_ext.extend_base(1, 3)
    tray_multi_ext.extend_base(0, 3)
    tray_multi_ext.end_base()

    tray_multi_ext.add_wall((1, 0), (2, 0))
    with pytest.raises(ValueError, match="more than one exterior wall type found for this wall"):
        tray_multi_ext.classify_index_walls()


def test_classify_index_walls_max_logic():
    material_thickness = 5.0
    inside_dim_cols = [100.0, 100.0, 100.0]
    inside_dim_rows = [100.0, 100.0, 100.0]

    tray = Tray(material_thickness, inside_dim_cols, inside_dim_rows)
    # Path: (0,0)-(1,0)-(1,1)-(3,1)-(3,3)-(0,3)-(0,0)
    tray.start_base(0, 0)
    tray.extend_base(1, 0)
    tray.extend_base(1, 1)
    tray.extend_base(3, 1)
    tray.extend_base(3, 3)
    tray.extend_base(0, 3)
    tray.end_base()

    # Wall (0,0)-(2,0) HORZ.
    # Against (0,0)-(1,0): COMBO (contains)
    # Max(COMBO, INTERIOR...) -> COMBO
    tray.add_wall((0, 0), (2, 0))
    tray.classify_index_walls()
    # No exception means it passed internal logic.
    # Individual wall classification is tested in test_classify_index_wall_unit.


def test_end_base_boundary_validation():
    # max_x = 2, max_y = 2
    tray = Tray(1.0, [10.0, 10.0], [10.0, 10.0])
    tray.start_base(0, 0)
    tray.extend_base(1, 0)
    tray.extend_base(1, 1)
    tray.extend_base(0, 1)
    # min_x=0, max_x=1, min_y=0, max_y=1
    # max_x should be 2, max_y should be 2
    with pytest.raises(ValueError, match="the base path must have points on the boundaries"):
        tray.end_base()


def test_classify_index_wall_unit():
    material_thickness = 5.0
    inside_dim_cols = [100.0, 100.0, 100.0]
    inside_dim_rows = [100.0, 100.0, 100.0]

    tray = Tray(material_thickness, inside_dim_cols, inside_dim_rows)
    # Path: (0,0)-(3,0)-(3,3)-(0,3)-(0,0) - Boundary path
    tray.start_base(0, 0)
    tray.extend_base(3, 0)
    tray.extend_base(3, 3)
    tray.extend_base(0, 3)
    tray.end_base()

    # 1. EXTERIOR: Wall completely within a path line
    wall_ext = WallLine(Point(1, 0), Point(2, 0))
    assert tray._classify_index_wall(wall_ext) == WallType.EXTERIOR

    # Verify that classify_index_walls actually sets the wall_type
    tray.index_walls = [wall_ext]
    tray.classify_index_walls()
    assert wall_ext.wall_type == WallType.EXTERIOR

    # 2. INTERIOR: Wall not collinear with any path line
    wall_int = WallLine(Point(0, 1), Point(3, 1))
    assert tray._classify_index_wall(wall_int) == WallType.INTERIOR

    # 3. COMBO: Wall partially overlapping path line
    # Add another path to create combo situation
    # Note: Tray.end_base requires path to be on boundaries.

    tray_conflict_3 = Tray(material_thickness, [100.0, 100.0], [100.0, 100.0, 100.0])
    # Path 1: (0,0)-(2,0)-(2,3)-(0,3)-(0,0)
    tray_conflict_3.start_base(0, 0)
    tray_conflict_3.extend_base(2, 0)
    tray_conflict_3.extend_base(2, 3)
    tray_conflict_3.extend_base(0, 3)
    tray_conflict_3.end_base()

    # Path 2: (0,0)-(1,0)-(1,1)-(2,1)-(2,3)-(0,3)-(0,0)
    tray_conflict_3.start_base(0, 0)
    tray_conflict_3.extend_base(1, 0)
    tray_conflict_3.extend_base(1, 1)
    tray_conflict_3.extend_base(2, 1)
    tray_conflict_3.extend_base(2, 3)
    tray_conflict_3.extend_base(0, 3)
    tray_conflict_3.end_base()

    wall_test = WallLine(Point(0, 0), Point(2, 0))
    # Path 1 has (0,0)-(2,0) -> Wall is EXTERIOR
    # Path 2 has (0,0)-(1,0) -> Wall is COMBO
    with pytest.raises(ValueError, match="wall type cannot be both combo and exterior"):
        tray_conflict_3._classify_index_wall(wall_test)

    # To get COMBO as result, we need COMBO and INTERIOR (or just COMBO)
    tray3 = Tray(material_thickness, [100.0, 100.0], [100.0, 100.0, 100.0])
    # Path: (0,0)-(1,0)-(1,1)-(2,1)-(2,3)-(0,3)-(0,0)
    tray3.start_base(0, 0)
    tray3.extend_base(1, 0)
    tray3.extend_base(1, 1)
    tray3.extend_base(2, 1)
    tray3.extend_base(2, 3)
    tray3.extend_base(0, 3)
    tray3.end_base()

    # Wall (0,0)-(2,0)
    # Against Path line (0,0)-(1,0): COMBO (contains it)
    # Against other path lines: INTERIOR
    # Result: COMBO
    assert tray3._classify_index_wall(wall_test) == WallType.COMBO

    # 4. Error: No wall type found (no paths)
    tray_empty = Tray(material_thickness, inside_dim_cols, inside_dim_rows)
    with pytest.raises(ValueError, match="no wall type found for this wall"):
        tray_empty._classify_index_wall(wall_ext)


def test_tray_classify_index_walls():
    material_thickness = 5.0
    inside_dim_cols = [100.0, 100.0, 100.0]
    inside_dim_rows = [100.0, 100.0, 100.0]
    tray = Tray(material_thickness, inside_dim_cols, inside_dim_rows)

    # Path that touches all boundaries:
    # (0,0) -> (3,0) -> (3,3) -> (0,3)
    tray.start_base(0, 0)
    tray.extend_base(3, 0)
    tray.extend_base(3, 3)
    tray.extend_base(0, 3)
    tray.end_base()

    # Add an exterior wall
    tray.add_wall((0, 0), (1, 0))
    # Add an interior wall
    tray.add_wall((1, 1), (2, 1))

    # Path segments for tray2:
    tray2 = Tray(material_thickness, inside_dim_cols, inside_dim_rows)
    tray2.start_base(0, 0)
    tray2.extend_base(3, 0)
    tray2.extend_base(3, 3)
    tray2.extend_base(2, 3)
    tray2.extend_base(2, 1)
    tray2.extend_base(1, 1)
    tray2.extend_base(1, 3)
    tray2.extend_base(0, 3)
    tray2.end_base()

    # Wall (1,1)-(2,1) matches L5 exactly -> EXTERIOR
    tray2.add_wall((1, 1), (2, 1))

    # Wall (0,1)-(3,1) is HORZ. -> COMBO
    tray2.add_wall((0, 1), (3, 1))

    # Wall (0,2)-(1,2) is HORZ. -> INTERIOR
    tray2.add_wall((0, 2), (1, 2))

    # No exception means it passed internal logic.
    tray2.classify_index_walls()


def test_tray_generate_walls_segments_interior():
    material_thickness = 5.0
    inside_dim_cols = [100.0, 100.0]
    inside_dim_rows = [100.0, 100.0]
    tray = Tray(material_thickness, inside_dim_cols, inside_dim_rows)

    # Boundary path: (0,0)-(2,0)-(2,2)-(0,2)-(0,0)
    tray.start_base(0, 0)
    tray.extend_base(2, 0)
    tray.extend_base(2, 2)
    tray.extend_base(0, 2)
    tray.end_base()

    # Add an interior wall (0,1)-(2,1)
    tray.add_wall((0, 1), (2, 1))
    tray.classify_index_walls()
    assert tray.index_walls[0].wall_type == WallType.INTERIOR

    tray.split_path_lines()
    tray.generate_walls_segments()

    wall = tray.index_walls[0]
    # INTERIOR wall should have first_joint_type = 0
    # segments should start with JointType.TS (0 % 2 == 0)
    assert wall.segment_path.lines[0].joint_type == JointType.TS


def test_tray_generate_walls_segments_with_no_segments():
    material_thickness = 5.0
    inside_dim_cols = [100.0, 100.0]
    inside_dim_rows = [100.0, 100.0]
    tray = Tray(material_thickness, inside_dim_cols, inside_dim_rows)

    # Boundary path: (0,0)-(2,0)-(2,2)-(0,2)-(0,0)
    tray.start_base(0, 0)
    tray.extend_base(2, 0)
    tray.extend_base(2, 2)
    tray.extend_base(0, 2)
    tray.end_base()

    # Add a wall that is exactly a boundary wall (0,0)-(2,0) -> EXTERIOR
    tray.add_wall((0, 0), (2, 0))
    # Add another wall that is exactly a boundary wall (0,0)-(0,2) -> EXTERIOR
    tray.add_wall((0, 0), (0, 2))

    tray.classify_index_walls()
    assert tray.index_walls[0].wall_type == WallType.EXTERIOR
    assert tray.index_walls[1].wall_type == WallType.EXTERIOR

    tray.split_path_lines()
    tray.generate_walls_segments()

    # wall1 (0,0)-(2,0) is horizontal
    wall1 = tray.index_walls[0]
    assert wall1.segment_path.lines[0].joint_type == JointType.FS

    # wall2 (0,0)-(0,2) is vertical
    wall2 = tray.index_walls[1]
    assert wall2.segment_path.lines[0].joint_type == JointType.FS


def test_tray_generate_walls_segments_combo_start_first():
    material_thickness = 5.0
    inside_dim_cols = [100.0, 100.0, 100.0]
    inside_dim_rows = [100.0, 100.0, 100.0]
    tray = Tray(material_thickness, inside_dim_cols, inside_dim_rows)

    # Path: (0,0)-(3,0)-(3,3)-(0,3)-(0,0)
    # This path is on the boundaries.
    tray.start_base(0, 0)
    tray.extend_base(3, 0)
    tray.extend_base(3, 3)
    tray.extend_base(0, 3)
    tray.end_base()

    # Wall (0,0)-(3,0) contains boundary path line (0,0)-(3,0) -> EXTERIOR
    tray.add_wall((0, 0), (3, 0))
    # Wall (0,0)-(0,3) contains boundary path line (0,0)-(0,3) -> EXTERIOR
    tray.add_wall((0, 0), (0, 3))

    # To test _does_wall_line_start_first, we need a wall that partially overlaps a path line.
    # We can add a break to the boundary path line (0,0)-(3,0) at (1,0) and (2,0).
    tray.index_paths[0].lines[0].add_break(Point(1, 0))
    tray.index_paths[0].lines[0].add_break(Point(2, 0))
    # Final path lines for (0,0)-(3,0) will be (0,0)-(1,0), (1,0)-(2,0), (2,0)-(3,0).

    # Wall (0,0)-(2,0) overlaps (0,0)-(1,0) and (1,0)-(2,0).
    # For (0,0)-(1,0), wall starts at 0, path line starts at 0. _does_wall_line_start_first -> False.
    # For (1,0)-(2,0), wall starts at 0, path line starts at 1. _does_wall_line_start_first -> True.
    tray.add_wall((0, 0), (2, 0))

    tray.classify_index_walls()
    # index_walls[0]: (0,0)-(3,0) -> EXTERIOR
    # index_walls[1]: (0,0)-(0,3) -> EXTERIOR
    # index_walls[2]: (0,0)-(2,0) -> COMBO (contains (0,0)-(1,0) and (1,0)-(2,0))

    tray.split_path_lines()
    tray.generate_walls_segments()

    # wall (0,0)-(3,0) EXTERIOR. Starts at 0. Path lines start at 0, 1, 2.
    # First path line is (0,0)-(1,0). starts at 0. _does_wall_line_start_first -> False. first_joint_type = 1.
    assert tray.index_walls[0].segment_path.lines[0].joint_type == JointType.FS

    # wall (0,0)-(0,3) EXTERIOR. Starts at 0. Path line (0,0)-(0,3) starts at 0.
    # _does_wall_line_start_first -> False. first_joint_type = 1.
    assert tray.index_walls[1].segment_path.lines[0].joint_type == JointType.FS

    # wall (0,0)-(2,0) COMBO. Starts at 0. Path lines (0,0)-(1,0) and (1,0)-(2,0).
    # First path line is (0,0)-(1,0). starts at 0. _does_wall_line_start_first -> False. first_joint_type = 1.
    assert tray.index_walls[2].segment_path.lines[0].joint_type == JointType.FS

    # Test wall starting BEFORE path line
    # Wall (0,0)-(2,0). We need it to overlap a path line that starts after 0.
    # (1,0)-(2,0) starts at 1.
    # But generate_wall_segments considers all overlapping path lines and sorts segment points.
    # For wall (0,0)-(2,0), segment_points will include Point(1,0) from both path lines.
    # sorted points: [wall.p1, (1,0), wall.p2] -> [(0,0), (1,0), (2,0)]
    # First segment is (0,0)-(1,0).
    # path_line_1 is (0,0)-(1,0) OR (1,0)-(2,0)?
    # segment_points[0] comes from path_line (0,0)-(1,0) if it's considered overlapping.
    # path_line (0,0)-(1,0) is_overlapping (0,0)-(2,0) is True.
    # segment_points[0].line is (0,0)-(1,0).
    # _does_wall_line_start_first((0,0)-(2,0), (0,0)-(1,0)) -> False.

    # Let's try wall (0,0)-(2,0) but the ONLY overlapping path line is (1,0)-(2,0).
    # This happens if we don't add a break at (1,0) but have a path line (1,0)-(3,0).
    # But all paths must be on boundaries... this is tricky.


def test_tray_split_path_lines_multiple_paths():
    tray = Tray(5.0, [100.0, 100.0, 100.0], [100.0, 100.0, 100.0])
    # Path 1: (0,0)-(3,0)-(3,3)-(0,3)-(0,0)
    tray.start_base(0, 0)
    tray.extend_base(3, 0)
    tray.extend_base(3, 3)
    tray.extend_base(0, 3)
    tray.end_base()

    # Path 2: (0,0)-(3,0)-(3,3)-(0,3)-(0,0) - same boundary, but maybe different internally
    # Let's just use the same one for simplicity of passing validation.
    tray.start_base(0, 0)
    tray.extend_base(3, 0)
    tray.extend_base(3, 3)
    tray.extend_base(0, 3)
    tray.end_base()

    tray.split_path_lines()
    assert len(tray.final_index_paths) == 2


def test_does_wall_line_start_first_bottom_right_to_top_left():
    # Test _does_wall_line_start_first when wall direction is bottom/right to top/left (p1 > p2)
    material_thickness = 5.0
    tray = Tray(material_thickness, [100.0], [100.0])

    # Wall (1,0) to (0,0) - direction is right to left. p1(1,0) > p2(0,0)
    # Normalized: p1_norm(0,0), p2_norm(1,0)
    wall = WallLine(Point(1, 0), Point(0, 0))

    # Path line (0.2, 0) to (0.8, 0) - horizontal
    # Normalized: p1_norm(0.2, 0), p2_norm(0.8, 0)
    # We use FinalPathLine for p2
    path_line = FinalPathLine(Point(0.2, 0.0), Point(0.8, 0.0))

    # In _does_wall_line_start_first:
    # line1_p1, line1_p2 = wall.normalize -> (0,0), (1,0)
    # line2_p1, line2_p2 = path_line.normalize -> (0.2, 0), (0.8, 0)
    # line1.p1 < line1.p2 is False ( (1,0) < (0,0) is False )
    # Returns (line1_p2.x > line2_p2.x) -> (1.0 > 0.8) -> True
    assert Tray._does_wall_line_start_first(wall, path_line) is True

    # Vertical case
    wall_v = WallLine(Point(0, 1), Point(0, 0))
    path_line_v = FinalPathLine(Point(0.0, 0.2), Point(0.0, 0.8))
    # Returns (line1_p2.y > line2_p2.y) -> (1.0 > 0.8) -> True
    assert Tray._does_wall_line_start_first(wall_v, path_line_v) is True


def test_generate_intersections_cross_updates_walls_and_segments():
    tray = Tray(5.0, [100.0], [100.0])
    wall_horz = WallLine(Point(0, 1), Point(2, 1))
    wall_vert = WallLine(Point(1, 0), Point(1, 2))
    tray.index_walls = [wall_horz, wall_vert]

    wall_horz.segment_path.add_segment(Point(0, 1), Point(2, 1), JointType.TS)
    wall_vert.segment_path.add_segment(Point(1, 0), Point(1, 2), JointType.TS)

    tray.generate_intersections()

    assert len(wall_horz.intersections) == 1
    assert len(wall_vert.intersections) == 1

    intrxn_h = wall_horz.intersections[0]
    intrxn_v = wall_vert.intersections[0]
    assert intrxn_h is intrxn_v
    assert intrxn_h.intrxn_type == IntrxnType.CROSS
    assert intrxn_h.intrxn_pt.coords == (1, 1)

    assert len(wall_horz.segment_path.lines[0].intersections) == 1
    assert len(wall_vert.segment_path.lines[0].intersections) == 1
    assert wall_horz.segment_path.lines[0].intersections[0].intrxn is intrxn_h
    assert wall_vert.segment_path.lines[0].intersections[0].intrxn is intrxn_h


def test_generate_intersections_corner_does_not_update_segments():
    tray = Tray(5.0, [100.0], [100.0])
    wall_horz = WallLine(Point(0, 0), Point(2, 0))
    wall_vert = WallLine(Point(0, 0), Point(0, 2))
    tray.index_walls = [wall_horz, wall_vert]

    wall_horz.segment_path.add_segment(Point(0, 0), Point(2, 0), JointType.TS)
    wall_vert.segment_path.add_segment(Point(0, 0), Point(0, 2), JointType.TS)

    tray.generate_intersections()

    assert len(wall_horz.intersections) == 1
    assert len(wall_vert.intersections) == 1
    assert wall_horz.intersections[0].intrxn_type == IntrxnType.CORNER_LT
    assert wall_horz.segment_path.lines[0].intersections == []
    assert wall_vert.segment_path.lines[0].intersections == []


def test_generate_intersections_no_intersection():
    tray = Tray(5.0, [100.0], [100.0])
    wall_horz = WallLine(Point(0, 0), Point(2, 0))
    wall_vert = WallLine(Point(3, 1), Point(3, 2))
    tray.index_walls = [wall_horz, wall_vert]

    tray.generate_intersections()

    assert wall_horz.intersections == []
    assert wall_vert.intersections == []
