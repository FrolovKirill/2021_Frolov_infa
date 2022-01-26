import turtle as t


def star(n, length):
    for _ in range(n):
        t.forward(length)
        t.right(180 * (n - 1) / n)


t.shape("turtle")
t.speed(5)
t.penup()
t.goto(-250, 0)
t.pendown()
star(10, 200)

t.penup()
t.goto(50, 0)
t.pendown()
star(11, 200)
t.exitonclick()
