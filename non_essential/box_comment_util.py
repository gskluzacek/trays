"""
Generate a Unicode box-drawing comment block from:
- an orthogonal base outline path (start_base/extend_base/end_base)
- extra wall segments (add_wall)

Key behavior:
- y increases going down
- base outline edges are rendered as DOUBLE lines
- add_wall() edges are rendered as SINGLE lines
- if an edge is both base+wall, render it as SINGLE (interior feature wins)

IMPORTANT FIX vs earlier versions:
- Long segments (e.g. (1,1)->(1,4)) are split into unit grid edges:
    (1,1)->(1,2), (1,2)->(1,3), (1,3)->(1,4)
  Otherwise junctions at intermediate points (like (1,2) and (1,3)) never get
  adjacency entries, and you’ll see corners (╚/╔) instead of T-joints (╞/╡).
"""

from __future__ import annotations

from typing import Literal

Style = Literal["s", "d"]  # single, double


def _hline(style: Style) -> str:
    return "─" if style == "s" else "═"


def _vline(style: Style) -> str:
    return "│" if style == "s" else "║"


def _add_edge(
    edges: dict[tuple[tuple[int, int], tuple[int, int]], Style],
    a: tuple[int, int],
    b: tuple[int, int],
    style: Style,
) -> None:
    ax, ay = a
    bx, by = b
    if ax != bx and ay != by:
        raise ValueError(f"Non-orthogonal segment: {a} -> {b}")

    key = (a, b) if a <= b else (b, a)
    prev = edges.get(key)
    if prev is None:
        edges[key] = style
        return

    # If an edge is both base(double) and interior wall(single), render it as SINGLE.
    if prev != style:
        edges[key] = "s"


def _add_segment_split(
    edges: dict[tuple[tuple[int, int], tuple[int, int]], Style],
    a: tuple[int, int],
    b: tuple[int, int],
    style: Style,
) -> None:
    """Split a long orthogonal segment into unit grid edges and add each."""
    ax, ay = a
    bx, by = b

    if ax == bx and ay == by:
        return
    if ax != bx and ay != by:
        raise ValueError(f"Non-orthogonal segment: {a} -> {b}")

    if ax == bx:
        step = 1 if by > ay else -1
        y = ay
        while y != by:
            y2 = y + step
            _add_edge(edges, (ax, y), (ax, y2), style)
            y = y2
    else:
        step = 1 if bx > ax else -1
        x = ax
        while x != bx:
            x2 = x + step
            _add_edge(edges, (x, ay), (x2, ay), style)
            x = x2


