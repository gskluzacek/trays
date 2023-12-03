import turtle

def main():
    print(turtle.pos())
    print(turtle.heading())
    # turtle.goto(10,10)
    # print(turtle.pos())
    # print(turtle.heading())
    d = turtle.towards(10,10 )
    print(turtle.pos())
    print(turtle.heading())
    print(d)

if __name__ == "__main__":
    main()