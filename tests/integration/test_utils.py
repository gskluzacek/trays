from tray.tray import Tray
from tray.geometry.types.geometric import PathOrientation, LineOrientation
from tray.geometry.types.tray import WallType, JointType
from tray.geometry.base.base_path import BasePath
from tray.geometry.final_base.final_base_path import FinalBasePath
from tray.geometry.wall_line import WallLine


def create_tray(
    material_thickness,
    inside_dim_cols,
    inside_dim_rows,
    base_points,
    base_walls=None,
    interior_walls=None,
    auto_exterior=False,
):
    """
    reusable function to create and finalize a tray
    :param material_thickness: material thickness
    :param inside_dim_cols: list of column dimensions
    :param inside_dim_rows: list of row dimensions
    :param base_points: list of (x, y) tuples for the base polygon
    :param walls: list of (start_index, end_index) tuples for additional walls
    :param auto_exterior: whether to auto-generate exterior walls
    :return: finalized Tray object
    """
    tray = Tray(material_thickness, inside_dim_cols, inside_dim_rows)

    tray.start_base(*base_points[0])
    for pt in base_points[1:]:
        tray.extend_base(*pt)
    tray.end_base()

    if auto_exterior:
        tray.auto_generate_exterior_base_walls()
    else:
        base_walls = base_walls or []
        for start, end in base_walls:
            tray.add_wall(start, end)

    interior_walls = interior_walls or []
    for start, end in interior_walls:
        tray.add_wall(start, end)

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

    # here we call the functions that were written before the tray methods above for finalize_walls,
    # classify_index_walls, split_path_lines, and generate_walls_segments. not sure if we will move
    # forward with this approach. or if we will scap these methods and do something else. But might
    # as well keep them in one test at least.
    tray.calc_center_to_center_dims()
    tray.calc_center_to_center_points()
    tray.calc_center_to_center_paths()
    tray.calc_center_to_center_walls()

    return tray


def assert_base_path(
    base_path: BasePath,
    expected_orientation,
    expected_points,
    expected_line_coords,
    expected_line_orientations,
    expected_line_breaks,
):
    """
    validates a BasePath object
    """
    assert base_path.orientation == expected_orientation
    assert len(base_path.points) == len(expected_points)
    assert base_path.points == expected_points

    assert len(base_path.lines) == len(expected_line_coords)
    assert base_path.lines == expected_line_coords

    line_orientations = [line.orientation for line in base_path.lines]
    assert line_orientations == expected_line_orientations

    line_breaks = [line.line_breaks for line in base_path.lines]
    assert line_breaks == expected_line_breaks


def assert_final_base_path(
    final_base_path: FinalBasePath, expected_orientation, expected_points, expected_line_coords, expected_line_orientations
):
    """
    validates a FinalBasePath object
    """
    assert final_base_path.orientation == expected_orientation
    assert len(final_base_path.points) == len(expected_points)
    assert final_base_path.points == expected_points

    assert len(final_base_path.lines) == len(expected_line_coords)
    assert final_base_path.lines == expected_line_coords

    line_orientations = [line.orientation for line in final_base_path.lines]
    assert line_orientations == expected_line_orientations


def assert_wall_lines(wall_lines: list[WallLine], expected_coords, expected_orientations, expected_wall_types):
    """
    validates a list of WallLine objects
    """
    assert len(wall_lines) == len(expected_coords)
    assert wall_lines == expected_coords

    line_orientations = [wall.orientation for wall in wall_lines]
    assert line_orientations == expected_orientations

    wall_types = [wall.wall_type for wall in wall_lines]
    assert wall_types == expected_wall_types


def assert_segment_paths(
    wall_lines: list[WallLine], expected_points, expected_lines, expected_orientations, expected_joint_types
):
    """
    validates segment_paths of WallLine objects
    """

    # can validate the points for each WallLine's SegmentPath by getting the segment_path.points attrbute
    # for each wall line.
    actual_points = [wall.segment_path.points for wall in wall_lines]
    assert actual_points == expected_points

    # same for the lines for each WallLine's SegmentPath
    actual_lines = [wall.segment_path.lines for wall in wall_lines]
    assert actual_lines == expected_lines

    # all segment lines for a given wall-line will have the same orientation
    # specify the orientation of each segment line
    for wall, orientation in zip(wall_lines, expected_orientations):
        assert all(line.orientation == orientation for line in wall.segment_path.lines)

    actual_joint_types = []
    for wall in wall_lines:
        # get the list of joint types for each wall-line's segment path's lines
        # and append into a list of list of joint types.
        actual_joint_types.append([line.joint_type for line in wall.segment_path.lines])
    assert actual_joint_types == expected_joint_types
