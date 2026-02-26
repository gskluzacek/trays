from tray.tray import Tray


def test_simple_box():
    auto_generate_exterior_base_walls = True
    material_thickness: float = 5
    inside_dim_cols: list[float] = [100]
    inside_dim_rows: list[float] = [100]

    tray = Tray(material_thickness, inside_dim_cols, inside_dim_rows)

    # define the polygon for the tray's base
    tray.start_base(0, 0)
    tray.extend_base(1, 0)
    tray.extend_base(1, 1)
    tray.extend_base(0, 1)
    tray.end_base()

    # add lines to represent the walls of the tray (these are the exterior or combo walls)
    if auto_generate_exterior_base_walls:
        tray.auto_generate_exterior_base_walls()
    else:
        pass

    tray.finalize_walls()
    tray.classify_index_walls()
    tray.split_path_lines()
    tray.generate_walls_segments()

    assert len(tray.index_paths) == 1
    assert len(tray.final_index_paths) == 1
    pass
