"""
Base
    list of pieces
    list of slots (actually list of tab-edges with the is_tab property set to false)
    list of parts (the sides of the containers)

    * mat_thick

    * col_widths (list of column  widths)
    nbr_cols (length of column widths)
    width (sum of column widths)
    list of column offsets - for each column, the cumulative length from the left-hand edge

    * row_heights (list of row heights)
    nbr_rows (length of row heights)
    height = (sum of row heights)
    list of row offsets - for each row, the cumulative length from the top edge

    * depth_outer
    ** depth_inner (or depth_outer if none)

    defaults for
    - finger max length beginning/end vectors
    - finger vector length
    - space vector length
    - tab-segment spacing vector length
    - tab max length beginning/end vectors
    - tab spacing vector length
    - number of tabs
    - max tab length

Part
    dictionary of edges: bottom, right, top left
    list of slots (actually list of tab-edges with the is_tab property set to false)

Edge
    list of edge-segments
    edge-length

edge-segment
    edge-generator-sub-class instance: straight, finger, tab
    edge-segment-length

    ::  for each type of edge-segment, we will need to check the previous and next segment and or edge. For example
        to correctly render the vector for the material. the material vector could be rendered as a line with a
        non-zero width stroke or a line with a zero width stroke

    straight-edge:
        no extra properties

    finger-edge:
        finger max length beginning/end vectors
        finger vector length
        space vector length
        starts-with-finger (True | False) ***

    tab-edge (delegates actual generating to the tab-segment generator):
        is_tab (True - is a tab OR False - is a slot)
        tab_orientation (None - if is_tab is False or if is_tab is True: hor (horizontal) or vert (vertical))
        list of tab-segments
        spacing vector length -- space added before tabs begin, after tabs end and between tabs
        * in the base (top/bottom) parts
            - for a tab ending at an outer wall the space will be the material thickness plus the spacing length
            - for a tab intersecting with an inner wall - same as above
            - for multiple tabs within a tab-segment - the space will be the material thickness plus the spacing length
        * in side parts (could have a flag to make 1st option the same as the 2nd option below???)
            - for a tab ending at a straight edge - do not take the material into consideration - just the spacing length
            - for all other - the space will be the material thickness plus the spacing length

    tab-segment (child/sub generator to the tab-edge)
        tab-segment-length (required)
        = specify 1 of the following properties, but not both
        = [ need to take into consideration the differences between how tabs for sides/bases are handled ]
        number of tabs -- [after considering material thickness] take the seg-len subtract (nbr-o-tabs plus 1) times spc-len and divide by nbr-o-tabs
        max tab length


finger edge use cases (rectangular bases only)
    - needs to be updated for edge-segments when dealing with base objects

    uc  curr    prev    be      fngr    spc     comp    mat         edges for non-base parts
    1   F       F       S       a       b       F > S   no-line     top & bottom parts all edges
    2   F       S       S       a       b       F > S   line        parts 2 & 4 left & right edges
    3   S       F       F       b       a       S > F   no-line     parts 2 & 4 top & bottom edges
    4   S       S       F       b       a       S > F   line        parts 1 & 3 all edges


finger / space calculations
    * may need to check if the result of the initial calculation has a remainder of 0 and if so no need to do int()+1

    total len = 200
    mat thick = 3
    be max len = 30
    minFS == total_len - ((mat_thick + be_len) * 2) ==> 134

    when starts with finger first
        fngr len = 20
        spc len = 10

        int( (min_FS + spc_len) / (fngr_len + spc_len) ) + 1  ==> number of fingers (where finger len is finger len)
                                              nbr_o_fngrs - 1 ==> number of spaces (where space len is space len)

        int((134 + 10) / (20 + 10)) + 1 ==> nbr_o_fngrs = 5 and nbr_o_spcs = 4

        be_max_len + ( ( min_FS - ((nbr_o_fngrs * fngr_len) + (nbr_o_spcs * spc_len)) ) / 2) ==> actual be len

        30 + ((134 - ((5 * 20) + (4 * 10))) / 2) = 27

    when starts with space first
        fngr len = 10
        spc len = 20

        int( (min_FS + fngr_len) / (spc_len  + fngr_len) ) + 1  ==> number of spaces (where space len is finger len)
                                                 nbr_o_spcs - 1 ==> number of fingers (where finger len is space len)

        int((134 + 10) / (20 + 10)) + 1 ==> nbr_o_spcs = 5 and nbr_o_fngrs = 4

        be_max_len + ( ( min_FS - ((nbr_o_spcs * fngr_len) + (nbr_o_fngrs * spc_len)) ) / 2) ==> actual be len

        30 + ((134 - ((5 * 20) + (4 * 10))) / 2) = 27


tab calculations
    when using number of tabs must determine the tab length

        ( tot_len - (( nbr_o_tabs + 1 ) * spc_len) ) / nbr_o_tabs ==> tab_len

        total length = 78
        space length = 5
        number of tabs = 3 / (number of spaces is nbr_o_tab + 1 ==> 4)

        (78 - ((3 + 1) * 5)) / 3 ==> 19.333333

    when using max tab length must do calculation in 2 steps

        1st calc number of tabs and spaces

            (tot_len - spc_len) / (max_tab_len - spc_len) ==> initial number of tabs

            if (tot_len - spc_len) modulo (max_tab_len - spc_len) doesn't equal 0 then
                nbr_o_tabs = int(init_nbr_o_tabs) + 1

        2nd calc actual tab length

            ( tot_len - (( nbr_o_tabs + 1 ) * spc_len) ) / nbr_o_tabs ==> tab_len

        total length = 78
        space length = 5
        max tab length = 20

        #1      (78 - 5) / (20 + 5) ==> 2.92 {the initial number of tabs}
                (78 - 5) % (20 + 5) ==> 23  {the remainder is not 0}
                      int(2.92) + 1 ==> 3 {final number of tabs}
                              3 + 1 ==> 4 {number of spaces}

        #2     (78 - ((3 + 1) * 5)) / 3 ==> 19.333333 {tab length}


column / row offset calculations

    multiple options
    - width & height are inside dimensions of each compartment
        overall dimensions will be greater by # cols + 1 * mt and # rows + 1 * mt
    - width & height are outside dimensions of each compartment
        overall dimensions will be reduced by # cols - 1 * mt and # rows - 1 * mt
    - width & height are on-center dimensions of each compartment
         overall dimensions will be greater by mt and mt
         inside compartment dims of each compartment will be reduced by mt & mt
    - width & height are ratios to the total with & height
        the overall width (ow) is the sum of all column widths
        the overall height (oh) is the sum of all row heights
        the dimensions of a given compartment is:
            (ow - ((nbr_of_cols + 1) * mat_thick)) * given_cols_width / ow
            (oh - ((nbr_of_rows + 1) * mat_thick)) * given_rows_width / oh
"""


