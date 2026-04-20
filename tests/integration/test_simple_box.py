from tray.geometry.types.geometric import PathOrientation, LineOrientation
from tray.geometry.types.tray import WallType, JointType, IntrxnType
from tests.integration.test_utils import (
    create_tray,
    assert_base_path,
    assert_final_base_path,
    assert_wall_lines,
    assert_segment_paths,
)


def test_simple_box():
    #
    # note double line indicates a smooth joint and single line indicates a finger-space (exterior
    #   walls) or tab-slot joint (interior walls) or a combination of both (combo walls)
    #
    #    ┌─────┐
    #    │     │
    #    └─────┘

    material_thickness: float = 5
    inside_dim_cols: list[float] = [100]
    inside_dim_rows: list[float] = [100]
    base_points = [
        (0, 0),
        (1, 0),
        (1, 1),
        (0, 1),
    ]

    # auto generate base walls, no additional interior walls
    tray = create_tray(
        material_thickness=material_thickness,
        inside_dim_cols=inside_dim_cols,
        inside_dim_rows=inside_dim_rows,
        base_points=base_points,
        auto_exterior=True,
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
        [(0, 0), (1, 0), (1, 1), (0, 1)],
    ]
    # one list of p1,p2 tuples per path
    expected_line_coords_list = [
        [
            ((0, 0), (1, 0)),
            ((1, 0), (1, 1)),
            ((1, 1), (0, 1)),
            ((0, 1), (0, 0)),
        ],
    ]
    # one list of LineOrientation per path
    expected_line_orientations_list = [
        [
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
        ]
    ]
    # one list of lists per path, each list is a list of LineBreaks
    expected_line_breaks_list = [[[], [], [], []]]

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
        [(0, 0), (1, 0), (1, 1), (0, 1)],
    ]
    # one list of p1,p2 tuples per path
    expected_line_coords_list = [
        [
            ((0, 0), (1, 0)),
            ((1, 0), (1, 1)),
            ((1, 1), (0, 1)),
            ((0, 1), (0, 0)),
        ],
    ]
    # one list of LineOrientation per path
    expected_line_orientations_list = [
        [
            LineOrientation.HORZ,
            LineOrientation.VERT,
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
            ((0, 0), (1, 0)),
            ((1, 0), (1, 1)),
            ((1, 1), (0, 1)),
            ((0, 1), (0, 0)),
        ],
        expected_orientations=[
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
        ],
        expected_wall_types=[
            WallType.EXTERIOR,
            WallType.EXTERIOR,
            WallType.EXTERIOR,
            WallType.EXTERIOR,
        ],
        expected_intersections=[
            [
                ((1, 0), IntrxnType.CORNER_RT),
                ((0, 0), IntrxnType.CORNER_LT),
            ],
            [
                ((1, 0), IntrxnType.CORNER_RT),
                ((1, 1), IntrxnType.CORNER_RB),
            ],
            [
                ((1, 1), IntrxnType.CORNER_RB),
                ((0, 1), IntrxnType.CORNER_LB),
            ],
            [
                ((0, 0), IntrxnType.CORNER_LT),
                ((0, 1), IntrxnType.CORNER_LB),
            ],
        ],
    )

    # ################################################################################
    # validate the SegmentPath for each WallLine object
    # ################################################################################

    assert_segment_paths(
        tray.index_walls,
        expected_points=[
            [(0, 0), (1, 0)],
            [(1, 0), (1, 1)],
            [(1, 1), (0, 1)],
            [(0, 1), (0, 0)],
        ],
        expected_lines=[
            [((0, 0), (1, 0))],
            [((1, 0), (1, 1))],
            [((1, 1), (0, 1))],
            [((0, 1), (0, 0))],
        ],
        expected_orientations=[
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
        ],
        expected_joint_types=[
            [JointType.FS],
            [JointType.FS],
            [JointType.FS],
            [JointType.FS],
        ],
        expected_intersections=[
            [[]],
            [[]],
            [[]],
            [[]],
        ],
    )
