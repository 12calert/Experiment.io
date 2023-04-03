from random import choice

def randomShape():
    shapes = ["circle", "rectangle", "square"]
    return choice(shapes)

def randomColour():
    colours = ['yellow', 'blue', 'green']
    return choice(colours)
