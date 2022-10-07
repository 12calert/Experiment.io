# Mapp generation for CS3026 group project
# TODO:
# - Add classes for other shapes, add possible heirarchical class structure
# i.e. Shapes is the parent class, all the other shapes are subclasses
# - Figure how to randomly place shapes in the grid (packing example may help to
# check if shapes overlap)  ---- I don't have my code anymore unfortunately
import random

class Map():
    """ class which holds information of the map """
    def __init__(self, length, depth, noOfObstacles):
        self.length = length
        self.depth = depth
        self.noOfObstacles = noOfObstacles
        self.map = [[0 for i in range(self.length)] for j in range(self.depth)]
        # stores the position of the free spaces, so we can more efficiently compute
        # where to place obstacles

    def initialiseMap(self, noOfObstacles):
        """Initalises the map, takes the noOfObstacles, and places them into the map,
        start with simple functionality and add complexity later"""
        #generate the shapes of random sizes
        shapes = [None]*noOfObstacles
        for i in range(noOfObstacles):
            shapes[i] = Square(random.randint(2,5))
        # pick a random spot in the grid (of spaces that are free). Try place the shape.
        #If not try some other spot, check if the obstacle would fit
        placed = False
        shapeWidth = shapes[i].getWidth()
        shapeHeight = shapes[i].getHeight()

    def printMap(self):
        """Prints the content of the map to the terminal, just
        now only used for testing purposes"""
        for i in range(self.length):
            for j in range(self.depth):
                print(self.map[i][j],end=" ")
            print()

class Square:
    def __init__(self,width):
        self.width = width
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.width
# Below is for testing purposes only
# values can be changed later
length = 20
depth = 20
noOfObstacles = 3
map = Map(length,depth,noOfObstacles)
map.initialiseMap(noOfObstacles)
map.printMap()
# variable map stores the n by n matrix
