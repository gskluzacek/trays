from tray.tray import Tray
from tray.geometry.point import PathOrientation


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
