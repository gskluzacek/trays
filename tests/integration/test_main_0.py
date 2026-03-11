from tests.integration.test_utils import (
    create_tray,
    assert_base_path,
    assert_final_base_path,
    assert_wall_lines,
    assert_segment_paths,
)
from tray.geometry.types.geometric import LineOrientation, PathOrientation
from tray.geometry.types.tray import WallType, JointType


def test_center_to_center_logic():
    #
    # note double line indicates a smooth joint and single line indicates a finger-space (exterior
    #   walls) or tab-slot joint (interior walls) or a combination of both (combo walls)
    #
    #    ┌─────┬───────────┐
    #    │     │           │
    #    ├─────┼─────┬─────┤
    #    │     │     │     │
    #    └─────┴─────┴─────┘

    material_thickness: float = 5
    inside_dim_cols: list[float] = [42.5, 70, 67.5]
    inside_dim_rows: list[float] = [67.5, 117.5]
    base_points = [
        (0, 0),
        (3, 0),
        (3, 2),
        (0, 2),
    ]
    # in the original integration test code we were testing both
    #       - base walls & auto_generate_exterior_base_walls=False
    #       - no base walls & auto_generate_exterior_base_walls=True
    # base_walls = [
    #     ((0, 0), (3, 0)),
    #     ((3, 0), (3, 2)),
    #     ((3, 2), (0, 2)),
    #     ((0, 2), (0, 0)),
    # ]
    interior_walls = [
        ((1, 0), (1, 2)),
        ((0, 1), (3, 1)),
        ((2, 1), (2, 2)),
    ]

    # we have created expected results for the tray with no base walls and auto_generate_exterior_base_walls=True
    tray = create_tray(
        material_thickness=material_thickness,
        inside_dim_cols=inside_dim_cols,
        inside_dim_rows=inside_dim_rows,
        base_points=base_points,
        interior_walls=interior_walls,
        auto_exterior=True,
    )

    # need to create expected results for the tray with base walls and auto_generate_exterior_base_walls=False
    # tray = create_tray(
    #     material_thickness=material_thickness,
    #     inside_dim_cols=inside_dim_cols,
    #     inside_dim_rows=inside_dim_rows,
    #     base_points=base_points,
    #     base_walls=base_walls,
    #     interior_walls=interior_walls,
    #     auto_exterior=False,
    # )

    # ################################################################################
    # validate index_paths
    # ################################################################################

    # one per path
    expected_orientation_list = [
        PathOrientation.CW,
    ]
    # one list of x,y tuples per path
    expected_points_list = [
        [(0, 0), (3, 0), (3, 2), (0, 2)],
    ]
    # one list of p1,p2 tuples per path
    expected_line_coords_list = [
        [
            ((0, 0), (3, 0)),
            ((3, 0), (3, 2)),
            ((3, 2), (0, 2)),
            ((0, 2), (0, 0)),
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
        [(0, 0), (3, 0), (3, 2), (0, 2)],
    ]
    # one list of p1,p2 tuples per path
    expected_line_coords_list = [
        [
            ((0, 0), (3, 0)),
            ((3, 0), (3, 2)),
            ((3, 2), (0, 2)),
            ((0, 2), (0, 0)),
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
    for i, index_path in enumerate(tray.index_paths):
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
            ((0, 0), (3, 0)),
            ((3, 0), (3, 2)),
            ((3, 2), (0, 2)),
            ((0, 2), (0, 0)),
            # interior walls
            ((1, 0), (1, 2)),
            ((0, 1), (3, 1)),
            ((2, 1), (2, 2)),
        ],
        expected_orientations=[
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
        ],
        expected_wall_types=[
            WallType.EXTERIOR,
            WallType.EXTERIOR,
            WallType.EXTERIOR,
            WallType.EXTERIOR,
            WallType.INTERIOR,
            WallType.INTERIOR,
            WallType.INTERIOR,
        ],
    )

    # ################################################################################
    # validate the SegmentPath for each WallLine object
    # ################################################################################
    assert_segment_paths(
        tray.index_walls,
        # each item (1 item per line) is for one wall-line's segment path points
        expected_points=[
            [(0, 0), (3, 0)],
            [(3, 0), (3, 2)],
            [(3, 2), (0, 2)],
            [(0, 2), (0, 0)],
            [(1, 0), (1, 2)],
            [(0, 1), (3, 1)],
            [(2, 1), (2, 2)],
        ],
        # each item (1 item per line) is for one wall-line's segment path lines
        expected_lines=[
            [((0, 0), (3, 0))],
            [((3, 0), (3, 2))],
            [((3, 2), (0, 2))],
            [((0, 2), (0, 0))],
            [((1, 0), (1, 2))],
            [((0, 1), (3, 1))],
            [((2, 1), (2, 2))],
        ],
        expected_orientations=[
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
        ],
        expected_joint_types=[
            [JointType.FS],
            [JointType.FS],
            [JointType.FS],
            [JointType.FS],
            [JointType.TS],
            [JointType.TS],
            [JointType.TS],
        ],
    )
