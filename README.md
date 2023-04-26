# Experiment.io

## Project Description
This project aims to develop a web-based platform for clients to create experiments and gather data automatically. The website features the MapTask experiment which allows 2 players to co-operate to navigate through a map of obstacles. There are plans for further experiment development.

## Experiment Data JSON File Contents
The JSON file contains the following information:

- Details of experiment(s) conducted.
- The condition(s) under which the experiment(s) were conducted.
- The game(s) played with those conditions active.
- The moves taken throughout the process of the game.
- The chats that took place during the game.
- The "rects" field in the JSON specifies the rectangular boundaries for each obstacle. They are stored with their positional values, width, and height.

The moves are characterized by two types, "un" meaning undo and "mv" meaning move. They have an "oldpos" meaning the position before the move and "newpos" the position after the move.

## Technologies Used
This project was developed using Django, a Python-based web framework, along with HTML, CSS, and JavaScript. The database used for this project is postgreSQL.

## How to Run
To run this project, follow these steps:
1. Create a [virtual environment](https://docs.python.org/3/library/venv.html) able to run Python
2. Install the required dependencies by running **pip install -r requirements.txt**.
3. Run the development server using the command **python manage.py runserver**.

## How to Test
Tests are located in [tests.py](accounts/tests.py)

To test run the following command after cloning the repository and installing dependencies:\
**python manage.py test**

## How to Deploy Your Own Version
To deploy your own version, modify the values in [settings.py](game_website/settings.py) to suit your needs.
Depending on your hosting service other additions or modifications may be needed. Please make sure to check the official documentation from your hosting service.

## How You Can Contribute
If you want to contribute to this project, either get in touch with the team at u14ar20@abdn.ac.uk or choose one of the [open issues](https://github.com/12calert/ProjectCS3028/issues) in this repository and create a pull request with the proposed change. Someone from the team will review the code accordingly.
