from django.test import TestCase, Client
from .models import Researcher, Chat, Experiment, Condition, Game, Move
from game_website.forms import ResearcherRegisterForm
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from game_website.views import intersect, outOfBounds, place, initialPlayer, setScreensize, saveMove, viewChats, viewConditions, saveMessage, acceptTOS, decrementUsers, is_ajax, viewGames
from django.http import HttpRequest
from django.test import TestCase, RequestFactory, Client # RequestFactory to simulate POST requests.


# Testing of Researcher registration
class ResearcherRegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'username': 'johndoe',
            'password1': 'Testpassword123',
            'password2': 'Testpassword123',
        }
        self.invalid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'username': 'johndoe',
            'password1': 'Testpassword123',
            'password2': 'Differentpassword123',
        }
        self.missing_field_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'username': '',
            'password1': 'Testpassword123',
            'password2': 'Testpassword123',
        }
        self.weak_password_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'username': 'johndoe',
            'password1': 'password',
            'password2': 'password',
        }

    def test_researcher_registration_page_render(self):
        response = self.client.get('/researcher_registration/')
        self.assertEqual(response.status_code, 200) # Still on the registration page
        self.assertTemplateUsed(response, 'researcher_registration.html')
        self.assertIsInstance(response.context['register'], ResearcherRegisterForm)

    def test_researcher_registration_valid_data(self):
        response = self.client.post('/researcher_registration/', self.valid_data)
        self.assertEqual(response.status_code, 302)  # Redirected to the home page
        self.assertTrue(User.objects.filter(username='johndoe').exists())
        user = User.objects.get(username='johndoe')
        self.assertTrue(Researcher.objects.filter(userkey=user).exists())

    def test_researcher_registration_invalid_data(self):
        response = self.client.post('/researcher_registration/', self.invalid_data)
        self.assertEqual(response.status_code, 200)  # Still on the registration page
        self.assertTemplateUsed(response, 'researcher_registration.html')
        self.assertFalse(User.objects.filter(username='johndoe').exists())
        self.assertFalse(Researcher.objects.filter(userkey__username='johndoe').exists())

    def test_researcher_registration_missing_field(self):
        response = self.client.post('/researcher_registration/', self.missing_field_data)
        self.assertEqual(response.status_code, 200) # Still on the registration page
        self.assertTemplateUsed(response, 'researcher_registration.html')
        self.assertFalse(User.objects.filter(email='john.doe@example.com').exists())
        self.assertFalse(Researcher.objects.filter(userkey__email='john.doe@example.com').exists())

    def test_researcher_registration_duplicate_username(self):
        User.objects.create_user(username='johndoe', email='john.doe@example.com', password='Testpassword123')

        response = self.client.post('/researcher_registration/', self.valid_data)
        self.assertEqual(response.status_code, 200) # Still on the registration page
        self.assertTemplateUsed(response, 'researcher_registration.html')
        self.assertEqual(User.objects.filter(username='johndoe').count(), 1)
        self.assertFalse(Researcher.objects.filter(userkey__email='john.doe@example.com').exists())

    def test_researcher_registration_weak_password(self):
        response = self.client.post('/researcher_registration/', self.weak_password_data)
        self.assertEqual(response.status_code, 200) # Still on the registration page
        self.assertTemplateUsed(response, 'researcher_registration.html')
        self.assertFalse(User.objects.filter(username='johndoe').exists())
        self.assertFalse(Researcher.objects.filter(userkey__username='johndoe').exists())

