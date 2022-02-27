from typing import List


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class ColCell:
    def __init__(self, col_span=1, row_span=1):
        self.width = None
        self.height = None
        self.col_span = col_span
        self.row_span = row_span

    def __str__(self):
        return f"{self.width} x {self.height} : {self.col_span}/{self.row_span}"

    @classmethod
    def sum_col_nbr(cls, columns: List) -> int:
        pass

    @classmethod
    def sum_col_len(cls, columns: List) -> float:
        pass


class Row:
    def __init__(self, col_cells: List[ColCell], table):
        # if not columns:
        #     raise Exception('at least one column object must be passed')
        # if Column.sum_col_nbr(columns) > table.nbr_cols:
        #     raise Exception(f'max number of table columns: {table.nbr_cols} exceeded with: {Column.sum_col_nbr(columns)} columns/col_spans')
        # if Column.sum_col_len(columns) > table.width:
        #     raise Exception(f'max table width: {table.width} exceeded ')
        # if len(table.rows) + 1 > table.nbr_rows:
        #     raise Exception(f'max number of table rows: {table.nbr_rows} exceeded')
        row_index = len(table.rows)
        for col_index, col_cell in enumerate(col_cells):
            if col_cell.col_span == 1:
                col_cell.width = table.col_widths[col_index]
            else:
                col_cell.width = sum(
                    table.col_widths[col_index : col_index + col_cell.col_span]
                )
            if col_cell.row_span == 1:
                col_cell.height = table.row_heights[row_index]
            else:
                col_cell.height = sum(
                    table.row_heights[row_index : row_index + col_cell.row_span]
                )
        self.col_cells = col_cells

    def __str__(self):
        col_cells = []
        for col_cell in self.col_cells:
            col_cells.append(str(col_cell))
        return " | ".join(col_cells)


class Table2:
    def __init__(
        self, mat_thick, col_widths, row_heights, depth_outer, depth_inner=None
    ):
        self.mat_thick = mat_thick
        self.nbr_cols = len(col_widths)
        self.col_widths = col_widths
        self.nbr_rows = len(row_heights)
        self.row_heights = row_heights
        self.width = sum(col_widths)
        self.height = sum(row_heights)
        self.depth_outer = depth_outer
        self.depth_inner = depth_inner or depth_outer
        self.rows = []
        self.parts = []

    def __str__(self):
        rows = []
        for row in self.rows:
            rows.append(str(row))
        return "\n".join(rows)

    def add_row(self, col_cells: List[ColCell]):
        self.rows.append(Row(col_cells, self))

    def generate(self):
        # generate parts which make up the tray
        self.parts.append(Part("base", self.width, self.height))
        self.parts.append(Part("top", self.width, self.depth_outer))
        self.parts.append(Part("bottom", self.width, self.depth_outer))
        self.parts.append(Part("left", self.height, self.depth_outer))
        self.parts.append(Part("right", self.height, self.depth_outer))


class Part:
    def __init__(self, part_type, width, height):
        self.origin = Point(0, 0)
        self.part_type = (
            part_type  # base, top, bottom, left, right, ltr_divider, ttb_divider
        )
        self.width = width
        self.height = height
        self.edges = {"top": None, "bottom": None, "left": None, "right": None}
        self.slots = []

    def set_origin(self, origin: Point):
        self.origin = origin


class Edge:
    def __init__(self, edge_type, length):
        self.edge_type = edge_type  # base_width, base_height, straight, vertical_joint, vertical_tab, horizontal_tab
        self.length = length
        self.vectors = []


class Slot:
    def __init__(self, slot_type, origin: Point):
        self.origin = origin
        self.slot_type = slot_type  # side_slot, ltr_base_slot, ttb_base_slot
        self.vectors = []


def main2():
    table = Table2(
        mat_thick=3,
        col_widths=[50, 50, 50, 50, 100],
        row_heights=[125, 50, 100, 25],
        depth_outer=50,
    )
    table.add_row([ColCell(), ColCell(), ColCell(), ColCell(), ColCell(row_span=3)])
    table.add_row([ColCell(col_span=4)])
    table.add_row([ColCell(col_span=4)])
    table.add_row([ColCell(col_span=5)])
    table.generate()
    print(table)


class Cell:
    def __init__(self, left=False, top=False, right=None, bottom=None, floor=True):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.floor = floor

    def __str__(self):
        val = []
        val.append("L" if self.left else " ")
        val.append("T" if self.top else " ")
        val.append("R" if self.right else "")
        val.append("B" if self.bottom else " ")
        val.append("F" if self.floor else " ")
        return "".join(val)


class Table:
    """ """

    def __init__(
        self, mat_thick, col_widths, row_heights, depth_outer, depth_inner=None
    ):
        self.mat_thick = mat_thick
        self.nbr_cols = len(col_widths)
        self.col_widths = col_widths
        self.nbr_rows = len(row_heights)
        self.row_heights = row_heights
        self.width = sum(col_widths)
        self.height = sum(row_heights)
        self.depth_outer = depth_outer
        self.depth_inner = depth_inner or depth_outer
        # finger/space beginning/ending max length  - for left to right & top to bottom parts
        # finger length                             - for left to right & top to bottom parts
        # space length                              - for left to right & top to bottom parts
        # outer-wall/intersection to slot/tab distance (beginning/ending max length)
        # number of vertical slots/tabs
        # max tab/slot length
        # max number of horizontal tabs/slots ????
        # for inner parts, the use of tabs/slots versus finger/spaces
        # kerf adjustment
        self.cells = []
        self.parts = []

    def __str__(self):
        rows = []
        for row in self.cells:
            cols = []
            for cell in row:
                cols.append(str(cell))
            rows.append(" | ".join(cols))
        return "\n".join(rows)

    def add_row(self, cells: List[Cell]):
        self.cells.append(cells)

    def generate(self):
        # generate parts which make up the tray
        self.parts.append(Part("base", self.width, self.height))
        self.parts.append(Part("top", self.width, self.depth_outer))
        self.parts.append(Part("bottom", self.width, self.depth_outer))
        self.parts.append(Part("left", self.height, self.depth_outer))
        self.parts.append(Part("right", self.height, self.depth_outer))


def main():
    table = Table(
        mat_thick=3,
        col_widths=[50, 50, 50, 50, 100],
        row_heights=[125, 50, 100, 25],
        depth_outer=50,
    )
    table.add_row(
        [
            Cell(True, True),
            Cell(True, True),
            Cell(True, True),
            Cell(True, True),
            Cell(True, True, True),
        ]
    )
    table.add_row(
        [
            Cell(True, True),
            Cell(False, True),
            Cell(False, True),
            Cell(False, True),
            Cell(True, False, True),
        ]
    )
    table.add_row(
        [
            Cell(True, True),
            Cell(False, True),
            Cell(False, True),
            Cell(False, True),
            Cell(True, False, True),
        ]
    )
    table.add_row(
        [
            Cell(True, True, None, True),
            Cell(False, True, None, True),
            Cell(False, True, None, True),
            Cell(False, True, None, True),
            Cell(False, True, True, True),
        ]
    )
    print(table)


if __name__ == "__main__":
    main()
