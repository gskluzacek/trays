import random


def test():
    seq = "111 222 333 444 555 666 777 888 999 000".split()
    for i in cyclic_n_tuples(seq, 5,  -2):
        print(*i)


def cyclic_n_tuples(seq, n=3, offset=-1):
    seq_len = len(seq)
    offset = seq_len + offset if offset < 0 else offset
    for i in range(offset, offset + seq_len):
        if (start := i % seq_len) < (end := (i + n) % seq_len):
            yield seq[start:end]
        else:
            yield seq[start:] + seq[:end]


def gen2(seq, n=3, o=-1):
    m = len(seq)
    for i in range(m):
        start = i + o
        end = start + n
        print(start, end)
        if True:
            pass
        yield seq[start:] + seq[:end]


if __name__ == "__main__":
    test()
