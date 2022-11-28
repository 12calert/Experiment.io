How to compile the application locally:
1.	If you have not installed Django locally, please do to make sure you can render the app. Please follow the instructions based on your software on how to install Django here: https://docs.djangoproject.com/en/4.1/topics/install/ (or from any other resource you prefer)
2.	Open the submission folder called “ProjectCS3028” to your preferable IDE (e.g., VScode).
3.	Open a terminal and type the following commands in the specified order:
  1)	python -m venv .venv
  
  If you using the latest version of VScode is going to ask you if you want the new environment to be selected for the workspace folder. Please select yes, otherwise select it manually based on your IDE. Make sure the virtual environment is running, otherwise you won't be able to host the application. (Caveat: virtual environments don't work in PowerShell which might be your IDE defaulted to).
  
  
  2)	pip install -r requirements.txt
  3)	python manage.py migrate
  4)	python -m pip install -U channels["daphne"]
  5)	python manage.py runserver
4.	The app should be successfully running now locally, in http://127.0.0.1:8000/

In case you are struggling please kindly email one of the team members for further instructions and guidance here: a.konstantinou.20@abdn.ac.uk 
