from django.test import TestCase, Client
from django.urls import reverse 
from .models import Researcher
from game_website.forms import ResearcherRegisterForm
from django.test import TestCase
from django.contrib.auth.models import User

# Testing of Researcher registration
class ResearcherRegistrationTests(TestCase):
    # Test that the registration page loads successfully:
    def test_registration_page_loads_successfully(self):
        url = reverse('researcher_registration')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def setUp(self):
        self.valid_data = {
            'forename': 'John',
            'surname': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'password123'
        }
        
        self.invalid_data = {
            'forename': 'John',
            'surname': 'Doe',
            'username': 'johndoe',
            'email': 'invalid_email',
            'password': 'password123'
        }
    
    def test_register_valid_data(self):
        # Make a POST request to the researcher_registration view with valid form data
        response = self.client.post(reverse('researcher_registration'), self.valid_data)
        
        # Check that the response is a redirect to the home page
        self.assertRedirects(response, reverse('home'))
        
        # Check that a new User object was created with the correct data
        self.assertTrue(User.objects.filter(username=self.valid_data['username']).exists())
        user = User.objects.get(username=self.valid_data['username'])
        self.assertEqual(user.email, self.valid_data['email'])
        self.assertEqual(user.first_name, self.valid_data['forename'])
        self.assertEqual(user.last_name, self.valid_data['surname'])     
        self.assertFalse(user.is_active) # The user should not be active yet
 
        # Check that a new Researcher object was created with the correct userkey
        self.assertTrue(Researcher.objects.filter(userkey=user).exists())
        researcher = Researcher.objects.get(userkey=user)
        self.assertIsNotNone(researcher.researcher_id)
        
        # Check that the user is not active until they are authenticated
        self.assertFalse(user.is_active)
        
    def test_register_invalid_data(self):
        # Make a POST request to the researcher_registration view with invalid form data
        response = self.client.post(reverse('researcher_registration'), self.invalid_data)
        
        # Check that the response is not a redirect
        self.assertEqual(response.status_code, 200)
        
        # Check that the form is invalid
        self.assertFalse(ResearcherRegisterForm(data=self.invalid_data).is_valid())
        
        # Check that no new User or Researcher objects were created
        self.assertFalse(User.objects.filter(username=self.invalid_data['username']).exists())
        self.assertFalse(Researcher.objects.filter(userkey__username=self.invalid_data['username']).exists())

