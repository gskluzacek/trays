from tray.geometry.types.geometric import PathOrientation, LineOrientation
from tray.geometry.types.tray import WallType
from tray.geometry.types.tray import JointType
from tray.tray import Tray


def test_simple_box():
    #
    # note double line indicates a smooth joint and single line indicates a finger-space (exterior
    #   walls) or tab-slot joint (interior walls) or a combination of both (combo walls)
    #
    #    ┌─────┐
    #    │     │
    #    └─────┘

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

    # TODO: think about the order in which we should do:
    #       * assigning joint types to the walls
    #       * splitting the path lines
    #       * generating the wall segments
    #  I'm thinking - we might not need the joint type on the walls, as we will have the joint type on the segments
    #  of each wall. and that the segments should be separate from the walls? and that we may want to wait to
    #  split the base path lines until after ? we have generated the wall segments?
    tray.finalize_walls()
    tray.classify_index_walls()
    tray.split_path_lines()
    tray.generate_walls_segments()

    # ################################################################################
    #
    # validate index_paths
    #
    # ################################################################################

    assert len(tray.index_paths) == 1

    index_path = tray.index_paths[0]

    # validations for a single path within index_paths

    # validate orientation of path
    assert index_path.orientation == PathOrientation.CW

    # validate number and coordinates of points
    assert len(index_path.points) == 4
    assert index_path.points == [
        (0, 0),
        (1, 0),
        (1, 1),
        (0, 1),
    ]

    # validate number, coordinates, orientation and line breaks of lines
    assert len(index_path.lines) == 4
    assert index_path.lines == [
        ((0, 0), (1, 0)),
        ((1, 0), (1, 1)),
        ((1, 1), (0, 1)),
        ((0, 1), (0, 0)),
    ]

    lines_orientation = [line.orientation for line in index_path.lines]
    assert lines_orientation == [
        LineOrientation.HORZ,
        LineOrientation.VERT,
        LineOrientation.HORZ,
        LineOrientation.VERT,
    ]

    line_breaks = [line.line_breaks for line in index_path.lines]
    assert line_breaks == [
        [],
        [],
        [],
        [],
    ]

    # ################################################################################
    #
    # validate final_index_paths
    #
    # ################################################################################

    assert len(tray.final_index_paths) == 1

    final_index_path = tray.final_index_paths[0]

    # validations for a single path within final_index_paths

    # validate orientation of path
    assert final_index_path.orientation == PathOrientation.CW

    # validate number and coordinates of points
    assert len(final_index_path.points) == 4
    assert final_index_path.points == [
        (0, 0),
        (1, 0),
        (1, 1),
        (0, 1),
    ]

    # validate number, coordinates, orientation and line breaks of lines
    assert len(final_index_path.lines) == 4
    assert final_index_path.lines == [
        ((0, 0), (1, 0)),
        ((1, 0), (1, 1)),
        ((1, 1), (0, 1)),
        ((0, 1), (0, 0)),
    ]

    lines_orientation = [line.orientation for line in final_index_path.lines]
    assert lines_orientation == [
        LineOrientation.HORZ,
        LineOrientation.VERT,
        LineOrientation.HORZ,
        LineOrientation.VERT,
    ]

    joint_types = [ln.joint_type for ln in final_index_path.lines]
    # assert joint_types == [
    #     JointType.FS,
    #     JointType.FS,
    #     JointType.FS,
    #     JointType.FS,
    # ]

    # ################################################################################
    #
    # validate index_walls
    #
    # ################################################################################

    # validate number, coordinates, orientation and wall types of each WallLine object
    assert len(tray.index_walls) == 4
    assert tray.index_walls == [
        ((0, 0), (1, 0)),
        ((1, 0), (1, 1)),
        ((1, 1), (0, 1)),
        ((0, 1), (0, 0)),
    ]

    lines_orientation = [line.orientation for line in tray.index_walls]
    assert lines_orientation == [
        LineOrientation.HORZ,
        LineOrientation.VERT,
        LineOrientation.HORZ,
        LineOrientation.VERT,
    ]

    wall_types = [wall.wall_type for wall in tray.index_walls]
    assert wall_types == [
        WallType.EXTERIOR,
        WallType.EXTERIOR,
        WallType.EXTERIOR,
        WallType.EXTERIOR,
    ]

    # ################################################################################
    #
    # validate the SegmentPath for each WalLine object
    #
    # ################################################################################

    # can validate the points for each WallLine's SegmentPath by getting the segment_path.points attrbute
    # for each wall line.
    wall_segment_points = [wall.segment_path.points for wall in tray.index_walls]
    assert wall_segment_points == [
        [(0, 0), (1, 0)],  # wall_line[0] : [ (P1), (P2), (P3), ... (Pn) ]
        [(1, 0), (1, 1)],  # wall_line[1] : [ (P1), (P2), (P3), ... (Pn) ]
        [(1, 1), (0, 1)],
        [(0, 1), (0, 0)],  # wall_line[n] : [ (P1), (P2), (P3), ... (Pn) ]
    ]

    # same for the lines for each WallLine's SegmentPath
    wall_segment_lines = [wall.segment_path.lines for wall in tray.index_walls]
    assert wall_segment_lines == [
        [((0, 0), (1, 0))],  # wall_line[0] : [  (L1: (P1), (P2)),   (L2: (P1), (P2)),   ... (Ln: (P1), (P2))  ]
        [((1, 0), (1, 1))],  # wall_line[1] : [  (L1: (P1), (P2)),   (L2: (P1), (P2)),   ... (Ln: (P1), (P2))  ]
        [((1, 1), (0, 1))],
        [((0, 1), (0, 0))],  # wall_line[n] : [  (L1: (P1), (P2)),   (L2: (P1), (P2)),   ... (Ln: (P1), (P2))  ]
    ]

    # all segment lines for a given wall-line will have the same orientation
    # specify the orientation of each segment line
    expected_segment_line_orientations = [
        LineOrientation.HORZ,
        LineOrientation.VERT,
        LineOrientation.HORZ,
        LineOrientation.VERT,
    ]
    for wall, orientation in zip(tray.index_walls, expected_segment_line_orientations):
        assert all(line.orientation == orientation for line in wall.segment_path.lines)

    joint_types = []
    for wall in tray.index_walls:
        # get the list of joint types for each wall-line's segment path's lines
        # and append into a list of list of joint types.
        joint_types.append([line.joint_type for line in wall.segment_path.lines])
    assert joint_types == [
        [JointType.FS],  # wall_line[0] : [ JT1, JT2, JT3, ... JTn ]
        [JointType.FS],  # wall_line[1] : [ JT1, JT2, JT3, ... JTn ]
        [JointType.FS],
        [JointType.FS],  # wall_line[n] : [ JT1, JT2, JT3, ... JTn ]
    ]

    pass
