from tray.tray import Tray


def main():
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

    material_thickness = 5
    inside_dim_cols = [100, 150, 100, 200, 150, 100]
    inside_dim_rows = [100, 50, 100, 150]

    tray = Tray(material_thickness, inside_dim_cols, inside_dim_rows)

    # base path
    tray.start_base(0, 0)
    tray.extend_base(2, 0)
    tray.extend_base(2, 2)
    tray.extend_base(4, 2)
    tray.extend_base(4, 0)
    tray.extend_base(6, 0)
    tray.extend_base(6, 4)
    tray.extend_base(0, 4)
    tray.end_base()

    # base walls
    tray.add_wall((0, 0), (2, 0))
    tray.add_wall((2, 0), (2, 4))
    tray.add_wall((4, 4), (4, 0))
    tray.add_wall((4, 0), (6, 0))
    tray.add_wall((6, 0), (6, 4))
    tray.add_wall((4, 4), (2, 4))
    tray.add_wall((0, 4), (0, 0))

    # interior walls
    tray.add_wall((0, 1), (2, 1))
    tray.add_wall((4, 1), (6, 1))
    tray.add_wall((0, 3), (6, 3))
    tray.add_wall((1, 0), (1, 3))
    tray.add_wall((3, 3), (3, 4))
    tray.add_wall((5, 0), (5, 3))

    tray.finalize_walls()
    tray.classify_index_walls()
    tray.split_path_lines()
    tray.generate_walls_segments()
    tray.generate_intersections()

    pass


if __name__ == "__main__":
    main()
