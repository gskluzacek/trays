from tray.geometry.types.geometric import PathOrientation
from tray.geometry.types.tray import JointType
from tray.tray import Tray


def test_main_3a():
    #
    # note double line indicates a smooth joint and single line indicates a finger-space (exterior
    #   walls) or tab-slot joint (interior walls) or a combination of both (combo walls)
    #
    #    ╔═══════════╗
    #    ║           ║
    #    ║           ║
    #    ║           ║
    #    ║     ╔═════╝
    #    ║     ║
    #    ║     │
    #    ║     │
    #    ║     ╞═════╗
    #    ║     │     ║
    #    ║     │     ║
    #    ║     │     ║
    #    ║     ╞═════╝
    #    ║     │
    #    ║     │
    #    ║     ║
    #    ║     ╚═════╗
    #    ║           ║
    #    ║           ║
    #    ║           ║
    #    ╚═══════════╝

    auto_generate_exterior_base_walls = False
    material_thickness: float = 5
    inside_dim_cols: list[float] = [50, 100]
    inside_dim_rows: list[float] = [25, 25, 50, 50, 25, 25, 50, 50, 25, 250]

    tray = Tray(material_thickness, inside_dim_cols, inside_dim_rows)

    # define the polygon for the tray's base
    tray.start_base(0, 0)
    tray.extend_base(2, 0)
    tray.extend_base(2, 2)
    tray.extend_base(1, 2)
    tray.extend_base(1, 4)
    tray.extend_base(2, 4)
    tray.extend_base(2, 6)
    tray.extend_base(1, 6)
    tray.extend_base(1, 8)
    tray.extend_base(2, 8)
    tray.extend_base(2, 10)
    tray.extend_base(0, 10)
    tray.end_base()

    # add lines to represent the walls of the tray (these are the exterior or combo walls)
    if auto_generate_exterior_base_walls:
        tray.auto_generate_exterior_base_walls()
    else:
        tray.add_wall((1, 3), (1, 7))

    # add lines to represent the walls of the tray (these are the interior walls)
    # tray.add_wall((1, 1), (3, 1))

    tray.finalize_walls()
    tray.classify_index_walls()
    tray.split_path_lines()
    tray.generate_walls_segments()

    #
    # validate final_index_paths
    #
    assert len(tray.final_index_paths) == 1
    # validations for a single path within final_index_paths
    final_index_path = tray.final_index_paths[0]
    assert len(final_index_path.points) == 14
    assert final_index_path.points == [
        (0, 0),
        (2, 0),
        (2, 2),
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 4),
        (2, 6),
        (1, 6),
        (1, 7),
        (1, 8),
        (2, 8),
        (2, 10),
        (0, 10),
    ]
    assert final_index_path.orientation == PathOrientation.CW
    assert len(final_index_path.lines) == 14
    assert final_index_path.lines == [
        ((0, 0), (2, 0)),
        ((2, 0), (2, 2)),
        ((2, 2), (1, 2)),
        ((1, 2), (1, 3)),
        ((1, 3), (1, 4)),
        ((1, 4), (2, 4)),
        ((2, 4), (2, 6)),
        ((2, 6), (1, 6)),
        ((1, 6), (1, 7)),
        ((1, 7), (1, 8)),
        ((1, 8), (2, 8)),
        ((2, 8), (2, 10)),
        ((2, 10), (0, 10)),
        ((0, 10), (0, 0)),
    ]
