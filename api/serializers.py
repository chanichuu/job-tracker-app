from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Job, Address, Contact
import logging

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class AddressSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        required=False
    )  # explicitly define id to access it in validated_data while updating a job object

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
    id = serializers.IntegerField(
        required=False
    )  # explicitly define id to access it in validated_data while updating a job object

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

        logger.debug(f"Address: {address_data}")
        logger.debug(f"Contact: {contact_data}")

        self.update_address(instance, validated_data, address_data)

        self.update_contact(instance, validated_data, contact_data)

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

    def update_contact(self, instance, validated_data, contact_data):
        if contact_data is not None:
            contact_id = contact_data.get("id")
            if contact_id:
                try:
                    contact_instance = Contact.objects.get(id=contact_id)
                    logger.debug(f"Contact found: {contact_instance}")
                    contact_instance.save()
                    instance.contact = contact_instance
                except Contact.DoesNotExist:
                    print(
                        f"Contact with ID {contact_id} not found, creating a new one."
                    )
                    new_contact = Contact.objects.create(**contact_data)
                    instance.contact = new_contact
                except Contact.MultipleObjectsReturned:
                    raise serializers.ValidationError(
                        {
                            "contact": "Multiple Contact objects found for the given ID. Data inconsistency."
                        }
                    )
            else:
                contact, _ = Contact.objects.get_or_create(**contact_data)
                instance.contact = contact
        else:
            instance.contact = None

    def update_address(self, instance, validated_data, address_data):
        if address_data is not None:
            address_id = address_data.get("id")
            if address_id:
                try:
                    address_instance = Address.objects.get(id=address_id)
                    address_instance.save()
                    instance.address = address_instance
                except Address.DoesNotExist:
                    logger.debug(
                        f"Address with ID {address_id} not found, creating a new one."
                    )
                    new_address = Address.objects.create(**address_data)
                    instance.address = new_address
                except Address.MultipleObjectsReturned:
                    # This should ideally not happen if using ID, but as a safeguard.
                    raise serializers.ValidationError(
                        {
                            "address": "Multiple Address objects found for the given ID. Data inconsistency."
                        }
                    )
            else:
                address, _ = Address.objects.get_or_create(**address_data)
                instance.address = address
        else:
            instance.address = None
