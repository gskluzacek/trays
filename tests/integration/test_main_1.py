from tests.integration.test_utils import (
    create_tray,
    assert_base_path,
    assert_final_base_path,
    assert_wall_lines,
    assert_segment_paths,
)
from tray.geometry.types.geometric import LineOrientation, PathOrientation, PointLine
from tray.geometry.types.tray import WallType, JointType, IntrxnType


def test_main_1():
    #
    # note double line indicates a smooth joint and single line indicates a finger-space (exterior
    #   walls) or tab-slot joint (interior walls) or a combination of both (combo walls)
    #
    #    ┌─────┬─────┐           ┌─────┬─────┐
    #    │     │     │           │     │     │
    #    ├─────┼─────┤           ├─────┼─────┤
    #    │     │     │           │     │     │
    #    │     │     ╞═══════════╡     │     │
    #    │     │     │           │     │     │
    #    ├─────┴─────┼─────┬─────┼─────┴─────┤
    #    │           │     │     │           │
    #    ╘═══════════┴─────┴─────┴═══════════╛

    material_thickness: float = 5
    inside_dim_cols: list[float] = [100, 150, 100, 200, 150, 100]
    inside_dim_rows: list[float] = [100, 50, 100, 150]
    base_points = [
        (0, 0),
        (2, 0),
        (2, 2),
        (4, 2),
        (4, 0),
        (6, 0),
        (6, 4),
        (0, 4),
    ]
    base_walls = [
        ((0, 0), (2, 0)),
        ((2, 0), (2, 4)),
        ((4, 4), (4, 0)),
        ((4, 0), (6, 0)),
        ((6, 0), (6, 4)),
        ((4, 4), (2, 4)),
        ((0, 4), (0, 0)),
    ]
    interior_walls = [
        ((0, 1), (2, 1)),
        ((4, 1), (6, 1)),
        ((0, 3), (6, 3)),
        ((1, 0), (1, 3)),
        ((3, 3), (3, 4)),
        ((5, 0), (5, 3)),
    ]

    tray = create_tray(
        material_thickness=material_thickness,
        inside_dim_cols=inside_dim_cols,
        inside_dim_rows=inside_dim_rows,
        base_points=base_points,
        base_walls=base_walls,
        interior_walls=interior_walls,
        auto_exterior=False,
    )

    # ################################################################################
    # validate index_paths
    # ################################################################################

    # one per path
    expected_orientation_list = [
        PathOrientation.CW,
    ]
    # one list of x,y tuples per path
    expected_points_list = [
        [(0, 0), (2, 0), (2, 2), (4, 2), (4, 0), (6, 0), (6, 4), (0, 4)],
    ]
    # one list of p1,p2 tuples per path
    expected_line_coords_list = [
        [
            ((0, 0), (2, 0)),
            ((2, 0), (2, 2)),
            ((2, 2), (4, 2)),
            ((4, 2), (4, 0)),
            ((4, 0), (6, 0)),
            ((6, 0), (6, 4)),
            ((6, 4), (0, 4)),
            ((0, 4), (0, 0)),
        ],
    ]
    # one list of LineOrientation per path
    expected_line_orientations_list = [
        [
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
        ]
    ]
    # one list of lists per path, each list is a list of LineBreaks
    expected_line_breaks_list = [
        [[], [], [], [], [], [], [(2, 4), (4, 4)], []],
    ]

    assert len(tray.index_paths) == 1
    for i, index_path in enumerate(tray.index_paths):
        assert_base_path(
            tray.index_paths[i],
            expected_orientation=expected_orientation_list[i],
            expected_points=expected_points_list[i],
            expected_line_coords=expected_line_coords_list[i],
            expected_line_orientations=expected_line_orientations_list[i],
            expected_line_breaks=expected_line_breaks_list[i],
        )

    # ################################################################################
    # validate final_index_paths
    # ################################################################################

    # one per path
    expected_orientation_list = [
        PathOrientation.CW,
    ]
    # one list of x,y tuples per path
    expected_points_list = [
        [(0, 0), (2, 0), (2, 2), (4, 2), (4, 0), (6, 0), (6, 4), (4, 4), (2, 4), (0, 4)],
    ]
    # one list of p1,p2 tuples per path
    expected_line_coords_list = [
        [
            ((0, 0), (2, 0)),
            ((2, 0), (2, 2)),
            ((2, 2), (4, 2)),
            ((4, 2), (4, 0)),
            ((4, 0), (6, 0)),
            ((6, 0), (6, 4)),
            ((6, 4), (4, 4)),
            ((4, 4), (2, 4)),
            ((2, 4), (0, 4)),
            ((0, 4), (0, 0)),
        ],
    ]
    # one list of LineOrientation per path
    expected_line_orientations_list = [
        [
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.HORZ,
            LineOrientation.HORZ,
            LineOrientation.VERT,
        ]
    ]

    assert len(tray.final_index_paths) == 1
    for i, final_index_path in enumerate(tray.final_index_paths):
        assert_final_base_path(
            tray.final_index_paths[i],
            expected_orientation=expected_orientation_list[i],
            expected_points=expected_points_list[i],
            expected_line_coords=expected_line_coords_list[i],
            expected_line_orientations=expected_line_orientations_list[i],
        )

    # ################################################################################
    # validate index_walls
    # ################################################################################

    assert_wall_lines(
        tray.index_walls,
        expected_coords=[
            # exterior walls
            ((0, 0), (2, 0)),
            ((2, 0), (2, 4)),
            ((4, 4), (4, 0)),
            ((4, 0), (6, 0)),
            ((6, 0), (6, 4)),
            ((4, 4), (2, 4)),
            ((0, 4), (0, 0)),
            # interior walls
            ((0, 1), (2, 1)),
            ((4, 1), (6, 1)),
            ((0, 3), (6, 3)),
            ((1, 0), (1, 3)),
            ((3, 3), (3, 4)),
            ((5, 0), (5, 3)),
        ],
        expected_orientations=[
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.HORZ,
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.VERT,
            LineOrientation.VERT,
        ],
        expected_wall_types=[
            WallType.EXTERIOR,
            WallType.COMBO,
            WallType.COMBO,
            WallType.EXTERIOR,
            WallType.EXTERIOR,
            WallType.EXTERIOR,
            WallType.EXTERIOR,
            WallType.INTERIOR,
            WallType.INTERIOR,
            WallType.INTERIOR,
            WallType.INTERIOR,
            WallType.INTERIOR,
            WallType.INTERIOR,
        ],
        expected_intersections=[
            [((2, 0), IntrxnType.CORNER_RT), ((0, 0), IntrxnType.CORNER_LT), ((1, 0), IntrxnType.TEE_T)],
            [
                ((2, 0), IntrxnType.CORNER_RT),
                ((2, 4), IntrxnType.CORNER_LB),
                ((2, 1), IntrxnType.TEE_R),
                ((2, 3), IntrxnType.CROSS),
            ],
            [
                ((4, 0), IntrxnType.CORNER_LT),
                ((4, 4), IntrxnType.CORNER_RB),
                ((4, 1), IntrxnType.TEE_L),
                ((4, 3), IntrxnType.CROSS),
            ],
            [((4, 0), IntrxnType.CORNER_LT), ((6, 0), IntrxnType.CORNER_RT), ((5, 0), IntrxnType.TEE_T)],
            [((6, 0), IntrxnType.CORNER_RT), ((6, 1), IntrxnType.TEE_R), ((6, 3), IntrxnType.TEE_R)],
            [((2, 4), IntrxnType.CORNER_LB), ((4, 4), IntrxnType.CORNER_RB), ((3, 4), IntrxnType.TEE_B)],
            [((0, 0), IntrxnType.CORNER_LT), ((0, 1), IntrxnType.TEE_L), ((0, 3), IntrxnType.TEE_L)],
            [((2, 1), IntrxnType.TEE_R), ((0, 1), IntrxnType.TEE_L), ((1, 1), IntrxnType.CROSS)],
            [((4, 1), IntrxnType.TEE_L), ((6, 1), IntrxnType.TEE_R), ((5, 1), IntrxnType.CROSS)],
            [
                ((2, 3), IntrxnType.CROSS),
                ((4, 3), IntrxnType.CROSS),
                ((6, 3), IntrxnType.TEE_R),
                ((0, 3), IntrxnType.TEE_L),
                ((1, 3), IntrxnType.TEE_B),
                ((3, 3), IntrxnType.TEE_T),
                ((5, 3), IntrxnType.TEE_B),
            ],
            [((1, 0), IntrxnType.TEE_T), ((1, 1), IntrxnType.CROSS), ((1, 3), IntrxnType.TEE_B)],
            [((3, 4), IntrxnType.TEE_B), ((3, 3), IntrxnType.TEE_T)],
            [((5, 0), IntrxnType.TEE_T), ((5, 1), IntrxnType.CROSS), ((5, 3), IntrxnType.TEE_B)],
        ],
    )

    # ################################################################################
    # validate the SegmentPath for each WallLine object
    # ################################################################################
    assert_segment_paths(
        tray.index_walls,
        # each item (1 item per line) is for one wall-line's segment path points
        expected_points=[
            [(0, 0), (2, 0)],
            [(2, 0), (2, 2), (2, 4)],
            [(4, 4), (4, 2), (4, 0)],
            [(4, 0), (6, 0)],
            [(6, 0), (6, 4)],
            [(4, 4), (2, 4)],
            [(0, 4), (0, 0)],
            [(0, 1), (2, 1)],
            [(4, 1), (6, 1)],
            [(0, 3), (6, 3)],
            [(1, 0), (1, 3)],
            [(3, 3), (3, 4)],
            [(5, 0), (5, 3)],
        ],
        # each item (1 item per line) is for one wall-line's segment path lines
        expected_lines=[
            [((0, 0), (2, 0))],
            [((2, 0), (2, 2)), ((2, 2), (2, 4))],
            [((4, 4), (4, 2)), ((4, 2), (4, 0))],
            [((4, 0), (6, 0))],
            [((6, 0), (6, 4))],
            [((4, 4), (2, 4))],
            [((0, 4), (0, 0))],
            [((0, 1), (2, 1))],
            [((4, 1), (6, 1))],
            [((0, 3), (6, 3))],
            [((1, 0), (1, 3))],
            [((3, 3), (3, 4))],
            [((5, 0), (5, 3))],
        ],
        expected_orientations=[
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.HORZ,
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.VERT,
            LineOrientation.VERT,
        ],
        expected_joint_types=[
            [JointType.FS],
            [JointType.FS, JointType.TS],
            [JointType.TS, JointType.FS],
            [JointType.FS],
            [JointType.FS],
            [JointType.FS],
            [JointType.FS],
            [JointType.TS],
            [JointType.TS],
            [JointType.TS],
            [JointType.TS],
            [JointType.TS],
            [JointType.TS],
        ],
        expected_intersections=[
            [[]],
            [[], [(PointLine.BETWEEN, (2, 3), IntrxnType.CROSS)]],
            [[(PointLine.BETWEEN, (4, 3), IntrxnType.CROSS)], []],
            [[]],
            [[]],
            [[]],
            [[]],
            [[(PointLine.BETWEEN, (1, 1), IntrxnType.CROSS)]],
            [[(PointLine.BETWEEN, (5, 1), IntrxnType.CROSS)]],
            [[(PointLine.BETWEEN, (2, 3), IntrxnType.CROSS), (PointLine.BETWEEN, (4, 3), IntrxnType.CROSS)]],
            [[(PointLine.BETWEEN, (1, 1), IntrxnType.CROSS)]],
            [[]],
            [[(PointLine.BETWEEN, (5, 1), IntrxnType.CROSS)]],
        ],
    )
