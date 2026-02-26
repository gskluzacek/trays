from tray.tray import Tray


def test_main_3():
    #
    # note double line indicates a smooth joint and single line indicates a finger-space (exterior
    #   walls) or tab-slot joint (interior walls) or a combination of both (combo walls)
    #
    #    ╔═══════════╗
    #    ║           ║
    #    ║     ╒═════╝
    #    ║     │
    #    ║     ╞═════╗
    #    ║     │     ║
    #    ║     ╞═════╝
    #    ║     │
    #    ║     ╘═════╗
    #    ║           ║
    #    ╚═══════════╝

    auto_generate_exterior_base_walls = False
    material_thickness: float = 5
    inside_dim_cols: list[float] = [50, 100]
    inside_dim_rows: list[float] = [50, 100, 50, 100, 50]

    tray = Tray(material_thickness, inside_dim_cols, inside_dim_rows)

    # define the polygon for the tray's base
    tray.start_base(0, 0)
    tray.extend_base(2, 0)
    tray.extend_base(2, 1)
    tray.extend_base(1, 1)
    tray.extend_base(1, 2)
    tray.extend_base(2, 2)
    tray.extend_base(2, 3)
    tray.extend_base(1, 3)
    tray.extend_base(1, 4)
    tray.extend_base(2, 4)
    tray.extend_base(2, 5)
    tray.extend_base(0, 5)
    tray.end_base()

    # add lines to represent the walls of the tray (these are the exterior or combo walls)
    if auto_generate_exterior_base_walls:
        tray.auto_generate_exterior_base_walls()
    else:
        tray.add_wall((1, 1), (1, 4))

    # add lines to represent the walls of the tray (these are the interior walls)
    # tray.add_wall((1, 1), (3, 1))

    tray.finalize_walls()
    tray.classify_index_walls()
    tray.split_path_lines()
    tray.generate_walls_segments()

    print("-" * 100)
    print("path lines")
    print("-" * 100)

    for i, index_path in enumerate(tray.index_paths):
        for j, line in enumerate(index_path.lines):
            print(f"[{i} {j}]: {line}")

    print("-" * 100)
    print("wall lines")
    print("-" * 100)

    for i, line in enumerate(tray.index_walls):
        print(f"[{i}]: {line}")

    print("--" * 100)
