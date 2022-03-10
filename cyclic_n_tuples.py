def cyclic_n_tuples(seq, n=3, offset=-1):
    seq_len = len(seq)
    offset = seq_len + offset if offset < 0 else offset
    for i in range(offset, offset + seq_len):
        if (start := i % seq_len) < (end := (i + n) % seq_len):
            yield seq[start:end]
        else:
            yield seq[start:] + seq[:end]


def pair_wind(seq, wind=None):
    ind = None
    seq_len = len(seq) - 1
    for i in range(seq_len):
        if wind is not None:
            if wind:
                ind = (i == 0)
            else:
                ind = (i == seq_len)
        yield seq[i], seq[i + 1], ind
