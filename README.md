How to run:
1. First, you might want to create venv
2. pip install -r requirements.txt
3. python manage.py runserver

JSON file contents:
lists details of experiment(s), their condition(s), the game(s) played with those conditions active, the moves taken throughout the process of the game, as well as the chats
The "rects" field specifies the rectangular boundaroes for each obstacle, they are stored with their positional values and width and height. 
The moves are characterised with 2 types, "un" meaning undo and "mv" meaning move. They have an "oldpos" meaning the position before the move and "newpos" the position after the move.

^^^^ this would be given to the researcher at some point when before/when they download the json of the data.
