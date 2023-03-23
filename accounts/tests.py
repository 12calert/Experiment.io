from django.test import TestCase, Client
from django.urls import reverse 
from .models import Researcher
from game_website.forms import ResearcherRegisterForm
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.messages import get_messages
from django.contrib.auth.models import User

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