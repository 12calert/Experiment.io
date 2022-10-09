import turtle # for python graphics
import random # for generating random numbers

t = turtle.Turtle()
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
    
    


draw_square(random.randint(10,200))
t.penup()
t.goto(random.randint(-350,350), random.randint(-250,250))
t.pendown()
draw_equilateral_triangle(random.randint(10,200))
t.penup()
t.goto(random.randint(-350,350), random.randint(-250,250))
t.pendown()
draw_circle(random.randint(10,200))
turtle.Screen().exitonclick() 

 