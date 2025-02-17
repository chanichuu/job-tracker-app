from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Job(models.Model):
    class State(models.TextChoices):
        NEW = "NEW", _("New")
        APPLIED = "APPLIED", _("Applied")
        INTERVIEW = "INTERVIEW", _("Interview")
        OFFER = "OFFER", _("Offer")
        REJECTED = "REJECTED", _("Rejected")

    class Priority(models.IntegerChoices):
        HIGH = 1, _("High")
        MEDIUM = 2, _("Medium")
        LOW = 3, _("Low")

    job_name = models.CharField(max_length=24)
    company_name = models.CharField(max_length=24)
    commute_time = models.PositiveIntegerField()
    description = models.CharField(max_length=256)
    state = models.CharField(
        max_length=9,
        choices=State.choices,
        default=State.NEW,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    salary = models.PositiveIntegerField()
    vacation_days = models.PositiveIntegerField()
    priority = models.IntegerField(choices=Priority.choices, default=Priority.LOW)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(
        "Address", on_delete=models.CASCADE, null=True, blank=True
    )
    contact = models.ForeignKey(
        "Contact", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"Job information: {self.job_name} at {self.company_name}"

    def __repr__(self):
        return f"Job({self.job_name} Company: {self.company_name})"


class Address(models.Model):
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=64)

    def __str__(self):
        return f"Address information: {self.street}, {self.city}, {self.state}, {self.zip_code}, {self.country}"

    def __repr__(self):
        return f"Address({self.street}, {self.city}, {self.state}, {self.zip_code}, {self.country})"


class Contact(models.Model):
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"Contact information: {self.name}, {self.phone}, {self.email}"

    def __repr__(self):
        return f"Contact({self.name}, {self.phone}, {self.email})"
