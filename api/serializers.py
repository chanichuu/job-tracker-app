from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Job, Address, Contact


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "id",
            "street",
            "city",
            "state",
            "zip_code",
            "country",
        )


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            "id",
            "name",
            "phone",
            "email",
        )


class JobSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)
    contact = ContactSerializer(required=False)

    class Meta:
        model = Job
        fields = (
            "id",
            "job_name",
            "company_name",
            "commute_time",
            "description",
            "state",
            "created_at",
            "salary",
            "vacation_days",
            "priority",
            "is_favourite",
            "address",
            "contact",
        )

    def create(self, validated_data):
        address_data = validated_data.pop("address", None)
        contact_data = validated_data.pop("contact", None)
        address = contact = None
        if address_data:
            address = Address.objects.create(**address_data)
        if contact_data:
            contact = Contact.objects.create(**contact_data)
        job = Job.objects.create(address=address, contact=contact, **validated_data)

        return job

    def update(self, instance, validated_data):
        address_data = validated_data.pop("address", None)
        contact_data = validated_data.pop("contact", None)
        if address_data:
            address = Address.objects.get_or_create(**address_data)[0]
            instance.address = address
        if contact_data:
            contact = Contact.objects.get_or_create(**contact_data)[0]
            instance.contact = contact

        instance.job_name = validated_data.get("job_name", instance.job_name)
        instance.company_name = validated_data.get(
            "company_name", instance.company_name
        )
        instance.commute_time = validated_data.get(
            "commute_time", instance.commute_time
        )
        instance.description = validated_data.get("description", instance.description)
        instance.state = validated_data.get("state", instance.state)
        instance.salary = validated_data.get("salary", instance.salary)
        instance.vacation_days = validated_data.get(
            "vacation_days", instance.vacation_days
        )
        instance.priority = validated_data.get("priority", instance.priority)
        instance.is_favourite = validated_data.get(
            "is_favourite", instance.is_favourite
        )
        instance.save()

        return instance
