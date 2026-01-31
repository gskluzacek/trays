import turtle as t


def main():
    print(t.pos())
    print(t.heading())
    # t.goto(10,10)
    # print(t.pos())
    # print(t.heading())
    d = t.towards(10,10 )
    print(t.pos())
    print(t.heading())
    print(d)
    t.mainloop()


if __name__ == "__main__":
    main()