from tray.geometry.types.geometric import PathOrientation, LineOrientation
from tray.geometry.types.tray import WallType, JointType
from tests.integration.test_utils import (
    create_tray,
    assert_base_path,
    assert_final_base_path,
    assert_wall_lines,
    assert_segment_paths,
)


def test_main_4():
    #
    # note double line indicates a smooth joint and single line indicates a finger-space (exterior
    #   walls) or tab-slot joint (interior walls) or a combination of both (combo walls)
    #
    #    ╔═══════════╗           ╔═══════════╗
    #    ║           ║           ║           ║
    #    ║           │           │           ║
    #    ║           │           │           ║
    #    ║           ╞═══════════╡           ║
    #    ║           │           │           ║
    #    ╚═══════════╡           ╞═══════════╝
    #                │           │
    #    ╔═══════════╡           ╞═══════════╗
    #    ║           │           │           ║
    #    ║           ╞═══════════╡           ║
    #    ║           │           │           ║
    #    ║           │           │           ║
    #    ║           ║           ║           ║
    #    ╚═══════════╝           ╚═══════════╝

    material_thickness: float = 5
    inside_dim_cols: list[float] = [20, 20, 20, 20, 20, 20]
    inside_dim_rows: list[float] = [20, 20, 20, 20, 20, 20, 20]
    base_points = [
        (0, 0),
        (2, 0),
        (2, 2),
        (4, 2),
        (4, 0),
        (6, 0),
        (6, 3),
        (4, 3),
        (4, 4),
        (6, 4),
        (6, 7),
        (4, 7),
        (4, 5),
        (2, 5),
        (2, 7),
        (0, 7),
        (0, 4),
        (2, 4),
        (2, 3),
        (0, 3),
    ]
    interior_walls = [
        ((2, 1), (2, 6)),
        ((4, 6), (4, 1)),
    ]

    # auto generate base walls, no additional interior walls
    tray = create_tray(
        material_thickness=material_thickness,
        inside_dim_cols=inside_dim_cols,
        inside_dim_rows=inside_dim_rows,
        base_points=base_points,
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
        [
            (0, 0),
            (2, 0),
            (2, 2),
            (4, 2),
            (4, 0),
            (6, 0),
            (6, 3),
            (4, 3),
            (4, 4),
            (6, 4),
            (6, 7),
            (4, 7),
            (4, 5),
            (2, 5),
            (2, 7),
            (0, 7),
            (0, 4),
            (2, 4),
            (2, 3),
            (0, 3),
        ],
    ]
    # one list of p1,p2 tuples per path
    expected_line_coords_list = [
        [
            ((0, 0), (2, 0)),
            ((2, 0), (2, 2)),
            ((2, 2), (4, 2)),
            ((4, 2), (4, 0)),
            ((4, 0), (6, 0)),
            ((6, 0), (6, 3)),
            ((6, 3), (4, 3)),
            ((4, 3), (4, 4)),
            ((4, 4), (6, 4)),
            ((6, 4), (6, 7)),
            ((6, 7), (4, 7)),
            ((4, 7), (4, 5)),
            ((4, 5), (2, 5)),
            ((2, 5), (2, 7)),
            ((2, 7), (0, 7)),
            ((0, 7), (0, 4)),
            ((0, 4), (2, 4)),
            ((2, 4), (2, 3)),
            ((2, 3), (0, 3)),
            ((0, 3), (0, 0)),
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
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
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
        [
            [],
            [(2, 1)],
            [],
            [(4, 1)],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [(4, 6)],
            [],
            [(2, 6)],
            [],
            [],
            [],
            [],
            [],
            [],
        ]
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
    expected_final_orientation_list = [
        PathOrientation.CW,
    ]
    # one list of x,y tuples per path
    expected_final_points_list = [
        [
            (0, 0),
            (2, 0),
            (2, 1),
            (2, 2),
            (4, 2),
            (4, 1),
            (4, 0),
            (6, 0),
            (6, 3),
            (4, 3),
            (4, 4),
            (6, 4),
            (6, 7),
            (4, 7),
            (4, 6),
            (4, 5),
            (2, 5),
            (2, 6),
            (2, 7),
            (0, 7),
            (0, 4),
            (2, 4),
            (2, 3),
            (0, 3),
        ],
    ]
    # one list of p1,p2 tuples per path
    expected_final_line_coords_list = [
        [
            ((0, 0), (2, 0)),
            ((2, 0), (2, 1)),
            ((2, 1), (2, 2)),
            ((2, 2), (4, 2)),
            ((4, 2), (4, 1)),
            ((4, 1), (4, 0)),
            ((4, 0), (6, 0)),
            ((6, 0), (6, 3)),
            ((6, 3), (4, 3)),
            ((4, 3), (4, 4)),
            ((4, 4), (6, 4)),
            ((6, 4), (6, 7)),
            ((6, 7), (4, 7)),
            ((4, 7), (4, 6)),
            ((4, 6), (4, 5)),
            ((4, 5), (2, 5)),
            ((2, 5), (2, 6)),
            ((2, 6), (2, 7)),
            ((2, 7), (0, 7)),
            ((0, 7), (0, 4)),
            ((0, 4), (2, 4)),
            ((2, 4), (2, 3)),
            ((2, 3), (0, 3)),
            ((0, 3), (0, 0)),
        ],
    ]
    # one list of LineOrientation per path
    expected_final_line_orientations_list = [
        [
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
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
            expected_orientation=expected_final_orientation_list[i],
            expected_points=expected_final_points_list[i],
            expected_line_coords=expected_final_line_coords_list[i],
            expected_line_orientations=expected_final_line_orientations_list[i],
        )

    # ################################################################################
    # validate index_walls
    # ################################################################################

    assert_wall_lines(
        tray.index_walls,
        expected_coords=[
            ((2, 1), (2, 6)),
            ((4, 6), (4, 1)),
        ],
        expected_orientations=[
            LineOrientation.VERT,
            LineOrientation.VERT,
        ],
        expected_wall_types=[
            WallType.COMBO,
            WallType.COMBO,
        ],
        expected_intersections=[
            [],
            [],
        ],
    )

    # ################################################################################
    # validate the SegmentPath for each WallLine object
    # ################################################################################
    assert_segment_paths(
        tray.index_walls,
        expected_points=[
            [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)],
            [(4, 6), (4, 5), (4, 4), (4, 3), (4, 2), (4, 1)],
        ],
        expected_lines=[
            [((2, 1), (2, 2)), ((2, 2), (2, 3)), ((2, 3), (2, 4)), ((2, 4), (2, 5)), ((2, 5), (2, 6))],
            [((4, 6), (4, 5)), ((4, 5), (4, 4)), ((4, 4), (4, 3)), ((4, 3), (4, 2)), ((4, 2), (4, 1))],
        ],
        expected_orientations=[
            LineOrientation.VERT,
            LineOrientation.VERT,
        ],
        expected_joint_types=[
            [JointType.FS, JointType.TS, JointType.FS, JointType.TS, JointType.FS],
            [JointType.FS, JointType.TS, JointType.FS, JointType.TS, JointType.FS],
        ],
        expected_intersections=[
            [[], [], [], [], []],
            [[], [], [], [], []],
        ],
    )
