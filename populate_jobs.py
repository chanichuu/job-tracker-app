import random
import os
import django

# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "job_tracker.settings")
django.setup()

from faker import Faker
from django.contrib.auth import get_user_model
from api.models import Job, Address, Contact


fake = Faker()
User = get_user_model()


def create_fake_address():
    return Address.objects.create(
        street=fake.street_address(),
        city=fake.city(),
        state=fake.state(),
        zip_code=fake.zipcode(),
        country=fake.country(),
    )


def create_fake_contact():
    return Contact.objects.create(
        name=fake.name(), phone=fake.phone_number(), email=fake.email()
    )


def create_fake_job(user):
    address = create_fake_address()
    contact = create_fake_contact()

    return Job.objects.create(
        job_name=fake.job(),
        company_name=fake.company(),
        commute_time=random.randint(10, 90),
        description=fake.text(max_nb_chars=200),
        state=random.choice([choice[0] for choice in Job.State.choices]),
        salary=random.randint(50000, 200000),
        vacation_days=random.randint(5, 30),
        priority=random.choice([choice[0] for choice in Job.Priority.choices]),
        user=user,
        address=address,
        contact=contact,
    )


def generate_jobs(n=5):
    users = list(User.objects.all())
    if not users:
        raise Exception(
            "No users found. Create at least one user before running this script."
        )

    for _ in range(n):
        user = random.choice(users)
        job = create_fake_job(user)
        print(f"Created job: {job}")


if __name__ == "__main__":
    print("Populating the databases...Please Wait")
    generate_jobs(10)
    print("Populating Complete")
