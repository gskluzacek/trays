from itertools import permutations


def perm(val_list):
    return perm_r(val_list, 1)


def swap(val_list, pos):
    l = pos - 1
    r = pos
    print(f"  {l}, {r}")
    val_list[l], val_list[r] = val_list[r], val_list[l]
    return val_list


def perm_r(val_list, pos):
    print(f"{val_list}, {pos}")
    while pos < len(val_list):
        pos += 1
        val_list = perm_r(val_list, pos)
        print(val_list)
        val_list = swap(val_list, pos)
    return val_list


def main():
    # perm = permutations([1, 2, 3, 4, 5])

    # for i in list(perm):
    #     print (i)

    """

    print the string
    swap the last 2 element


    """
    a = [1, 2, 3]
    perm(a)


if __name__ == "__main__":
    main()
