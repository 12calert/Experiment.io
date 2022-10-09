import turtle # for python graphics
from turtle import Screen
import random # for generating random numbers

t = turtle.Turtle() # creatng a turtle pen
screen = Screen()

#Draw a square
def draw_square(length):
    for i in range(0,4):
        t.forward(length)
        t.right(90) # move cursor in an angle of 90 degrees
    
#Draw an equilateral triangle
def draw_equilateral_triangle(length):
    t.forward(length) # draw base
    t.left(120) # move cursor in an angle of 120 degrees
    
    t.forward(length)
    t.left(120) # move cursor in an angle of 120 degrees
    
    t.forward(length)
    
def draw_circle(radius):
    t.circle(radius)
    
# Change the size of python screen/box (play around what is the best to be fit in the website)
screen.setup(1000,900)
t.penup()
t.goto(random.randint(-350,0), random.randint(-250,0))
t.pendown()
# set the fillcolor
t.fillcolor("green")
# start the filling color
t.begin_fill()
draw_equilateral_triangle(random.randint(10,200))
# ending the filling of the color
t.end_fill()
t.penup()
t.goto(random.randint(0,350), random.randint(0,250))
t.pendown()
# set the fillcolor
t.fillcolor("blue")
# start the filling color
t.begin_fill()
draw_circle(random.randint(10,200))
# ending the filling of the color
t.end_fill()
t.penup()
t.goto(random.randint(0,350), random.randint(-250,0))
t.pendown()
# set the fillcolor
t.fillcolor("red")
# start the filling color
t.begin_fill()
draw_square(random.randint(20,120))
# ending the filling of the color
t.end_fill()
turtle.Screen().exitonclick() 
