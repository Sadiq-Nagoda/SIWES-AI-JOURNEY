from turtle import Turtle, Screen
screen = Screen()
import random

screen.setup(width=500, height=400,)

is_race_on = False
user_input = screen.textinput(title="Turtle race", prompt="choose your turle's color")
colors = ["red", "blue", "green", "yellow", "purple", "black"]
distance = [-100,-50, 0, 50, 100, 150]
all_turtles = []

for turtle_index in range(0,6):
    new_turtle = Turtle(shape = "turtle")
    new_turtle.penup()
    new_turtle.color(colors[turtle_index])
    new_turtle.goto(x=-230, y=distance[turtle_index])
    all_turtles.append(new_turtle)
    



if user_input:
    is_race_on = True


while is_race_on:

    for turtle in all_turtles:
        if turtle.xcor() > 230:
            is_race_on = False
            winning_color = turtle.pencolor()
            if winning_color == user_input:
                print(f"you've won, the {winning_color} is the winner!")
            else:
                print(f"you've lost, the {winning_color} is the winner!")
        rand_distance = random.randint(0, 10)
        turtle.forward(rand_distance)




























# tom = Turtle(shape = "turtle")
# tom.color("blue")
# tom.penup()
# tom.goto(x=-230, y=-50)


# mit = Turtle(shape = "turtle")
# mit.color("green")
# mit.penup()
# mit.goto(x=-230, y=0)


# mot = Turtle(shape = "turtle")
# mot.color("yellow")
# mot.penup()
# mot.goto(x=-230, y=50)


# jon = Turtle(shape = "turtle")
# jon.color("purple")
# jon.penup()
# jon.goto(x=-230, y=100)


# sim = Turtle(shape = "turtle")
# sim.color("black")
# sim.penup()
# sim.goto(x=-230, y=150)








screen.exitonclick()