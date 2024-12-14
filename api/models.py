from django.db import models
from django.utils.translation import gettext_lazy as _


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
    location = models.CharField(max_length=24)
    commute_time = models.IntegerField()
    description = models.CharField(max_length=256)
    state = models.CharField(
        max_length=9,
        choices=State.choices,
        default=State.NEW,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    salary = models.IntegerField()
    vacation_days = models.IntegerField()
    priority = models.IntegerField(choices=Priority.choices, default=Priority.LOW)

    def __repr__(self):
        return f"Job: {self.job_name} Company: {self.company_name}"
