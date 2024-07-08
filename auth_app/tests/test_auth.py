from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from models import User

class AuthTests(APITestCase):
    def test_register_user_successfully(self):
        url = reverse('register')
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@gmail.com",
            "password": "password123",
            "phone": "1234567890"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("accessToken", response.data['data'])
        self.assertEqual(response.data['data']['user']['first_name'], "John")

    def test_login_user_successfully(self):
        user = User.objects.create_user(email="john.doe@gmail.com", first_name="John", last_name="Doe", password="password123")
        url = reverse('login')
        data = {
            "email": "john.doe@gmail.com",
            "password": "password123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("accessToken", response.data['data'])
        self.assertEqual(response.data['data']['user']['first_name'], "John")

    def test_register_user_with_missing_fields(self):
        url = reverse('register')
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@gmail.com",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_register_user_with_duplicate_email(self):
        User.objects.create_user(email="john.doe@gmail.com", first_name="John", last_name="Doe", password="password123")
        url = reverse('register')
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@gmail.com",
            "password": "password123",
            "phone": "1234567890"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)