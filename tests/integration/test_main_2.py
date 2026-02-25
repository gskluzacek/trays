from tray.tray import Tray


def test_main_2():
    auto_generate_exterior_base_walls = False
    material_thickness: float = 5
    inside_dim_cols: list[float] = [100, 25, 50, 75]
    inside_dim_rows: list[float] = [25, 125, 50, 200]

    tray = Tray(material_thickness, inside_dim_cols, inside_dim_rows)

    # define the polygon for the tray's base
    tray.start_base(0, 0)
    tray.extend_base(4, 0)
    tray.extend_base(4, 4)
    tray.extend_base(0, 4)
    tray.end_base()

    # add lines to represent the walls of the tray (these are the exterior or combo walls)
    if auto_generate_exterior_base_walls:
        tray.auto_generate_exterior_base_walls()
    else:
        tray.add_wall((0, 0), (2, 0))
        tray.add_wall((4, 2), (4, 4))
        tray.add_wall((3, 4), (1, 4))
        tray.add_wall((0, 4), (0, 0))

    # add lines to represent the walls of the tray (these are the interior walls)
    tray.add_wall((1, 1), (3, 1))
    tray.add_wall((1, 3), (3, 3))
    tray.add_wall((1, 1), (1, 3))
    tray.add_wall((3, 1), (3, 3))

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
    print("Final path lines")
    print("-" * 100)

    for i, index_path in enumerate(tray.final_index_paths):
        for j, line in enumerate(index_path.lines):
            print(f"[{i} {j}]: {line}")

    print("-" * 100)
    print("wall lines")
    print("-" * 100)

    for i, line in enumerate(tray.index_walls):
        print(f"[{i}]: {line}")

    print("--" * 100)