def _junction_char(n: Style | None, e: Style | None, s: Style | None, w: Style | None) -> str:
    """
    Pick the best single Unicode box-drawing glyph for a junction.

    When opposite directions on the same axis disagree in style (e.g. n="d", s="s"),
    resolve that axis to SINGLE ("weaker") so we get T-junctions like ╞ instead of corners.
    """

    def axis_style(a: Style | None, b: Style | None) -> Style | None:
        if a is None and b is None:
            return None
        if a is None:
            return b
        if b is None:
            return a
        return "s" if ("s" in (a, b)) else "d"

    conns = {"n": n, "e": e, "s": s, "w": w}
    present = {k for k, v in conns.items() if v is not None}
    if not present:
        return " "

    v_style = axis_style(n, s)
    h_style = axis_style(e, w)
    key = frozenset(present)

    # Straight lines
    if present <= {"e", "w"}:
        return "─" if h_style == "s" else "═"
    if present <= {"n", "s"}:
        return "│" if v_style == "s" else "║"

    # Same-style junctions
    if v_style == "s" and h_style == "s":
        table = {
            frozenset(("e", "s")): "┌",
            frozenset(("w", "s")): "┐",
            frozenset(("e", "n")): "└",
            frozenset(("w", "n")): "┘",
            frozenset(("n", "e", "w")): "┴",
            frozenset(("s", "e", "w")): "┬",
            frozenset(("n", "s", "e")): "├",
            frozenset(("n", "s", "w")): "┤",
            frozenset(("n", "s", "e", "w")): "┼",
        }
        return table.get(key, "┼")

    if v_style == "d" and h_style == "d":
        table = {
            frozenset(("e", "s")): "╔",
            frozenset(("w", "s")): "╗",
            frozenset(("e", "n")): "╚",
            frozenset(("w", "n")): "╝",
            frozenset(("n", "e", "w")): "╩",
            frozenset(("s", "e", "w")): "╦",
            frozenset(("n", "s", "e")): "╠",
            frozenset(("n", "s", "w")): "╣",
            frozenset(("n", "s", "e", "w")): "╬",
        }
        return table.get(key, "╬")

    # Mixed axis (Unicode-supported)
    if v_style == "s" and h_style == "d":
        table = {
            frozenset(("e", "s")): "╒",
            frozenset(("w", "s")): "╕",
            frozenset(("e", "n")): "╘",
            frozenset(("w", "n")): "╛",
            frozenset(("n", "s", "e")): "╞",
            frozenset(("n", "s", "w")): "╡",
            frozenset(("s", "e", "w")): "╤",
            frozenset(("n", "e", "w")): "╧",
            frozenset(("n", "s", "e", "w")): "╪",
        }
        return table.get(key, "╪")

    if v_style == "d" and h_style == "s":
        table = {
            frozenset(("e", "s")): "╓",
            frozenset(("w", "s")): "╖",
            frozenset(("e", "n")): "╙",
            frozenset(("w", "n")): "╜",
            frozenset(("n", "s", "e")): "╟",
            frozenset(("n", "s", "w")): "╢",
            frozenset(("s", "e", "w")): "╥",
            frozenset(("n", "e", "w")): "╨",
            frozenset(("n", "s", "e", "w")): "╫",
        }
        return table.get(key, "╫")

    return "┼"


def render_comment(
    base_points: list[tuple[int, int]],
    walls: list[tuple[tuple[int, int], tuple[int, int]]],
    *,
    cell_w: int = 5,
    cell_h: int = 2,
    prefix: str = "# ",
) -> str:
    if len(base_points) < 3:
        raise ValueError("base_points must contain at least 3 points.")

    # Avoid missing interior stroke rows/cols
    cell_w = max(2, cell_w)
    cell_h = max(2, cell_h)

    edges: dict[tuple[tuple[int, int], tuple[int, int]], Style] = {}

    # Base outline (double), split long segments
    closed = base_points + [base_points[0]]
    for p, q in zip(closed, closed[1:]):
        _add_segment_split(edges, p, q, "d")

    # Interior walls (single), split long segments  <-- THIS is the big fix for ╞ vs ╚/╔
    for p, q in walls:
        _add_segment_split(edges, p, q, "s")

    pts = {pt for edge in edges for pt in edge}
    xs = [x for x, _ in pts]
    ys = [y for _, y in pts]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    ww = (max_x - min_x) * cell_w + 1
    hh = (max_y - min_y) * cell_h + 1
    canvas = [[" " for _ in range(ww)] for _ in range(hh)]

    def to_canvas(pt: tuple[int, int]) -> tuple[int, int]:
        x, y = pt
        return (x - min_x) * cell_w, (y - min_y) * cell_h

    # Draw segments (fill between junction points)
    for (a, b), style in edges.items():
        (ax, ay), (bx, by) = a, b
        x1, y1 = to_canvas((ax, ay))
        x2, y2 = to_canvas((bx, by))

        if y1 == y2:
            ch = _hline(style)
            lo, hi = sorted((x1, x2))
            for x in range(lo + 1, hi):
                canvas[y1][x] = ch
        else:
            ch = _vline(style)
            lo, hi = sorted((y1, y2))
            for y in range(lo + 1, hi):
                canvas[y][x1] = ch

    # Build per-point adjacency for junctions
    adj: dict[tuple[int, int], dict[str, Style]] = {}
    for (a, b), style in edges.items():
        (ax, ay), (bx, by) = a, b
        if ax == bx:
            if by > ay:
                adj.setdefault((ax, ay), {})["s"] = style
                adj.setdefault((bx, by), {})["n"] = style
            else:
                adj.setdefault((ax, ay), {})["n"] = style
                adj.setdefault((bx, by), {})["s"] = style
        else:
            if bx > ax:
                adj.setdefault((ax, ay), {})["e"] = style
                adj.setdefault((bx, by), {})["w"] = style
            else:
                adj.setdefault((ax, ay), {})["w"] = style
                adj.setdefault((bx, by), {})["e"] = style

    # Place junction glyphs
    for pt, dirs in adj.items():
        cx, cy = to_canvas(pt)
        canvas[cy][cx] = _junction_char(dirs.get("n"), dirs.get("e"), dirs.get("s"), dirs.get("w"))

    # Emit comment block
    lines = ["".join(row).rstrip() for row in canvas]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()

    return "\n".join(prefix + line for line in lines)


