import json
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from ..models import Job
from ..serializers import JobSerializer
from .setup import init_test_user
from rest_framework.test import APIClient


# initialize the APIClient app
client = APIClient()


class GetAllJobsTest(TestCase):
    """Test module for GET all jobs API"""

    def setUp(self):
        test_user = init_test_user()
        client.force_authenticate(user=test_user)

        Job.objects.create(
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
        Job.objects.create(
            job_name="DevOps",
            company_name="Google",
            location="Tokyo",
            commute_time=60,
            description="DevOps Job using Python and Django",
            state="NEW",
            salary=100_000,
            vacation_days=15,
            priority=2,
            user=test_user,
        )
        Job.objects.create(
            job_name="Tech Lead",
            company_name="Rakuten",
            location="Osaka",
            commute_time=30,
            description="Tech Lead position for Microservice Team",
            state="INTERVIEW",
            salary=80_000,
            vacation_days=21,
            priority=2,
            user=test_user,
        )
        Job.objects.create(
            job_name="Software Engineer",
            company_name="Bloob",
            location="Sendai",
            commute_time=360,
            description="Backend-Developer Job using Python and Django",
            state="OFFER",
            salary=80_000,
            vacation_days=10,
            priority=3,
            user=test_user,
        )

    def test_get_all_jobs(self):
        # get API response
        response = client.get(reverse("job_list"))
        # get data from db
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_jobs_by_state(self):
        response = client.get("/api/jobs?state=NEW")
        jobs = Job.objects.filter(state="NEW")
        serializer = JobSerializer(jobs, many=True)
        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_jobs_by_priority(self):
        response = client.get("/api/jobs?priority=1")
        jobs = Job.objects.filter(priority=1)
        serializer = JobSerializer(jobs, many=True)
        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual((response.data), (serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_jobs_by_state_and_priority(self):
        response = client.get("/api/jobs?state=NEW&priority=1")
        jobs = Job.objects.filter(state="NEW", priority=1)
        serializer = JobSerializer(jobs, many=True)
        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual((response.data), (serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleJobTest(TestCase):
    """Test module for GET single Job API"""

    def setUp(self):
        test_user = init_test_user()
        client.force_authenticate(user=test_user)

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
        self.job_google = Job.objects.create(
            job_name="DevOps",
            company_name="Google",
            location="Tokyo",
            commute_time=60,
            description="DevOps Job using Python and Django",
            state="NEW",
            salary=100_000,
            vacation_days=15,
            priority=2,
            user=test_user,
        )
        self.job_rakuten = Job.objects.create(
            job_name="Tech Lead",
            company_name="Rakuten",
            location="Osaka",
            commute_time=30,
            description="Tech Lead position for Microservice Team",
            state="INTERVIEW",
            salary=80_000,
            vacation_days=21,
            priority=2,
            user=test_user,
        )
        self.job_bloob = Job.objects.create(
            job_name="Software Engineer",
            company_name="Bloob",
            location="Sendai",
            commute_time=360,
            description="Backend-Developer Job using Python and Django",
            state="OFFER",
            salary=80_000,
            vacation_days=10,
            priority=3,
            user=test_user,
        )

    def test_get_valid_single_job(self):
        response = client.get(reverse("job_detail", kwargs={"pk": self.job_mercari.pk}))
        job = Job.objects.get(pk=self.job_mercari.pk)
        serializer = JobSerializer(job)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_job(self):
        response = client.get(reverse("job_detail", kwargs={"pk": 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewJobTest(TestCase):
    """Test module for inserting a new Job"""

    def setUp(self):
        test_user = init_test_user()
        client.force_authenticate(user=test_user)

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

        self.invalid_payload_empty_job_name = self.valid_payload.copy()
        self.invalid_payload_empty_job_name["job_name"] = ""

        self.invalid_payload_invalid_job_name = self.valid_payload.copy()
        self.invalid_payload_invalid_job_name["job_name"] = (
            "This job name is way too long to be a real job name."
        )

        self.invalid_payload_empty_company_name = self.valid_payload.copy()
        self.invalid_payload_empty_company_name["company_name"] = ""

        self.invalid_payload_invalid_company_name = self.valid_payload.copy()
        self.invalid_payload_invalid_company_name["company_name"] = (
            "This company name is way too long to be a real company name."
        )

        self.invalid_payload_invalid_location = self.valid_payload.copy()
        self.invalid_payload_invalid_location["location"] = (
            "This location is way too long to be a real location."
        )

        self.invalid_payload_invalid_description = self.valid_payload.copy()
        self.invalid_payload_invalid_description["description"] = (
            "This description is way too long to be a real description." * 5
        )

        self.invalid_payload_invalid_state = self.valid_payload.copy()
        self.invalid_payload_invalid_state["state"] = "INVALID"

        self.invalid_payload_invalid_priority = self.valid_payload.copy()
        self.invalid_payload_invalid_priority["priority"] = "INVALID"

        self.invalid_payload_negative_salary = self.valid_payload.copy()
        self.invalid_payload_negative_salary["salary"] = -1000

        self.invalid_payload_negative_commute_time = self.valid_payload.copy()
        self.invalid_payload_negative_commute_time["commute_time"] = -60

        self.invalid_payload_negative_vacation_days = self.valid_payload.copy()
        self.invalid_payload_negative_vacation_days["vacation_days"] = -10

    def test_create_valid_job(self):
        test_data = json.dumps(self.valid_payload)
        response = client.post(
            reverse("job_list"),
            data=test_data,
            content_type="application/json",
        )
        self.assertEqual(response.data["job_name"], "Software Developer")
        self.assertEqual(response.data["company_name"], "Docomo")
        self.assertEqual(response.data["location"], "Roppongi")
        self.assertEqual(response.data["commute_time"], 45)
        self.assertEqual(
            response.data["description"], "Mid-level software engineering position"
        )
        self.assertEqual(response.data["state"], "NEW")
        self.assertIsNotNone(response.data["created_at"])
        self.assertEqual(response.data["salary"], 1_000_000)
        self.assertEqual(response.data["vacation_days"], 14)
        self.assertEqual(response.data["priority"], 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # JOB NAME
    def test_create_invalid_job_job_name(self):
        response = client.post(
            reverse("job_list"),
            data=json.dumps(self.invalid_payload_empty_job_name),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_job_job_name_max_len_exceeded(self):
        response = client.post(
            reverse("job_list"),
            data=json.dumps(self.invalid_payload_invalid_job_name),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # COMPANY NAME
    def test_create_invalid_job_empty_company_name(self):
        response = client.post(
            reverse("job_list"),
            data=json.dumps(self.invalid_payload_empty_company_name),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_job_company_name_max_len_exceeded(self):
        response = client.post(
            reverse("job_list"),
            data=json.dumps(self.invalid_payload_invalid_company_name),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # LOCATION
    def test_create_invalid_job_location_max_len_exceeded(self):
        response = client.post(
            reverse("job_list"),
            data=json.dumps(self.invalid_payload_invalid_location),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # DESCRIPTION
    def test_create_invalid_job_description_max_len_exceeded(self):
        response = client.post(
            reverse("job_list"),
            data=json.dumps(self.invalid_payload_invalid_description),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # STATE
    def test_create_invalid_job_wrong_state(self):
        response = client.post(
            reverse("job_list"),
            data=json.dumps(self.invalid_payload_invalid_state),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # PRIORITY
    def test_create_invalid_job_wrong_priority(self):
        response = client.post(
            reverse("job_list"),
            data=json.dumps(self.invalid_payload_invalid_priority),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # SALARY
    def test_create_invalid_job_negative_salary(self):
        response = client.post(
            reverse("job_list"),
            data=json.dumps(self.invalid_payload_negative_salary),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # COMMUTE TIME
    def test_create_invalid_job_negative_commute_time(self):
        response = client.post(
            reverse("job_list"),
            data=json.dumps(self.invalid_payload_negative_commute_time),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # VACATION DAYS
    def test_create_invalid_job_negative_vacation_days(self):
        response = client.post(
            reverse("job_list"),
            data=json.dumps(self.invalid_payload_negative_vacation_days),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleJobTest(TestCase):
    """Test module for updating an existing Job record"""

    def setUp(self):
        test_user = init_test_user()
        client.force_authenticate(user=test_user)

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
        self.job_google = Job.objects.create(
            job_name="DevOps",
            company_name="Google",
            location="Tokyo",
            commute_time=60,
            description="DevOps Job using Python and Django",
            state="NEW",
            salary=100_000,
            vacation_days=15,
            priority=2,
            user=test_user,
        )

        self.valid_payload = {
            "job_name": "Software Developer",
            "company_name": "Mercarci",
            "location": "Roppongi",
            "commute_time": 45,
            "description": "Backend-Developer Job using Python and FastAPI",
            "state": "APPLIED",
            "created_at": "2024-12-13T22:30:04.000Z",
            "salary": 2000000,
            "vacation_days": 13,
            "priority": 1,
        }

        self.invalid_payload_empty_job_name = self.valid_payload.copy()
        self.invalid_payload_empty_job_name["job_name"] = ""

        self.invalid_payload_invalid_job_name = self.valid_payload.copy()
        self.invalid_payload_invalid_job_name["job_name"] = (
            "This job name is way too long to be a real job name."
        )

        self.invalid_payload_empty_company_name = self.valid_payload.copy()
        self.invalid_payload_empty_company_name["company_name"] = ""

        self.invalid_payload_invalid_company_name = self.valid_payload.copy()
        self.invalid_payload_invalid_company_name["company_name"] = (
            "This company name is way too long to be a real company name."
        )

        self.invalid_payload_invalid_location = self.valid_payload.copy()
        self.invalid_payload_invalid_location["location"] = (
            "This location is way too long to be a real location."
        )

        self.invalid_payload_invalid_description = self.valid_payload.copy()
        self.invalid_payload_invalid_description["description"] = (
            "This description is way too long to be a real description." * 5
        )

        self.invalid_payload_state = self.valid_payload.copy()
        self.invalid_payload_state["state"] = "TO BE DONE"

        self.invalid_payload_priority = self.valid_payload.copy()
        self.invalid_payload_priority["priority"] = 15

        self.invalid_payload_negative_salary = self.valid_payload.copy()
        self.invalid_payload_negative_salary["salary"] = -1000

        self.invalid_payload_negative_commute_time = self.valid_payload.copy()
        self.invalid_payload_negative_commute_time["commute_time"] = -60

        self.invalid_payload_negative_vacation_days = self.valid_payload.copy()
        self.invalid_payload_negative_vacation_days["vacation_days"] = -10

    def test_valid_update_job(self):
        response = client.put(
            reverse("job_detail", kwargs={"pk": self.job_mercari.pk}),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # JOB NAME
    def test_invalid_update_job_empty_job_name(self):
        response = client.put(
            reverse("job_detail", kwargs={"pk": self.job_mercari.pk}),
            data=json.dumps(self.invalid_payload_empty_job_name),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_update_job_job_name_max_len_exceeded(self):
        response = client.put(
            reverse("job_detail", kwargs={"pk": self.job_mercari.pk}),
            data=json.dumps(self.invalid_payload_invalid_job_name),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # COMPANY
    def test_invalid_update_job_empty_company_name(self):
        response = client.put(
            reverse("job_detail", kwargs={"pk": self.job_mercari.pk}),
            data=json.dumps(self.invalid_payload_empty_company_name),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_update_job_company_name_max_len_exceeded(self):
        response = client.put(
            reverse("job_detail", kwargs={"pk": self.job_mercari.pk}),
            data=json.dumps(self.invalid_payload_invalid_company_name),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_update_job_wrong_job_company_and_job_name(self):
        response = client.put(
            reverse("job_detail", kwargs={"pk": self.job_google.pk}),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # LOCATION
    def test_invalid_update_job_location_max_len_exceeded(self):
        response = client.put(
            reverse("job_detail", kwargs={"pk": self.job_mercari.pk}),
            data=json.dumps(self.invalid_payload_invalid_location),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # DESCRIPTION
    def test_invalid_update_job_description_max_len_exceeded(self):
        response = client.put(
            reverse("job_detail", kwargs={"pk": self.job_mercari.pk}),
            data=json.dumps(self.invalid_payload_invalid_description),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # STATE
    def test_invalid_update_job_wrong_state(self):
        response = client.put(
            reverse("job_detail", kwargs={"pk": self.job_mercari.pk}),
            data=json.dumps(self.invalid_payload_state),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # PRIORITY
    def test_invalid_update_job_wrong_priority(self):
        response = client.put(
            reverse("job_detail", kwargs={"pk": self.job_mercari.pk}),
            data=json.dumps(self.invalid_payload_priority),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # SALARY
    def test_invalid_update_job_negative_salary(self):
        response = client.put(
            reverse("job_detail", kwargs={"pk": self.job_mercari.pk}),
            data=json.dumps(self.invalid_payload_negative_salary),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # COMMUTE TIME
    def test_invalid_update_job_negative_commute_time(self):
        response = client.put(
            reverse("job_detail", kwargs={"pk": self.job_mercari.pk}),
            data=json.dumps(self.invalid_payload_negative_commute_time),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # VACATION DAYS
    def test_invalid_update_job_negative_vacation_days(self):
        response = client.put(
            reverse("job_detail", kwargs={"pk": self.job_mercari.pk}),
            data=json.dumps(self.invalid_payload_negative_vacation_days),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleJobTest(TestCase):
    """Test module for deleting an existing Job record"""

    def setUp(self):
        test_user = init_test_user()
        client.force_authenticate(user=test_user)

        self.job_bloob = Job.objects.create(
            job_name="Software Engineer",
            company_name="Bloob",
            location="Sendai",
            commute_time=360,
            description="Backend-Developer Job using Python and Django",
            state="OFFER",
            salary=80_000,
            vacation_days=10,
            priority=3,
            user=test_user,
        )

    def test_valid_delete_job(self):
        response = client.delete(
            reverse("job_detail", kwargs={"pk": self.job_bloob.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_job(self):
        response = client.delete(reverse("job_detail", kwargs={"pk": 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
