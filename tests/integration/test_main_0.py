from tests.integration.test_utils import create_tray


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
    base_points = [(0, 0), (3, 0), (3, 2), (0, 2)]
    walls = [((1, 0), (1, 2)), ((0, 1), (3, 1)), ((2, 1), (2, 2))]

    tray = create_tray(material_thickness, inside_dim_cols, inside_dim_rows, base_points, walls=walls)

    # here we call the functions that were written before the tray methods above for finalize_walls,
    # classify_index_walls, split_path_lines, and generate_walls_segments. not sure if we will move
    # forward with this approach. or if we will scap these methods and do something else. But might
    # as well keep them in one test at least.
    tray.calc_center_to_center_dims()
    tray.calc_center_to_center_points()
    tray.calc_center_to_center_paths()
    tray.calc_center_to_center_walls()

    ...
