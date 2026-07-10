from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Candidate, Project


class RegistrationSecurityTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Security test",
            infinite_registration_period=True,
            max_registrations=1,
        )
        self.payload = {
            "student": "d",
            "forename": "Test",
            "surname": "Person",
            "email": "person@example.com",
            "school": "Test school",
            "school_class": "5a",
            "address_street": "Teststr. 1",
            "address_city": "12345 Teststadt",
            "application": "Test",
            "phone_number": "123456",
            "accept_privacy": "on",
        }

    @patch("ui.views.successful_registration_action")
    def test_valid_registration_is_created(self, action):
        response = self.client.post(
            reverse("show_project", args=[self.project.project_id]), self.payload
        )

        self.assertRedirects(
            response,
            reverse("registration_success", args=[self.project.project_id]),
        )
        self.assertEqual(Candidate.objects.count(), 1)
        action.assert_called_once()

    def test_post_cannot_bypass_closed_registration(self):
        self.project.infinite_registration_period = False
        self.project.registration_starting_date = timezone.localdate() - timedelta(days=2)
        self.project.registration_closing_date = timezone.localdate() - timedelta(days=1)
        self.project.save()

        response = self.client.post(
            reverse("show_project", args=[self.project.project_id]), self.payload
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Candidate.objects.count(), 0)

    def test_post_cannot_bypass_project_capacity(self):
        Candidate.objects.create(
            project=self.project,
            student="d",
            forename="Existing",
            surname="Person",
            email="existing@example.com",
            school="School",
            school_class="5a",
            address_street="Street 1",
            address_city="City",
            phone_number="123",
        )

        response = self.client.post(
            reverse("show_project", args=[self.project.project_id]), self.payload
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(Candidate.objects.count(), 1)
