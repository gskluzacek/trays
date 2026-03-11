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
    )
