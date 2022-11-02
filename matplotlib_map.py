import matplotlib.pyplot as plt
import numpy as np
from random import randint
from math import floor, ceil

maxwidth = 1000
maxheight = 1000
shapes = []
amountOfShapes = 3
# create grid
plt.axes()

# split the grid into equal parts to place shapes
# split screen into two, place floor(n/2) shapes in the top half and ceil(n/2) shapes in the bottom half
# note: this will look very ugly for high amounts of shapes we are only splitting by height once, will extend later
# we assume we are placing two or more shapes
shapesCoordRange = [] #keep track of the coordinates to place the shapes
tempH = maxheight/2  # halfway up the screen (for now)
amountTop = floor(amountOfShapes/2)  # amount of shapes to place in the top
amountBot = ceil(amountOfShapes/2)  # amount of shapes to place in the bottom
incrementTop = maxwidth/amountTop   # how much space each shape gets in the top
incrementBot =  maxwidth/amountBot  # how much space each shapes gets in the bottom

#place the first shape
shapesCoordRange.append((0,incrementTop,tempH,maxheight))
placed = 1

# find the coords for the top shapes
# loop until we place every shape in the top
while(placed != amountTop):
    # append the tuple of the range of coordinates to list where:
    # (startX,endX,startY,endY)
    shapesCoordRange.append((shapesCoordRange[-1][1],shapesCoordRange[-1][1]+incrementTop,tempH,maxheight))
    placed += 1

#place the first shape on the bottom row
shapesCoordRange.append((0,incrementBot,0,tempH))
placed += 1

#the same but for the bottom row
while(placed != amountOfShapes):
    shapesCoordRange.append((shapesCoordRange[-1][1],shapesCoordRange[-1][1]+incrementBot,0,tempH))
    placed += 1

#create shape objects
# loop throught the shape coordinate ranges in the list
# place the shape somewhere randomly withing the range of the two integers for x and y
# <------------ note: only places cirlces for now and of only one colour, can easily be 
# extended to place differing shapes and colours, will do this is if we decide to use this implementation of the map ------------>
for shapeCoord in shapesCoordRange:
    circle = plt.Circle((randint(shapeCoord[0],shapeCoord[1]), randint(shapeCoord[2],shapeCoord[3])), radius=100, fc='y')
    print(shapeCoord[0],shapeCoord[1],shapeCoord[2],shapeCoord[3])
    shapes.append(circle)


#add shapes to grid
for i in shapes:
    plt.gca().add_patch(i)

# turn off axis labels and 'zoom' out
plt.axis('off')
plt.axis('scaled')

#define axis limits
plt.xlim([0, maxwidth])
plt.ylim([0,maxheight])

#show the map
plt.show()
