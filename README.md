How to compile the application locally:
1.	If you have not installed Django locally, please do to make sure you can render the app. Please follow the instructions based on your software on how to install Django here: https://docs.djangoproject.com/en/4.1/topics/install/ (or from any other resource you prefer)
2.	Open the submission folder called “DON’T FORGET TO ADD THE NAME of the directory which will include all the files of the app” to your preferable IDE (e.g., VScode).
3.	Open a terminal and type the following commands with the specified order:
  1)	python -m venv .venv
  2)	pip install -r requirements.txt
  3)	python manage.py migrate
  4)	python -m pip install -U channels["daphne"]
  5)	python manage.py runserver
4.	The app should be successfully running now locally, in http://127.0.0.1:8000/

