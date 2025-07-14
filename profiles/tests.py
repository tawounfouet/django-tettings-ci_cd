from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile


class ProfileModelTest(TestCase):
    """Tests pour le modèle Profile"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.profile = Profile.objects.create(user=self.user, favorite_city="Paris")

    def test_profile_creation(self):
        """Test la création d'un profil"""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.favorite_city, "Paris")

    def test_profile_str_representation(self):
        """Test la représentation string d'un profil"""
        self.assertEqual(str(self.profile), "testuser")

    def test_profile_user_relationship(self):
        """Test la relation OneToOne avec User"""
        self.assertEqual(self.profile.user.username, "testuser")
        self.assertEqual(self.profile.user.email, "test@example.com")

    def test_profile_favorite_city_blank(self):
        """Test qu'un profil peut avoir une ville favorite vide"""
        profile_blank = Profile.objects.create(
            user=User.objects.create_user(
                username="testuser2", email="test2@example.com", password="testpass123"
            ),
            favorite_city="",
        )
        self.assertEqual(profile_blank.favorite_city, "")


class ProfilesViewTest(TestCase):
    """Tests pour les vues de l'application profiles"""

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username="alice", email="alice@example.com", password="alicepass123"
        )
        self.user2 = User.objects.create_user(
            username="bob", email="bob@example.com", password="bobpass123"
        )
        self.profile1 = Profile.objects.create(
            user=self.user1, favorite_city="New York"
        )
        self.profile2 = Profile.objects.create(user=self.user2, favorite_city="London")

    def test_profiles_index_view(self):
        """Test la vue index des profils"""
        response = self.client.get(reverse("profiles:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "alice")
        self.assertContains(response, "bob")

    def test_profile_detail_view(self):
        """Test la vue détail d'un profil"""
        response = self.client.get(
            reverse("profiles:detail", args=[self.user1.username])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "alice")
        self.assertContains(response, "New York")

    def test_profile_detail_view_not_found(self):
        """Test la vue détail avec un username inexistant"""
        response = self.client.get(reverse("profiles:detail", args=["nonexistent"]))
        self.assertEqual(response.status_code, 404)

    def test_multiple_profiles_display(self):
        """Test l'affichage de plusieurs profils"""
        response = self.client.get(reverse("profiles:index"))
        self.assertEqual(response.status_code, 200)
        # Vérifier que les deux profils sont affichés
        self.assertContains(response, "alice")
        self.assertContains(response, "bob")