from enum import Enum
from typing import List, Dict, Optional


class EdgeName(Enum):
    # enumeration values start at 1?
    # EdgeName.BOTTOM.name --> 'BOTTOM'
    # EdgeName['BOTTOM'] == EdgeName(1) == EdgeName.BOTTOM
    # edge_name = EdgeName.BOTTOM; edge_name.name == 'BOTTOM'; edge_name.value == 1
    # list(EdgeName) --> [<EdgeName.BOTTOM: 1>, <EdgeName.RIGHT: 2>, <EdgeName.TOP: 3>, <EdgeName.LEFT: 4>]
    # for name, member in EdgeName.__members__.items(): print(name, member.value
    BOTTOM = 1
    RIGHT = 2
    TOP = 3
    LEFT = 4


class DimFactory:
    def __init__(self, mat_thick):
        self.mat_thick = mat_thick

    def from_lhd(self, left_hand_dim):
        return Dim(left_hand_dim, left_hand_dim + self.mat_thick)

    def from_rhd(self, right_hand_dim):
        return Dim(right_hand_dim - self.mat_thick, right_hand_dim)


class Dim:
    def __init__(self, left_hand_dim, right_hand_dim):
        self.left_hand_dim = left_hand_dim
        self.right_hand_dim = right_hand_dim

    def __str__(self):
        return f"[{self.left_hand_dim}, {self.right_hand_dim}]"

    def get_inside_dim(self, other):
        # TODO: self must be the left-hand dim
        #   other must be the right-hand dim
        #   have a validation and raise an error if not correct
        #   this must validate both lhd's rhd < rhd's lhd
        #   and lhd's lhd < rhd's rhd
        return other.left_hand_dim - self.right_hand_dim

    def get_outside_dim(self, other):
        # TODO: self must be the left-hand dim
        #   other must be the right-hand dim
        #   have a validation and raise an error if not correct
        #   this must validate both lhd's rhd < rhd's lhd
        #   and lhd's lhd < rhd's rhd
        return other.coord_2 - self.left_hand_dim


class EdgeSegment:
    def __init__(self):
        pass


class Edge:
    def __init__(self):
        self.length = 0
        self.edge_segments = []


class Part:
    def __init__(self):
        self.edges: Dict[EdgeName, Edge] = {edge_name: Edge() for edge_name in EdgeName}
        self.slots = []


