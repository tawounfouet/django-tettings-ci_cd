from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import Address, Letting


class AddressModelTest(TestCase):
    """Tests pour le modèle Address"""

    def setUp(self):
        self.address = Address.objects.create(
            number=123,
            street="Main Street",
            city="Springfield",
            state="IL",
            zip_code=62701,
            country_iso_code="USA",
        )

    def test_address_creation(self):
        """Test la création d'une adresse"""
        self.assertEqual(self.address.number, 123)
        self.assertEqual(self.address.street, "Main Street")
        self.assertEqual(self.address.city, "Springfield")
        self.assertEqual(self.address.state, "IL")
        self.assertEqual(self.address.zip_code, 62701)
        self.assertEqual(self.address.country_iso_code, "USA")

    def test_address_str_representation(self):
        """Test la représentation string d'une adresse"""
        self.assertEqual(str(self.address), "123 Main Street")

    def test_address_validation_number_max(self):
        """Test la validation du numéro maximum"""
        with self.assertRaises(ValidationError):
            address = Address(
                number=10000,  # Dépasse MaxValueValidator(9999)
                street="Test Street",
                city="Test City",
                state="TX",
                zip_code=12345,
                country_iso_code="USA",
            )
            address.full_clean()

    def test_address_validation_state_min_length(self):
        """Test la validation de la longueur minimale de l'état"""
        with self.assertRaises(ValidationError):
            address = Address(
                number=123,
                street="Test Street",
                city="Test City",
                state="T",  # Moins de 2 caractères
                zip_code=12345,
                country_iso_code="USA",
            )
            address.full_clean()


class LettingModelTest(TestCase):
    """Tests pour le modèle Letting"""

    def setUp(self):
        self.address = Address.objects.create(
            number=456,
            street="Oak Avenue",
            city="Chicago",
            state="IL",
            zip_code=60601,
            country_iso_code="USA",
        )
        self.letting = Letting.objects.create(
            title="Beautiful Chicago Apartment", address=self.address
        )

    def test_letting_creation(self):
        """Test la création d'un letting"""
        self.assertEqual(self.letting.title, "Beautiful Chicago Apartment")
        self.assertEqual(self.letting.address, self.address)

    def test_letting_str_representation(self):
        """Test la représentation string d'un letting"""
        self.assertEqual(str(self.letting), "Beautiful Chicago Apartment")

    def test_letting_address_relationship(self):
        """Test la relation OneToOne avec Address"""
        self.assertEqual(self.letting.address.number, 456)
        self.assertEqual(self.letting.address.street, "Oak Avenue")


class LettingsViewTest(TestCase):
    """Tests pour les vues de l'application lettings"""

    def setUp(self):
        self.client = Client()
        self.address = Address.objects.create(
            number=789,
            street="Pine Street",
            city="Boston",
            state="MA",
            zip_code=2101,
            country_iso_code="USA",
        )
        self.letting = Letting.objects.create(title="Boston Loft", address=self.address)

    def test_lettings_index_view(self):
        """Test la vue index des lettings"""
        response = self.client.get(reverse("lettings:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Boston Loft")

    def test_letting_detail_view(self):
        """Test la vue détail d'un letting"""
        response = self.client.get(reverse("lettings:detail", args=[self.letting.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Boston Loft")
        self.assertContains(response, "789 Pine Street")

    def test_letting_detail_view_not_found(self):
        """Test la vue détail avec un ID inexistant"""
        response = self.client.get(reverse("lettings:detail", args=[9999]))
        self.assertEqual(response.status_code, 404)
