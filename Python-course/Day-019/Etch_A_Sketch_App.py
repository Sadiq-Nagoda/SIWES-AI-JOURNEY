from turtle import Turtle, Screen

tim = Turtle()
screen = Screen()
tim.speed("fastest")


def move_forwards():
    tim.forward(15)
def move_backwards():
    tim.backward(15)
def move_counter_clockwise():
    new_heading = tim.heading() + 15
    tim.setheading(new_heading)

def move_clockwise():
    new_heading = tim.heading() - 15
    tim.setheading(new_heading)
    
def clear():
    tim.clear()
    tim.penup()
    tim.home()
    

screen.listen()
screen.onkey( move_forwards, "f")
screen.onkey( move_backwards,  "b")
screen.onkey( move_counter_clockwise, "a")
screen.onkey( move_clockwise, "e")
screen.onkey( clear, "c")












screen.exitonclick()