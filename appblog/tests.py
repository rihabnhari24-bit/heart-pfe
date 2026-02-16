from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthenticationFlowTests(TestCase):
    def test_register_success_creates_user_and_redirects_to_login(self):
        response = self.client.post(
            reverse("register"),
            {
                "name": "Ali",
                "email": "ali@example.com",
                "password": "StrongPass123!",
            },
        )

        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="ali@example.com").exists())

    def test_register_invalid_data_shows_red_error_message(self):
        response = self.client.post(
            reverse("register"),
            {
                "name": "",
                "email": "not-an-email",
                "password": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Les informations sont mal écrites.")
        self.assertEqual(User.objects.count(), 0)
