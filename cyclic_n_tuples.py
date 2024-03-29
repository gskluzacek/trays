def cyclic_n_tuples(seq, n=3, offset=-1):
    seq_len = len(seq)
    offset = seq_len + offset if offset < 0 else offset
    for i in range(offset, offset + seq_len):
        if (start := i % seq_len) < (end := (i + n) % seq_len):
            yield seq[start:end]
        else:
            yield seq[start:] + seq[:end]


def fwd_pair(seq):
    seq_len = len(seq) - 1
    for i in range(seq_len):
        yield seq[i], seq[i + 1]


def rev_pair(seq):
    seq_len = len(seq) - 1
    for i in range(seq_len, 0, -1):
        yield seq[i - 1], seq[i]


def fwd_n_tuple(seq, n=3):
    m = n - 1
    seq_len = len(seq) - m
    for i in range(seq_len):
        yield tuple(seq[i:i + n])
