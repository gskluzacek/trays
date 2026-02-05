import pytest
from tray.tray import Tray
from tray.geometry.point import Point, PathOrientation
from tray.geometry.line import Line, LineOrientation, WallType


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
    assert c2c_path.orientation == tray.index_paths[0].orientation
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


def test_start_base_validation():
    tray = Tray(1.0, [10.0, 10.0], [10.0, 10.0])
    with pytest.raises(ValueError, match="the index starting point must be within the bounds"):
        tray.start_base(3, 0)
    with pytest.raises(ValueError, match="the index starting point must be within the bounds"):
        tray.start_base(0, 3)
    with pytest.raises(ValueError, match="the index starting point must be within the bounds"):
        tray.start_base(-1, 0)


def test_extend_base_validation():
    tray = Tray(1.0, [10.0, 10.0], [10.0, 10.0])
    tray.start_base(0, 0)

    with pytest.raises(ValueError, match="the index point being added must be within the bounds"):
        tray.extend_base(3, 0)

    with pytest.raises(ValueError, match="cannot add the same point twice"):
        tray.extend_base(0, 0)

    with pytest.raises(ValueError, match="the point being added must have either the same x or y coordinate"):
        tray.extend_base(1, 1)

    # Valid extension
    tray.extend_base(1, 0)


def test_end_base_validation():
    tray = Tray(1.0, [10.0, 10.0], [10.0, 10.0])
    tray.start_base(0, 0)

    with pytest.raises(ValueError, match="the number of points in the base path must be at least 4"):
        tray.end_base()

    tray.extend_base(2, 0)
    tray.extend_base(2, 2)
    # 3 points total now.

    with pytest.raises(ValueError, match="the number of points in the base path must be at least 4"):
        tray.end_base()

    tray.extend_base(0, 2)
    # 4 points, but not even? No, 4 is even.
    # Actually, current implementation says:
    # if len(self.index_paths[-1].points) % 2 == 1:
    #     raise ValueError("the number of points in the base path must be even")
    # 4 is even.

    # But wait, it checks boundaries:
    # if min_x != 0 or max_x != len(self.inside_dim_cols) or min_y != 0 or max_y != len(self.inside_dim_rows):
    #     raise ValueError("the base path must have points on the boundaries...")

    # For 2x2 grid, max_x = 2, max_y = 2.
    # Our points: (0,0), (2,0), (2,2), (0,2).
    # min_x=0, max_x=2, min_y=0, max_y=2. Should pass boundaries.

    tray.end_base()  # Should pass.

    # Test odd number of points (if possible given orthogonality)
    # (0,0) -> (2,0) -> (2,1) -> (1,1) -> (1,2) -> (0,2) -> 6 points.
    # To get odd number, we'd need to break orthogonality or have same point.
    # Actually, if we add (0,0) at the end, Path.add_point will have it, but Tray.end_base doesn't add the closing point.
    # Path.finalize() adds the closing point if it's not already there.
    # Tray.end_base calls self.index_paths[-1].finalize()

    # Let's check overlapping lines in base path
    tray2 = Tray(1.0, [10.0, 10.0], [10.0, 10.0])
    tray2.start_base(0, 0)
    tray2.extend_base(2, 0)
    tray2.extend_base(2, 2)
    tray2.extend_base(0, 2)
    tray2.extend_base(0, 1)
    tray2.extend_base(2, 1) # This line (0,1)->(2,1) overlaps with nothing?
    # Wait, (0,1)->(2,1) crosses (2,0)->(2,2)? No.
    # Let's make it overlap: (0,0)->(2,0) and then later (2,0)->(0,0)
    # But Tray.end_base doesn't allow consecutive lines with same orientation.

    # (0,0) -> (2,0) -> (2,2) -> (0,2) -> (0,0) -- this is what finalize does.
    # Overlap: (0,0) -> (2,0) -> (2,2) -> (1,2) -> (1,0) -> (0,0) -> (0,2) ... hard to do with orthogonality.

    # How about (0,0) -> (2,0) -> (2,2) -> (0,2) -> (0,1) -> (2,1) -> (2,0) ...
    # (0,1) -> (2,1) and (2,1) -> (2,0) and (2,0) -> (0,0) ...
    # Let's try to create a "C" shape that overlaps itself.
    # (0,0) -> (2,0) -> (2,2) -> (0,2) -> (0,1) -> (1,1) -> (1,0) -> (0,0)
    tray3 = Tray(1.0, [10.0, 10.0, 10.0], [10.0, 10.0, 10.0])
    tray3.start_base(0, 0)
    tray3.extend_base(3, 0)
    tray3.extend_base(3, 3)
    tray3.extend_base(0, 3)
    tray3.extend_base(0, 1)
    tray3.extend_base(2, 1)
    tray3.extend_base(2, 2)
    tray3.extend_base(0, 2) # (0,2) is between (0,3) and (0,1)
    # Lines: (0,0)-(3,0), (3,0)-(3,3), (3,3)-(0,3), (0,3)-(0,1), (0,1)-(2,1), (2,1)-(2,2), (2,2)-(0,2), (0,2)-(0,0)
    # (0,3)-(0,1) and (0,2)-(0,0) overlap!
    with pytest.raises(ValueError, match="lines within the base path cannot overlap"):
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
    tray.extend_base(2, 0) # Allowed by extend_base
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
    tray.extend_base(0, 0) # 5 points
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
    tray.add_wall((1, 1), (1, 2)) # Not overlapping, just intersecting.
    tray.finalize_walls() # Should pass.

    tray.add_wall((0, 1), (1, 1)) # Overlaps with (0,1)-(2,1)
    with pytest.raises(ValueError, match="Cannot have overlapping walls"):
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
    wall_ext = Line(Point(1, 0), Point(2, 0))
    assert tray._classify_index_wall(wall_ext, LineOrientation.HORZ) == WallType.EXTERIOR

    # 2. INTERIOR: Wall not collinear with any path line
    wall_int = Line(Point(0, 1), Point(3, 1))
    assert tray._classify_index_wall(wall_int, LineOrientation.HORZ) == WallType.INTERIOR

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
    
    wall_test = Line(Point(0, 0), Point(2, 0))
    # Path 1 has (0,0)-(2,0) -> Wall is EXTERIOR
    # Path 2 has (0,0)-(1,0) -> Wall is COMBO
    with pytest.raises(ValueError, match="wall type cannot be both combo and exterior"):
        tray_conflict_3._classify_index_wall(wall_test, LineOrientation.HORZ)

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
    assert tray3._classify_index_wall(wall_test, LineOrientation.HORZ) == WallType.COMBO

    # 4. Error: No wall type found (no paths)
    tray_empty = Tray(material_thickness, inside_dim_cols, inside_dim_rows)
    with pytest.raises(ValueError, match="no wall type found for this wall"):
        tray_empty._classify_index_wall(wall_ext, LineOrientation.HORZ)