# class Link:
#     def __init__(self):
#         pass


# class Piece:
#     def __init__(self):
#         self.part = None
#         self.links = []


class Base:
    def __init__(
        self,
        mat_thick: float,
        col_widths: List[float],
        row_heights: List[float],
        depth_outer: float,
        depth_inner: float = None,
    ):
        self.pieces: List[Part] = []
        self.slots = []
        self.slots = []

        self.mat_thick = mat_thick
        self.depth_outer = depth_outer
        self.depth_inner = depth_inner or self.depth_outer

        self.col_widths = col_widths
        self.nbr_cols = len(self.col_widths)
        self.width = sum(self.col_widths)

        self.row_heights = row_heights
        self.nbr_rows = len(self.row_heights)
        self.height = sum(self.row_heights)

        df = DimFactory(self.mat_thick)

        # calc the ratio to adjust the column widths with
        #   total_mat_thickness = (nbr_of_cols + 1) * mat_thick
        #   total_inside_dim_cols_widths = total_of_all_columns - total_mat_thickness
        #   ratio = total_inside_dim_cols_widths / total_of_all_columns
        col_ratio = (self.width - ((self.nbr_cols + 1) * self.mat_thick)) / self.width
        # calc adjusted columns (i.e., inside dim width)
        col_id_widths = [col * col_ratio for col in self.col_widths]
        # calc the offsets when adj col widths are accumulated with corresponding mat_thickness
        # initial col position
        col_offsets = [0]
        for i, col_id_width in enumerate(col_id_widths):
            prev_col_offset = col_offsets[i]
            # take previous column position add current column position plus the mat_thickness
            col_offsets.append(prev_col_offset + col_id_width + self.mat_thick)
        # generate the left-hand/right-hand dimension objects for each column position
        self.col_dims = [df.from_lhd(col_offset) for col_offset in col_offsets]
        # print out the inside dimension for each column should be equal to `col_id_widths`
        # for i in range(1, len(self.col_dims)):
        #     print(self.col_dims[i - 1].get_inside_dim(self.col_dims[i]))
        # print('-' * 100)

        row_ratio = (self.height - ((self.nbr_rows + 1) * self.mat_thick)) / self.height
        row_id_heights = [row * row_ratio for row in self.row_heights]
        row_offsets = [0]
        for i, row_id_height in enumerate(row_id_heights):
            prev_row_offset = row_offsets[i]
            row_offsets.append(prev_row_offset + row_id_height + self.mat_thick)
        self.row_dims = [df.from_lhd(row_offset) for row_offset in row_offsets]
        # print out the inside dimension for each row should be equal to `row_id_heights`
        # for i in range(1, len(self.row_dims)):
        #     print(self.row_dims[i - 1].get_inside_dim(self.row_dims[i]))
        # print()

    def add_piece(self):
        part = Part()
        self.pieces.append(part)
        return part

    def add_part(self):
        pass

    def add_edge_segment(self, part: Part, edge_name: EdgeName, start, end):
        start, end = (end, start) if start > end else (start, end)
        start_col = self.col_dims[start(0)]
        end_col = self.col_dims[end(0)]
        start_row = self.col_dims[start(1)]
        end_row = self.col_dims[end(1)]
        part.edges[edge_name].length = 99
        part.edges[edge_name].edge_segments.append()


def main():
    base = Base(
        mat_thick=3,
        col_widths=[50, 50, 50, 50, 100],
        row_heights=[125, 50, 100, 25],
        depth_outer=50,
    )

    for i in range(1, len(base.col_dims)):
        inside_dim = base.col_dims[i - 1].get_inside_dim(base.col_dims[i])
        unadj_dim = base.col_widths[i - 1]
        print(inside_dim, unadj_dim, unadj_dim - inside_dim)
    print("-" * 100)
    for i in range(1, len(base.row_dims)):
        inside_dim = base.row_dims[i - 1].get_inside_dim(base.row_dims[i])
        unadj_dim = base.row_heights[i - 1]
        print(inside_dim, unadj_dim, unadj_dim - inside_dim)

    pc1 = base.add_piece()
    base.add_edge_segment(pc1, EdgeName.BOTTOM, (0, 4), (5, 4))
    base.add_edge_segment(pc1, EdgeName.RIGHT, (5, 4), (5, 0))
    base.add_edge_segment(pc1, EdgeName.TOP, (5, 0), (0, 0))
    base.add_edge_segment(pc1, EdgeName.LEFT, (0, 0), (0, 4))

    base.add_piece()


if __name__ == "__main__":
    main()
