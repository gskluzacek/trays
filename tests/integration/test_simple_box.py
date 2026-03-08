from tray.geometry.types.geometric import PathOrientation, LineOrientation
from tray.geometry.types.tray import WallType, JointType
from tests.integration.test_utils import (
    create_tray,
    assert_base_path,
    assert_final_base_path,
    assert_wall_lines,
    assert_segment_paths,
)


def test_simple_box():
    #
    #    ┌─────┐
    #    │     │
    #    └─────┘

    material_thickness: float = 5
    inside_dim_cols: list[float] = [100]
    inside_dim_rows: list[float] = [100]
    base_points = [(0, 0), (1, 0), (1, 1), (0, 1)]

    tray = create_tray(material_thickness, inside_dim_cols, inside_dim_rows, base_points)

    # ################################################################################
    # validate index_paths
    # ################################################################################

    assert len(tray.index_paths) == 1
    assert_base_path(
        tray.index_paths[0],
        expected_orientation=PathOrientation.CW,
        expected_points=[(0, 0), (1, 0), (1, 1), (0, 1)],
        expected_line_coords=[
            ((0, 0), (1, 0)),
            ((1, 0), (1, 1)),
            ((1, 1), (0, 1)),
            ((0, 1), (0, 0)),
        ],
        expected_line_orientations=[
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
        ],
        expected_line_breaks=[[], [], [], []],
    )

    # ################################################################################
    # validate final_index_paths
    # ################################################################################

    assert len(tray.final_index_paths) == 1
    assert_final_base_path(
        tray.final_index_paths[0],
        expected_orientation=PathOrientation.CW,
        expected_points=[(0, 0), (1, 0), (1, 1), (0, 1)],
        expected_line_coords=[
            ((0, 0), (1, 0)),
            ((1, 0), (1, 1)),
            ((1, 1), (0, 1)),
            ((0, 1), (0, 0)),
        ],
        expected_line_orientations=[
            LineOrientation.HORZ,
            LineOrientation.VERT,
            LineOrientation.HORZ,
            LineOrientation.VERT,
        ],
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
    )
