# Experiment.io

## Project Description
This project aims to develop a web-based game with various experimental conditions for research purposes. The game allows players to navigate through obstacles and solve puzzles. The data collected during gameplay will be used for research purposes.

## Technologies Used
This project was developed using Django, a Python-based web framework, along with HTML, CSS, and JavaScript. The database used for this project is postgreSQL.

## How to Run
To run this project, follow these steps:

1. Install the required dependencies by running **pip install -r requirements.txt**.
2. Run the development server using the command **python manage.py runserver**.

## JSON File Contents
The JSON file contains the following information:

- Details of experiment(s) conducted.
- The condition(s) under which the experiment(s) were conducted.
- The game(s) played with those conditions active.
- The moves taken throughout the process of the game.
- The chats that took place during the game.
- The "rects" field in the JSON specifies the rectangular boundaries for each obstacle. They are stored with their positional values, width, and height.

The moves are characterized by two types, "un" meaning undo and "mv" meaning move. They have an "oldpos" meaning the position before the move and "newpos" the position after the move.

We would provide a way for the researcher to recreate the games either within our website or by giving them a package (possible in any programming language) that they can use to recreate it on their own without having to use the website.