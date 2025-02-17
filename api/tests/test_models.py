from django.test import TestCase
from ..models import Job, Address, Contact
from .setup import init_test_user


class JobTest(TestCase):
    """Test module for Job model"""

    def setUp(self):
        test_user = init_test_user()

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
            user=test_user,
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


class AddressTest(TestCase):
    """Test module for Address model"""

    def setUp(self):
        self.expected_address = Address.objects.create(
            street="123 Main St",
            city="Seattle",
            state="WA",
            zip_code="98101",
            country="USA",
        )

    def test_address_model(self):
        actual_address = Address.objects.get(pk=self.expected_address.id)

        self.assertEqual(self.expected_address.street, actual_address.street)
        self.assertEqual(self.expected_address.city, actual_address.city)
        self.assertEqual(self.expected_address.state, actual_address.state)
        self.assertEqual(self.expected_address.zip_code, actual_address.zip_code)
        self.assertEqual(self.expected_address.country, actual_address.country)


class ContactTest(TestCase):
    """Test module for Contact model"""

    def setUp(self):
        self.expected_contact = Contact.objects.create(
            name="John Doe", phone="123-4568-7890", email="john.doe@test-mail.com"
        )

    def test_contact_model(self):
        actual_contact = Contact.objects.get(pk=self.expected_contact.id)

        self.assertEqual(self.expected_contact.name, actual_contact.name)
        self.assertEqual(self.expected_contact.phone, actual_contact.phone)
        self.assertEqual(self.expected_contact.email, actual_contact.email)
