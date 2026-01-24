from typing import Protocol, Self, TypeVar, overload
from collections.abc import Iterator, Sequence

T = TypeVar("T")


class Chunk(Protocol[T]):
    """A slice result that can be concatenated with another slice result of the same type."""

    def __len__(self) -> int: ...

    @overload
    def __getitem__(self, index: int, /) -> T: ...

    @overload
    def __getitem__(self, index: slice, /) -> Self: ...

    def __add__(self, other: Self, /) -> Self: ...


class WrapSequence(Protocol[T]):
    """Minimal interface for cyclic slicing and concatenation."""

    def __len__(self) -> int: ...

    @overload
    def __getitem__(self, index: int, /) -> T: ...

    @overload
    def __getitem__(self, index: slice, /) -> Chunk[T]: ...


def cyclic_n_tuples(seq: WrapSequence[T], n: int = 3, offset: int = -1) -> Iterator[Chunk[T]]:
    """
    Staring at offset, loops over seq yielding chunks of length n, wrapping around the end back to the beginning if necessary.
    Starting at `offset`, yield chunks of length `n`, wrapping around the end to the beginning as needed.

    :param seq: The list of elements to loop over.
    :param n: The number of elements to `yield` as a chunk for each iteration of the loop.
    :param offset: Index where the iteration starts. If negative, it’s converted to a positive index.
    :return: An iterator yielding chunks of length `n`.

    Will return the same number of chunks as there are elements in seq.

    Doctest examples:
    >>> list(cyclic_n_tuples([1, 2, 3], n=2, offset=0))
    [[1, 2], [2, 3], [3, 1]]
    >>> list(cyclic_n_tuples((1, 2, 3), n=2, offset=0))
    [(1, 2), (2, 3), (3, 1)]
    >>> list(cyclic_n_tuples("abcd", n=3, offset=0))
    ['abc', 'bcd', 'cda', 'dab']
    >>> list(cyclic_n_tuples([1, 2, 3], n=2, offset=-1))
    [[3, 1], [1, 2], [2, 3]]
    """
    # stores the length of seq
    seq_len = len(seq)
    # if negative, convert to positive index
    offset = seq_len + offset if offset < 0 else offset

    # Iterate over each element of seq, beginning from the offset index.
    # We are implementing wrapping so i may be greater than seq_len.
    # The resulting list is exclusive of the end value.
    for i in range(offset, offset + seq_len):
        # calculate start and end indices for the current chunk
        # for start: if i greater than seq_len, then start is wrapped by using the modulo operator
        # for end: if i + n is greater than seq_len, then end is wrapped by using the modulo operator
        if (start := i % seq_len) < (end := (i + n) % seq_len):
            # if start is less than end then yield the slice defined by the start and end indices
            yield seq[start:end]
        else:
            # else yield the concatenation of 2 slices:
            # slice 1: the start index to the end of seq
            # slice 2: the beginning of seq to the end index
            yield seq[start:] + seq[:end]


def fwd_pair(seq: Sequence[T]) -> Iterator[tuple[T, T]]:
    """
    Loops over seq yielding pairs of adjacent elements.
    :param seq: The list of elements to loop over.
    :return: An iterator yielding adjacent pairs.

    The first pair yielded will be (seq[0], seq[1])
    The last pair yielded will be (seq[-2], seq[-1])

    If there are n elements in seq, then n-1 pairs will be yielded.

    Note for seq with length 0 or 1, no pairs will be yielded.

    Doctest examples:
    >>> list(fwd_pair([1, 2, 3, 4]))
    [(1, 2), (2, 3), (3, 4)]
    >>> list(fwd_pair([1]))
    []
    """
    # The end of the range specified is the length of seq minus 1
    range_end = len(seq) - 1

    # The resulting list is exclusive of the end value
    for i in range(range_end):
        yield seq[i], seq[i + 1]


def rev_pair(seq: Sequence[T]) -> Iterator[tuple[T, T]]:
    """
    Loops over seq backwards yielding pairs of adjacent elements.
    :param seq: The list of elements to loop over.
    :return: An iterator yielding adjacent pairs in reverse order.

    The first pair yielded will be (seq[-2], seq[-1])
    The last pair yielded will be (seq[0], seq[1])

    If there are n elements in seq, then n-1 pairs will be yielded.

    Note for seq with length 0 or 1, no pairs will be yielded.

    Doctest examples:
    >>> list(rev_pair([1, 2, 3, 4]))
    [(3, 4), (2, 3), (1, 2)]
    >>> list(rev_pair([]))
    []
    """
    # The start of the range specified is the length of seq minus 1.
    # The resulting list is inclusive of the start value.
    # Since the first pair yielded have indexes of i-1 and i,
    # we must start at the last index minus 1.
    range_start = len(seq) - 1

    # The range is specified with a step value of -1 (i.e., backwards).
    # The resulting list is exclusive of the end value 0 (i.e., a value of 1).
    for i in range(range_start, 0, -1):
        yield seq[i - 1], seq[i]


def fwd_n_tuple(seq: Sequence[T], n: int = 3) -> Iterator[tuple[T, ...]]:
    """
    Loops over seq yielding tuples of length n.

    :param seq: The list of elements to loop over.
    :param n: The number of elements to `yield` as a chunk for each iteration of the loop.
    :return: An iterator yielding tuples of length `n`.

    If there are j elements in seq, then j - n + 1 tuples will be yielded.

    Doctest examples:
    >>> list(fwd_n_tuple([1, 2, 3, 4], n=3))
    [(1, 2, 3), (2, 3, 4)]
    >>> list(fwd_n_tuple([1, 2], n=3))
    []
    """
    # the max index that we iterate up to is the length of seq minus 1
    # however, the resulting list is exclusive of the end value, so we must add 1 to the range end value.
    range_end = len(seq) - n + 1
    for i in range(range_end):
        yield tuple(seq[i:i + n])
