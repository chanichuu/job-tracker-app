import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Job
from ..serializers import JobSerializer


# initialize the APIClient app
client = Client()


class GetAllJobsTest(TestCase):
    """Test module for GET all jobs API"""

    def setUp(self):
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_jobs_by_priority(self):
        response = client.get("/api/jobs?priority=1")
        jobs = Job.objects.filter(priority=1)
        serializer = JobSerializer(jobs, many=True)
        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_jobs_by_state_and_priority(self):
        response = client.get("/api/jobs?state=NEW&priority=1")
        jobs = Job.objects.filter(state="NEW", priority=1)
        serializer = JobSerializer(jobs, many=True)
        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleJobTest(TestCase):
    """Test module for GET single Job API"""

    def setUp(self):
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
        self.valid_payload = {
            "job_name": "Software Developer",
            "company_name": "Docomo",
            "location": "Roppongi",
            "commute_time": 45,
            "description": "Mid-level software engineering position for MerPay",
            "state": "NEW",
            "created_at": "2024-12-13T22:30:04.000Z",
            "salary": 1000000,
            "vacation_days": 14,
            "priority": 1,
        }

        self.invalid_payload = {
            "job_name": "",
            "company_name": "Docomo",
            "location": "Roppongi",
            "commute_time": 45,
            "description": "Mid-level software engineering position for MerPay",
            "state": "NEW",
            "created_at": "2024-12-13T22:30:04.000Z",
            "salary": 1000000,
            "vacation_days": 14,
            "priority": 1,
        }

    def test_create_valid_job(self):
        response = client.post(
            reverse("job_list"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_job(self):
        response = client.post(
            reverse("job_list"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # todo add more specific tests for invalid state, prio, datetime etc...


class UpdateSingleJobTest(TestCase):
    """Test module for updating an existing Job record"""

    def setUp(self):
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
        )

        self.valid_payload = self.valid_payload = {
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

        self.invalid_payload = {
            "job_name": "",
            "company_name": "Google",
            "location": "Tokyo",
            "commute_time": 45,
            "description": "DevOps Job using Python and FastAPI",
            "state": "REJECTED",
            "created_at": "2024-12-13T22:30:04.000Z",
            "salary": 1000000,
            "vacation_days": 14,
            "priority": 1,
        }

    def test_valid_update_job(self):
        response = client.put(
            reverse("job_detail", kwargs={"pk": self.job_mercari.pk}),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_job(self):
        response = client.put(
            reverse("job_detail", kwargs={"pk": self.job_google.pk}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # todo add more specific tests for invalid state, prio, datetime etc...


class DeleteSingleJobTest(TestCase):
    """Test module for deleting an existing Job record"""

    def setUp(self):
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
        )

    def test_valid_delete_job(self):
        response = client.delete(
            reverse("job_detail", kwargs={"pk": self.job_bloob.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_job(self):
        response = client.delete(reverse("job_detail", kwargs={"pk": 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
