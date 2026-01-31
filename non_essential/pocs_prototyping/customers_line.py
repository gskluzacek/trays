import random


def main2():
    q = []
    at = random.randint(1, 10)
    count = 0
    for i in range(1, 721):
        print(i)
        if i == at:
            count += 1
            print(f"customer {count} arrived at {i}")


def main():
    vals = list(range(1, 34))
    print(len(vals))
    print("-" * 100)
    for i, n in enumerate(vals):
        print(f"[{str(i).zfill(2)}, {str(n).zfill(2)}], ", end="")
        if (i + 1) % 10 == 0:
            print("*\n", end="")
    if len(vals) % 10 != 0:
        print("#\n", end="")
    print("-" * 100)


if __name__ == "__main__":
    main()
