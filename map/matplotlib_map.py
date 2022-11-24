import matplotlib.pyplot as plt
import numpy as np
from random import randint, choice
from math import floor, ceil

def run():
    #can be changed depending on screen size etc. code should be robust enough to account for changing values
    maxwidth = 1000
    maxheight = 1000
    shapesToChoose = ["circle","square","rectangle","triangle"]
    colours = ["g","b","r","y"]
    shapes = []
    amountOfShapes = 3
    # should each shape/colour be distinct (just some examples of restrictions that researchers can define
    distinctShape = True
    distinctColour = True
    #define the size of the shapes note: can be changed later, right now it depends on the screen size
    size = ((1/ceil(amountOfShapes/2))*maxwidth/2)
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
    # loop until we place every shape we need to in the top
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
    # <------------- extended to place any of threee shapes and pick one of the 4 random colours,
    # can be made better by using objects --------->
    for shapeCoord in shapesCoordRange:
        # pick random shape and colour from the lists of available
        shape = choice(shapesToChoose)
        colour = choice(colours)
        # if the researcher instructs each shape to be different...
        if (distinctShape):
            shapesToChoose.remove(shape)
        # if the researcher instructs each colour to be different...
        if (distinctColour):
            colours.remove(colour)
        # if using python version predating 3.10 uncomment this (switch statements not supported in older versions)
        """if shape == "circle":
            newShape = plt.Circle((randint(shapeCoord[0]+size/2,shapeCoord[1]-size/2), randint(shapeCoord[2]+size/2,shapeCoord[3]-size/2)), size/2, fc=colour)
        elif shape == "rectangle":
            newShape = Rectangle((randint(shapeCoord[0],shapeCoord[1]-size), randint(shapeCoord[2],shapeCoord[3]-size/2)), size, size/2, fc=colour)
        elif shape == "square":
            newShape = Rectangle((randint(shapeCoord[0],shapeCoord[1]-size),randint(shapeCoord[2],shapeCoord[3]-size)), size, size, fc=colour)

        shapes.append(newShape)"""
        match shape:
            case "circle":
                newShape = plt.Circle((randint(shapeCoord[0]+size/2,shapeCoord[1]-size/2), randint(shapeCoord[2]+size/2,shapeCoord[3]-size/2)), radius = size/2, color = colour)
            case "rectangle":
                newShape = plt.Rectangle((randint(shapeCoord[0],shapeCoord[1]-size), randint(shapeCoord[2],shapeCoord[3]-size/2)), width = size, height = size/2, color = colour)
            case "square":
                newShape = plt.Rectangle((randint(shapeCoord[0],shapeCoord[1]-size),randint(shapeCoord[2],shapeCoord[3]-size)), width = size, height = size, color = colour)
            case "triangle":
                # we need the three coordinates for the point of the triangle then make a polygon with those points
                tempx = randint(shapeCoord[0],shapeCoord[1]-size)
                tempy = randint(shapeCoord[2],shapeCoord[3]-size)
                p = np.array([[tempx,tempy],[tempx+size,tempy],[tempx+size/2,tempy+size]])
                newShape = plt.Polygon(p[:3,:],color=colour)
        shapes.append(newShape)

    #add shapes to grid
    for i in shapes:
        plt.gca().add_patch(i)

    # turn off axis labels and 'zoom' out
    plt.axis('off')
    plt.axis('scaled')

    #define axis limits
    plt.xlim([0, maxwidth])
    plt.ylim([0,maxheight])
    return plt

#not particularly modular or efficient
for i in range(10):
    generatedMap = run()
    name = "map"+str(i)+".png"
    generatedMap.savefig(name)
    generatedMap.clf()


