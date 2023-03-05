from django.test import TestCase
from django.urls import reverse
from .models import Researcher
 
# Researcher Registration Testing  
# !!!!!!!!!!!!!! These comments are to help with the report writing and u can delete later: !!!!!!!!!!!!!!
# This test case checks the registration process for a new Researcher
# in the system. It first counts the initial number of researchers in the database, then submits the registration form with test data.
# It checks whether the form submission was successful, and whether a new Researcher was saved to the database. It also checks whether
# the new Researcher has the expected data.
class ResearcherRegistrationTest(TestCase):
    def test_registration(self):
        # Count the initial number of researchers in the database
        initial_count = Researcher.objects.count()
 
        # Submit the registration form with test data
        response = self.client.post(reverse('researcher_registration'), {
            'name': 'Jane',
            'surname': 'Doe',
            'email': 'jane@example.com',
            'username': 'janedoe',
            'password': 'password123'
        })
 
        # Check that the form submission was successful
        self.assertEqual(response.status_code, 302)  # Redirect after successful POST is expected
 
        # Check that a new Researcher was saved to the database
        self.assertEqual(Researcher.objects.count(), initial_count + 1)
 
        # Check that the new Researcher has the expected data
        new_researcher = Researcher.objects.get(email='jane@example.com')
        self.assertEqual(new_researcher.name, 'Jane')
        self.assertEqual(new_researcher.surname, 'Doe')
        self.assertEqual(new_researcher.username, 'janedoe')
        self.assertEqual(new_researcher.password, 'password123')

 
 