# Testing of Researcher login
class ResearcherLoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='johndoe',
            email='john.doe@example.com',
            password='Testpassword123',
            first_name='John',
            last_name='Doe',
        )
        Researcher.objects.create(userkey=self.user)

        self.valid_credentials = {
            'username': 'johndoe',
            'password': 'Testpassword123',
        }
        self.invalid_credentials = {
            'username': 'johndoe',
            'password': 'WrongPassword',
        }

    def test_researcher_login_page_render(self):
        response = self.client.get('/researcher_login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'researcher_login.html')

    def test_researcher_login_valid_credentials(self):
        response = self.client.post('/researcher_login/', self.valid_credentials)
        self.assertEqual(response.status_code, 302)  # Redirected after successful login

    def test_researcher_login_invalid_credentials(self):
        response = self.client.post('/researcher_login/', self.invalid_credentials)
        self.assertEqual(response.status_code, 200)  # Still on the login page
        self.assertTemplateUsed(response, 'researcher_login.html')
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid username or password.')

class UtilityFunctionsTest(TestCase):
    # Testing of test_intersect function
    def test_intersect(self):
        # Check if 2 objects are intersecting
        r1 = {"left": 0, "top": 0, "width": 10, "height": 10}
        r2 = {"left": 5, "top": 5, "width": 10, "height": 10}
        self.assertTrue(intersect(r1, r2))

        # Check if 2 objects are not intersecting
        r3 = {"left": 15, "top": 15, "width": 10, "height": 10}
        self.assertFalse(intersect(r1, r3))

        # 2 objects sharing an edge but not intersecting
        r4 = {"left": 10, "top": 0, "width": 10, "height": 10}
        self.assertFalse(intersect(r1, r4))

        # 2 objects sharing a corner but not intersecting
        r5 = {"left": 10, "top": 10, "width": 10, "height": 10}
        self.assertFalse(intersect(r1, r5))

        # Objects with negative coordinates intersecting
        r1 = {"left": -5, "top": -5, "width": 10, "height": 10}
        r2 = {"left": -3, "top": -3, "width": 10, "height": 10}
        self.assertTrue(intersect(r1, r2))

        # Objects with negative coordinates not intersecting
        r3 = {"left": -15, "top": -15, "width": 10, "height": 10}
        self.assertFalse(intersect(r1, r3))
        
    # Testing of test_outOfBounds function
    def test_outOfBounds(self):
        # Object completely out of bounds
        obj1 = {"left": -20, "top": -20, "width": 10, "height": 10}
        containerWidth = 800
        self.assertTrue(outOfBounds(obj1, containerWidth))

        # Object partially out of bounds
        obj2 = {"left": 790, "top": 0, "width": 20, "height": 20}
        self.assertTrue(outOfBounds(obj2, containerWidth))

        # Object completely within bounds
        obj3 = {"left": 100, "top": 100, "width": 10, "height": 10}
        self.assertFalse(outOfBounds(obj3, containerWidth))

        # Object partially out of bounds on the top edge
        obj1 = {"left": 10, "top": -5, "width": 10, "height": 10}
        containerWidth = 800
        self.assertTrue(outOfBounds(obj1, containerWidth))

        # Object partially out of bounds on the bottom edge
        obj2 = {"left": 10, "top": 545, "width": 10, "height": 10}
        self.assertTrue(outOfBounds(obj2, containerWidth))
        
    # Testing of test_place function
    def test_place(self):
        containerWidth = 800
        # Object intersecting with an obstacle and out of bounds
        obj4 = {"left": 790, "top": 100, "width": 20, "height": 20}
        obstacle1 = {"left": 800, "top": 100, "width": 10, "height": 10}
        obstacles = [obstacle1]
        self.assertFalse(place(obj4, obstacles, containerWidth))
        
        # Object placeable with multiple obstacles
        obj1 = {"left": 50, "top": 50, "width": 10, "height": 10}
        obstacle1 = {"left": 0, "top": 0, "width": 10, "height": 10}
        obstacle2 = {"left": 100, "top": 100, "width": 10, "height": 10}
        obstacles = [obstacle1, obstacle2]
        self.assertTrue(place(obj1, obstacles, containerWidth))

        # Object not placeable because of intersection with one of the obstacles
        obj2 = {"left": 5, "top": 5, "width": 10, "height": 10}
        self.assertFalse(place(obj2, obstacles, containerWidth))

        # Object not placeable because of being out of bounds
        obj3 = {"left": 900, "top": 900, "width": 10, "height": 10}
        self.assertFalse(place(obj3, obstacles, containerWidth))

        # Object not placeable because of intersection with one of the obstacles and being out of bounds
        obj4 = {"left": 800, "top": 0, "width": 20, "height": 20}
        obstacle3 = {"left": 810, "top": 0, "width": 10, "height": 10}
        obstacles.append(obstacle3)
        self.assertFalse(place(obj4, obstacles, containerWidth))

# Testing for saveMove() function in views file
class ViewFunctionsTest(TestCase):
    def setUp(self):
        # Create a User object
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Use the created User object when creating the Researcher object
        self.researcher = Researcher.objects.create(userkey=self.user)

        # Set up RequestFactory and Client for testing requests
        self.factory = RequestFactory()
        self.client = Client()

        # Create objects for testing: Experiment, Condition, and Game
        self.experiment = Experiment.objects.create(name="Test Experiment", created_by=self.researcher)
        self.condition = Condition.objects.create(amount_item=2, created_by=self.researcher, name="Test Condition", experiment=self.experiment)
        self.game = Game.objects.create(has_condition=self.condition, public=True)

        # Create a session object for testing
        self.session = self.client.session
        self.session.save()
    
    # Checks if the saveMove view function works correctly when handling an "undo" move type
    def test_saveMove_undo(self):
        # Create required objects for testing
        researcher = Researcher.objects.create(userkey=self.user)
        experiment = Experiment.objects.create(name="Test Experiment", created_by=researcher)
        condition = Condition.objects.create(amount_item=1, created_by=researcher, name="Test Condition", experiment=experiment)
        game = Game.objects.create(has_condition=condition, room_name="test_room", public=True)

        # Set up the POST data for the request
        data = {
            "roomName": game.room_name,
            "type": "un",
            "x": 0,  # Add the "x" key with a default value
            "y": 0,  # Add the "y" key with a default value
        }

        # Create a request object with the POST data and simulate an AJAX request
        request = self.factory.post('/saveMove/', data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = self.user
        request.session = self.session

        # Call the saveMove view function with the request
        response = saveMove(request)

        # Check if the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)

        # Check if a new Move object is created in the database with the correct data (move_type set to 'un').
        move = Move.objects.last()
        self.assertIsNotNone(move)
        self.assertEqual(move.move_type, 'un') 
        
    # Checks if the initialPlayer view function works correctly. 
    def test_initialPlayer(self):
        # Create a request object with the POST data and simulate an AJAX request
        request = self.factory.post('/initialPlayer/', {'x': 10, 'y': 20, 'room_name': self.game.room_name}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        # Call the initialPlayer view function with the request
        response = initialPlayer(request)

        # Check if the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)

        # Check if the initial player position is updated correctly with the new x and y values sent in the request
        self.game.refresh_from_db()
        self.assertEqual(self.game.follower_position, {'x': 10, 'y': 20})
        
    # Checks the functionality of the setScreensize view function. Checks if it updates the session data with the provided screen size information, and it returns a successful response.
    def test_setScreensize(self):
        # Set up a session for the request
        session = self.client.session
        session.save()

        # Create a request object with the POST data and simulate an AJAX request
        request = self.factory.post('/setScreensize/', {'width': 800, 'height': 600}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.session = session

        # Call the setScreensize view function with the request
        response = setScreensize(request)
        
        # Check if the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)

        # Check if the session data has been updated with the correct screen size
        self.assertEqual(request.session['width'], 800)
        self.assertEqual(request.session['height'], 600)

    # Checks saveMove function if it behaves as expected when provided with correct input data 
    def test_saveMove(self):
        # Create a request object with the POST data and simulate an AJAX request
        request = self.factory.post('/saveMove/', {'roomName': self.game.room_name, 'type': 'mv', 'x': 2, 'y': 3}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Call the saveMove view function with the request
        response = saveMove(request)

        # Check if the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)

        # Check if the Move object was created with the correct data
        move = Move.objects.last()
        self.assertIsNotNone(move)
        self.assertEqual(move.move_type, 'mv')
        self.assertEqual(move.oldPos, {'x': 0, 'y': 0})
        self.assertEqual(move.newPos, {'x': 64, 'y': 96})
  
# Checks acceptTOS view function works properly  
class TestAcceptTOSTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_acceptTOS(self):
        request = self.factory.get('/acceptTOS/')
        request.session = {}  # Mimic session behavior
        response = acceptTOS(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(request.session['TOSaccept'])
        
# Checks decrementUsers view function works properly  
class DecrementUsersTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        
        # Create a user and researcher
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.researcher = Researcher.objects.create(userkey=self.user)

        self.condition = Condition.objects.create(
            amount_item=1,
            restriction="Some restriction",
            active=True,
            name="Test Condition",
            created_by=self.researcher  # Set created_by to the researcher instance
        )
        self.game = Game.objects.create(
            room_name="test_room",
            users=5,
            has_condition=self.condition,
            public=True
        )
            
    def test_decrement_users(self):
        request = self.factory.post('/some_path/', {'roomName': 'test_room'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = decrementUsers(request)

        # Reload the game object to get the updated value of users
        updated_game = Game.objects.get(room_name="test_room")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_game.users, 4)

# Checks viewChats from when researcher wants to view the data, it request a
# POST to the function with the data and checks if the response has the correct data
class ViewChatsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.researcher = Researcher.objects.create(userkey=self.user)
        self.experiment = Experiment.objects.create(name='Test Experiment', created_by=self.researcher)
        self.condition = Condition.objects.create(name='Test Condition', created_by=self.researcher, experiment=self.experiment, amount_item=1)
        self.game = Game.objects.create(room_name='test_room', has_condition=self.condition, public=True)
        self.chat1 = Chat.objects.create(content='Hello from follower', role='Follower', game=self.game)
        self.chat2 = Chat.objects.create(content='Hello from giver!', role='Giver', game=self.game)

    def test_view_chats(self):
        request = self.factory.post('/view_chats/', {'room_name': 'test_room'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = self.user
        response = viewChats(request)

        # Check if the response has a status code of 200
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the correct chat messages
        self.assertIn('Hello from follower', response.content.decode())
        self.assertIn('Hello from giver!', response.content.decode())
        
# Checks saveMessage view function e.g. role, message etc that are POSTed
class SaveMessageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.researcher = Researcher.objects.create(userkey=self.user)
        self.experiment = Experiment.objects.create(name='Test Experiment', created_by=self.researcher)
        self.condition = Condition.objects.create(amount_item=1,restriction="Some restriction",active=True,name="Test Condition",created_by=self.researcher)
        self.game = Game.objects.create(room_name="test_room",users=5,has_condition=self.condition,public=True)

    def test_save_message(self):
        request = HttpRequest()
        request.method = 'POST'
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        request.POST = {"role": "follower","message": "Test message","room_name": self.game.room_name
        }
        request.user = self.user

        response = saveMessage(request)

        self.assertEqual(response.status_code, 200)
        chat = Chat.objects.first()
        self.assertEqual(chat.role, "follower")
        self.assertEqual(chat.content, "Test message")
        self.assertEqual(chat.game, self.game)
