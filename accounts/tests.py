from django.test import TestCase, Client
from django.urls import reverse 
from .models import Researcher
from game_website.forms import ResearcherRegisterForm
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Researcher


class ResearcherRegistrationTestCase(TestCase):
    def test_valid_registration(self):
        # Create a user for authentication purposes
        user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

        # Define test data
        form_data = {
            'forename': 'John',
            'surname': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'password'
        }

        # Instantiate the form with test data
        form = ResearcherRegisterForm(data=form_data)

        # Verify that the form is valid
        self.assertTrue(form.is_valid())

        # Save the form data to the database
        researcher = Researcher(
            user=user,
            forename=form.cleaned_data['forename'],
            surname=form.cleaned_data['surname'],
            email=form.cleaned_data['email'],
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        researcher.save()

        # Verify that the researcher was added to the database
        self.assertEqual(Researcher.objects.count(), 1)

    def test_invalid_registration(self):
        # Define test data with missing required fields
        form_data = {
            'forename': 'John',
            'surname': 'Doe',
            'username': 'johndoe'
        }

        # Instantiate the form with test data
        form = ResearcherRegisterForm(data=form_data)

        # Verify that the form is invalid
        self.assertFalse(form.is_valid())
    
    def test_form_fields(self):
        # Check if all form fields are present
        form = ResearcherRegisterForm()
        self.assertTrue('forename' in form.fields)
        self.assertTrue('surname' in form.fields)
        self.assertTrue('username' in form.fields)
        self.assertTrue('email' in form.fields)
        self.assertTrue('password' in form.fields)