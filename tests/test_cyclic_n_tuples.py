# import unittest
#
# import cyclic_n_tuples
#
#
# class TestCyclicNTuples(unittest.TestCase):
#     def test_offset_zero_pairs(self) -> None:
#         expected = [[1, 2], [2, 3], [3, 1]]
#         actual = list(cyclic_n_tuples.cyclic_n_tuples([1, 2, 3], n=2, offset=0))
#         self.assertEqual(expected, actual)
#
#     def test_negative_offset_wrap(self) -> None:
#         expected = [[3, 1], [1, 2], [2, 3]]
#         actual = list(cyclic_n_tuples.cyclic_n_tuples([1, 2, 3], n=2, offset=-1))
#         self.assertEqual(expected, actual)
#
#     def test_negative_offset_beyond_length(self) -> None:
#         expected = [[40, 10, 20], [10, 20, 30], [20, 30, 40], [30, 40, 10]]
#         actual = list(cyclic_n_tuples.cyclic_n_tuples([10, 20, 30, 40], n=3, offset=-5))
#         self.assertEqual(expected, actual)
#
#     def test_n_equal_length_returns_full_sequence(self) -> None:
#         expected = [[2, 3, 1], [3, 1, 2], [1, 2, 3]]
#         actual = list(cyclic_n_tuples.cyclic_n_tuples([1, 2, 3], n=3, offset=1))
#         self.assertEqual(expected, actual)
#
#     def test_tuple_input_preserves_tuple_chunks(self) -> None:
#         expected = [(1, 2), (2, 3), (3, 1)]
#         actual = list(cyclic_n_tuples.cyclic_n_tuples((1, 2, 3), n=2, offset=0))
#         self.assertEqual(expected, actual)
#
#
# if __name__ == "__main__":
#     unittest.main()

import pytest

from cyclic_n_tuples import cyclic_n_tuples, fwd_n_tuple, fwd_pair, rev_pair


class TestCyclicNTuples:
    def test_wraps_from_end_to_start_with_offset_0(self) -> None:
        assert list(cyclic_n_tuples([1, 2, 3], n=2, offset=0)) == [
            [1, 2],
            [2, 3],
            [3, 1],
        ]

    def test_negative_offset_is_converted(self) -> None:
        assert list(cyclic_n_tuples([1, 2, 3], n=2, offset=-1)) == [
            [3, 1],
            [1, 2],
            [2, 3],
        ]

    def test_negative_offset_beyond_length(self) -> None:
        assert list(cyclic_n_tuples([10, 20, 30, 40], n=3, offset=-5)) == [
            [40, 10, 20],
            [10, 20, 30],
            [20, 30, 40],
            [30, 40, 10],
        ]

    def test_negative_offset_beyond_length_2(self) -> None:
        assert list(cyclic_n_tuples([10, 20, 30, 40], n=3, offset=-6)) == [
            [30, 40, 10],
            [40, 10, 20],
            [10, 20, 30],
            [20, 30, 40],
        ]

    def test_n_equal_length_returns_full_sequence(self) -> None:
        assert list(cyclic_n_tuples([1, 2, 3], n=3, offset=1)) == [
            [2, 3, 1],
            [3, 1, 2],
            [1, 2, 3],
        ]

    def test_tuple_input_preserves_tuple_chunks(self) -> None:
        assert list(cyclic_n_tuples((1, 2, 3), n=2, offset=0)) == [(1, 2), (2, 3), (3, 1)]

    def test_works_with_strings_too(self) -> None:
        assert list(cyclic_n_tuples("abcd", n=3, offset=0)) == ["abc", "bcd", "cda", "dab"]

    def test_n_1_yields_singletons_in_order(self) -> None:
        assert list(cyclic_n_tuples([10, 20, 30], n=1, offset=0)) == [[10], [20], [30]]

    def test_empty_sequence_yields_nothing(self) -> None:
        assert list(cyclic_n_tuples([], n=2, offset=0)) == []


class TestFwdPair:
    def test_typical(self) -> None:
        assert list(fwd_pair([1, 2, 3, 4])) == [(1, 2), (2, 3), (3, 4)]

    def test_empty(self) -> None:
        assert list(fwd_pair([])) == []

    def test_singleton(self) -> None:
        assert list(fwd_pair([1])) == []


class TestRevPair:
    def test_typical(self) -> None:
        assert list(rev_pair([1, 2, 3, 4])) == [(3, 4), (2, 3), (1, 2)]

    def test_empty(self) -> None:
        assert list(rev_pair([])) == []

    def test_singleton(self) -> None:
        assert list(rev_pair([1])) == []


class TestFwdNTuple:
    def test_window_3(self) -> None:
        assert list(fwd_n_tuple([1, 2, 3, 4], n=3)) == [(1, 2, 3), (2, 3, 4)]

    def test_n_larger_than_length_yields_nothing(self) -> None:
        assert list(fwd_n_tuple([1, 2], n=3)) == []

    def test_n_1_yields_singletons_as_tuples(self) -> None:
        assert list(fwd_n_tuple([7, 8, 9], n=1)) == [(7,), (8,), (9,)]
