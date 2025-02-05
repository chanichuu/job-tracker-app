from django.contrib.auth.models import User
import os


def init_test_user():
    user = User.objects.create(username=f"{os.getenv('TEST_USER')}")
    user.set_password(f"{os.getenv('TEST_PWD')}")
    user.save()

    return user