def test_main_4():
    base_points = [
        (0, 0),
        (2, 0),
        (2, 2),
        (4, 2),
        (4, 0),
        (6, 0),
        (6, 3),
        (4, 3),
        (4, 4),
        (6, 4),
        (6, 7),
        (4, 7),
        (4, 5),
        (2, 5),
        (2, 7),
        (0, 7),
        (0, 4),
        (2, 4),
        (2, 3),
        (0, 3),
    ]
    interior_walls = [
        ((2, 1), (2, 6)),
        ((4, 6), (4, 1)),
    ]
    return base_points, interior_walls


def main_3a():
    base = [
        (0, 0),
        (2, 0),
        (2, 2),
        (1, 2),
        (1, 4),
        (2, 4),
        (2, 6),
        (1, 6),
        (1, 8),
        (2, 8),
        (2, 10),
        (0, 10),
    ]
    walls = [((1, 3), (1, 7))]
    return base, walls


def main_3():
    base = [
        (0, 0),
        (2, 0),
        (2, 1),
        (1, 1),
        (1, 2),
        (2, 2),
        (2, 3),
        (1, 3),
        (1, 4),
        (2, 4),
        (2, 5),
        (0, 5),
    ]
    walls = [((1, 1), (1, 4))]
    return base, walls


def main_2():
    base = [
        (0, 0),
        (4, 0),
        (4, 4),
        (0, 4),
    ]
    walls = [
        ((0, 0), (2, 0)),
        ((4, 2), (4, 4)),
        ((3, 4), (1, 4)),
        ((0, 4), (0, 0)),
        ((1, 1), (3, 1)),
        ((1, 3), (3, 3)),
        ((1, 1), (1, 3)),
        ((3, 1), (3, 3)),
    ]
    return base, walls


def main_1():
    base = [
        (0, 0),
        (2, 0),
        (2, 2),
        (4, 2),
        (4, 0),
        (6, 0),
        (6, 4),
        (0, 4),
    ]
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
    return base, walls


def main_0():
    base = [
        (0, 0),
        (3, 0),
        (3, 2),
        (0, 2),
    ]
    walls = [
        ((0, 0), (3, 0)),
        ((3, 0), (3, 2)),
        ((3, 2), (0, 2)),
        ((0, 2), (0, 0)),
        ((1, 0), (1, 2)),
        ((0, 1), (3, 1)),
        ((2, 1), (2, 2)),
    ]
    return base, walls


def simple_tray():
    base = [
        (0, 0),
        (1, 0),
        (1, 1),
        (0, 1),
    ]
    walls = [
        ((0, 0), (1, 0)),
        ((1, 0), (1, 1)),
        ((1, 1), (0, 1)),
        ((0, 1), (0, 0)),
    ]
    return base, walls


def main():
    base, walls = test_main_4()
    print(
        render_comment(
            base_points=base,
            walls=walls,
            cell_w=6,
            cell_h=2,
            prefix="#    ",
        )
    )


if __name__ == "__main__":
    main()
