from django.test import TestCase
from ..models import Job


class JobTest(TestCase):
    """Test module for Job model"""

    def setUp(self):
        Job.objects.create(
            job_name="Software Developer",
            company_name="Ebay",
            location="Seattle",
            commute_time=60,
            description="Backend-Developer Job using Python and Django",
            state="APPLIED",
            salary=80_000,
            vacation_days=15,
            priority=2,
        )

    def test_job_model(self):
        job = Job.objects.get(job_name="Software Developer", company_name="Ebay")

        self.assertEqual("Software Developer", job.job_name)
        self.assertEqual("Ebay", job.company_name)
        self.assertEqual("Seattle", job.location)
        self.assertEqual(60, job.commute_time)
        self.assertEqual(
            "Backend-Developer Job using Python and Django", job.description
        )
        self.assertEqual("APPLIED", job.state)
        self.assertEqual(80_000, job.salary)
        self.assertEqual(15, job.vacation_days)
        self.assertEqual(2, job.priority)
        self.assertIsNotNone(job.created_at)
