from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import json
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from ..models import Job


# initialize the APIClient app
auth_client = APIClient()


def init_test_user():
    user = User.objects.create(username="TEST_USER")
    user.set_password("1234")
    user.save()

    return user


class CRUDJobsTest_Authorized(TestCase):
    """Test module for GET all jobs API"""

    def setUp(self):
        test_user = init_test_user()

        # setup auth_client to get valid bearer token
        user_payload = {
            "username": "TEST_USER",
            "password": "1234",
        }
        test_user_data = json.dumps(user_payload)
        response = auth_client.post(
            reverse("token_obtain_pair"),
            data=test_user_data,
            content_type="application/json",
        )

        access_token = response.data["access"]
        auth_client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

        self.job_mercari = Job.objects.create(
            job_name="Software Developer",
            company_name="Mercarci",
            location="Tokyo",
            commute_time=60,
            description="Backend-Developer Job using Python and Django",
            state="NEW",
            salary=80_000,
            vacation_days=15,
            priority=1,
            user=test_user,
        )

    def test_get_all_jobs_authorized(self):
        response = auth_client.get(reverse("job_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_job_authorized(self):
        response = auth_client.get(reverse("job_detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_job_authorized(self):
        self.valid_payload = {
            "job_name": "Software Developer",
            "company_name": "Docomo",
            "location": "Roppongi",
            "commute_time": 45,
            "description": "Mid-level software engineering position",
            "state": "NEW",
            "salary": 1_000_000,
            "vacation_days": 14,
            "priority": 1,
        }
        job_data = json.dumps(self.valid_payload)
        response = auth_client.post(
            reverse("job_list"),
            data=job_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_job_authorized(self):
        valid_payload = {
            "job_name": "Software Developer",
            "company_name": "Mercarci",
            "location": "Roppongi",
            "commute_time": 45,
            "description": "Backend-Developer Job using Python and Django",
            "state": "APPLIED",
            "salary": 10_000_000,
            "vacation_days": 16,
            "priority": 1,
        }
        job_data = json.dumps(valid_payload)
        response = auth_client.put(
            reverse("job_detail", kwargs={"pk": self.job_mercari.pk}),
            data=job_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CRUDJobsTest_Unauthorized(TestCase):
    """Test module for GET all jobs API"""

    def setUp(self):
        # setup auth_client w/o valid bearer token
        invalid_access_token = "INVALID_ACCESS_TOKEN"
        auth_client.credentials(HTTP_AUTHORIZATION="Bearer " + invalid_access_token)

    def test_get_all_jobs_unauthorized(self):
        response = auth_client.get(reverse("job_list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_single_job_unauthorized(self):
        response = auth_client.get(reverse("job_detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_job_unauthorized(self):
        response = auth_client.post(reverse("job_list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_job_unauthorized(self):
        response = auth_client.put(reverse("job_detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_job_unauthorized(self):
        response = auth_client.delete(reverse("job_detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
