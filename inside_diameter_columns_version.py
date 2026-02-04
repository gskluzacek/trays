from __future__ import annotations

from tray.tray import Tray


def main_1():
    # advanced testing for base path to external walls analysis
    auto_generate_exterior_base_walls = False
    material_thickness: float = 5
    inside_dim_cols: list[float] = [100, 150, 100, 200, 150, 100]
    inside_dim_rows: list[float] = [100, 50, 100, 150]

    tray = Tray(material_thickness, inside_dim_cols, inside_dim_rows)

    # define the polygon for the tray's base
    tray.start_base(0, 0)
    tray.extend_base(2, 0)
    tray.extend_base(2, 2)
    tray.extend_base(4, 2)
    tray.extend_base(4, 0)
    tray.extend_base(6, 0)
    tray.extend_base(6, 4)
    tray.extend_base(0, 4)
    tray.end_base()

    # add lines to represent the walls of the tray (these are the exterior walls)
    if auto_generate_exterior_base_walls:
        tray.auto_generate_exterior_base_walls()
    else:
        tray.add_wall((0, 0), (2, 0))
        # tray.add_wall((2, 0), (2, 2))
        tray.add_wall((2, 0), (2, 4))
        # tray.add_wall((4, 2), (4, 0))
        tray.add_wall((4, 4), (4, 0))
        tray.add_wall((4, 0), (6, 0))
        tray.add_wall((6, 0), (6, 4))
        tray.add_wall((4, 4), (2, 4))
        tray.add_wall((0, 4), (0, 0))

    # add lines to represent the walls of the tray (these are the interior walls)
    tray.add_wall((0, 1), (2, 1))
    tray.add_wall((4, 1), (6, 1))
    tray.add_wall((0, 3), (6, 3))
    tray.add_wall((1, 0), (1, 3))
    tray.add_wall((3, 3), (3, 4))
    tray.add_wall((5, 0), (5, 3))

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

    tray.classify_index_walls()

    # tray.calc_center_to_center_dims()
    # tray.calc_center_to_center_points()
    # tray.calc_center_to_center_paths()
    # tray.calc_center_to_center_walls()

    ...


def main_0():
    # initial testing of base code
    auto_generate_exterior_base_walls = True
    material_thickness: float = 5
    inside_dim_cols: list[float] = [42.5, 70, 67.5]
    inside_dim_rows: list[float] = [67.5, 117.5]

    tray = Tray(material_thickness, inside_dim_cols, inside_dim_rows)

    # define the polygon for the tray's base
    tray.start_base(0, 0)
    tray.extend_base(3, 0)
    tray.extend_base(3, 2)
    tray.extend_base(0, 2)
    tray.end_base()

    # add lines to represent the walls of the tray (these are the exterior walls)
    if auto_generate_exterior_base_walls:
        tray.auto_generate_exterior_base_walls()
    else:
        tray.add_wall((0, 0), (3, 0))
        tray.add_wall((3, 0), (3, 2))
        tray.add_wall((3, 2), (0, 2))
        tray.add_wall((0, 2), (0, 0))

    # add lines to represent the walls of the tray (these are the interior walls)
    tray.add_wall((1, 0), (1, 2))
    tray.add_wall((0, 1), (3, 1))
    tray.add_wall((2, 1), (2, 2))

    tray.calc_center_to_center_dims()
    tray.calc_center_to_center_points()
    tray.calc_center_to_center_paths()
    tray.calc_center_to_center_walls()

    ...


if __name__ == "__main__":
    main_1()
