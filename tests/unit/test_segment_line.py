from tray.geometry.basic.point import Point
from tray.geometry.intersection import Intersection
from tray.geometry.segment.segment_line import SegLnInterxn, SegmentLine
from tray.geometry.types.tray import IntrxnType, JointType


def test_segment_line_init():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    jt = JointType.TS
    sl = SegmentLine(p1, p2, jt)
    assert sl.p1 == p1
    assert sl.p2 == p2
    assert sl.joint_type == jt
    assert sl.intersections == []


def test_segment_line_intersections_can_store_seg_ln_intersections():
    sl = SegmentLine(Point(0, 0), Point(10, 0), JointType.TS)
    pt_chk = Point(5, 0)
    intrxn = Intersection(Point(5, 1), IntrxnType.TEE_T)
    seg_ln_intrxn = SegLnInterxn(pt_chk=pt_chk, intrxn=intrxn)

    sl.intersections.append(seg_ln_intrxn)

    assert sl.intersections == [seg_ln_intrxn]


def test_seg_ln_interxn_dataclass_fields_and_repr():
    pt_chk = Point(1, 2)
    intrxn = Intersection(Point(3, 4), IntrxnType.CROSS)

    seg_ln_intrxn = SegLnInterxn(pt_chk=pt_chk, intrxn=intrxn)

    assert seg_ln_intrxn.pt_chk == pt_chk
    assert seg_ln_intrxn.intrxn == intrxn
    assert repr(seg_ln_intrxn) == "SegLnInterxn(pt_chk=Point(x=1, y=2), intrxn=Intersection((3, 4), IntrxnType.CROSS))"


def test_seg_ln_interxn_dataclass_equality():
    pt_chk = Point(1, 2)
    intrxn = Intersection(Point(3, 4), IntrxnType.CROSS)

    left = SegLnInterxn(pt_chk=pt_chk, intrxn=intrxn)
    right = SegLnInterxn(pt_chk=pt_chk, intrxn=intrxn)

    assert left == right


def test_segment_line_repr():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    jt = JointType.TS
    sl = SegmentLine(p1, p2, jt)
    expected = "SegmentLine(p1=(0, 0), p2=(10, 0), orientation=LineOrientation.HORZ, joint_type=JointType.TS)"
    assert repr(sl) == expected


def test_segment_line_str():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    jt = JointType.TS
    sl = SegmentLine(p1, p2, jt)
    expected = "[(0, 0), (10, 0), LineOrientation.HORZ, JointType.TS]"
    assert str(sl) == expected
