from tray.tray import Tray


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

    tray.finalize_walls()
    tray.classify_index_walls()
    tray.split_path_lines()
    tray.generate_walls_segments()

    # here we call the functions that were written before the tray methods above for finalize_walls,
    # classify_index_walls, split_path_lines, and generate_walls_segments. not sure if we will move
    # forward with this approach. or if we will scap these methods and do something else. But might
    # as well keep them in one test at least.
    tray.calc_center_to_center_dims()
    tray.calc_center_to_center_points()
    tray.calc_center_to_center_paths()
    tray.calc_center_to_center_walls()

    ...
