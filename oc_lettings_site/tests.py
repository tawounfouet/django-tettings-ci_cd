from django.test import TestCase, Client
from django.urls import reverse


class IndexViewTest(TestCase):
    """Tests pour la page d'accueil"""

    def setUp(self):
        self.client = Client()

    def test_index_view_status_code(self):
        """Test que la page d'accueil retourne un status 200"""
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_content(self):
        """Test que la page d'accueil contient le bon contenu"""
        response = self.client.get(reverse("index"))
        self.assertContains(response, "Holiday Homes")
        self.assertContains(response, "Welcome to Holiday Homes")
