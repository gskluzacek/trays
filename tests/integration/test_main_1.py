from tests.integration.test_utils import create_tray


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
    base_points = [(0, 0), (2, 0), (2, 2), (4, 2), (4, 0), (6, 0), (6, 4), (0, 4)]
    walls = [
        ((0, 0), (2, 0)),
        ((2, 0), (2, 4)),
        ((4, 4), (4, 0)),
        ((4, 0), (6, 0)),
        ((6, 0), (6, 4)),
        ((4, 4), (2, 4)),
        ((0, 4), (0, 0)),
        ((0, 1), (2, 1)),
        ((4, 1), (6, 1)),
        ((0, 3), (6, 3)),
        ((1, 0), (1, 3)),
        ((3, 3), (3, 4)),
        ((5, 0), (5, 3)),
    ]

    tray = create_tray(material_thickness, inside_dim_cols, inside_dim_rows, base_points, walls=walls, auto_exterior=False)

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

    tray.calc_center_to_center_dims()
    tray.calc_center_to_center_points()
    tray.calc_center_to_center_paths()
    tray.calc_center_to_center_walls()
