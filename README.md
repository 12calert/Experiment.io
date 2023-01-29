How to run:
1. First, you might want to create venv
2. pip install -r requirements.txt
3. python manage.py runserver

What works:
1. /game_website - root app
2. /assets - images and css/js files available in html with the use of Django template language, eg. "{% static 'css/home.css' %}" or "{% static 'js/example.js' %}"
3. /templates - stores html files

Placeholders:
1. /accounts - holds db schema, login and registration logic - it will be useful later
2. /chat - tutorial copied 1 to 1 by Athena - it won't be of any use unless heavily modified


TODO:
1. Pretty much implement the entire frontend
  - start with the home page
  - make a view where the actualy game takes place
  - other useful ones such as "about"
  - login for researchers and their view ( eg. statistics.html )
2. Modify/Remake the chat in a way that is actually relevant to our needs
3. Design db schema ( not only what we need to store, but it needs to be in depth, specifically naming tables and relations between them )
4. Gameplay logic
5. Statistics - pulled from db and displayed in a nice way to the researchers
6. Last semester I got blamed for everything, so this time you've got the chance to shine