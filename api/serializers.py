from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            "id",
            "job_name",
            "company_name",
            "location",
            "commute_time",
            "description",
            "state",
            "created_at",
            "salary",
            "vacation_days",
            "priority",
        )
