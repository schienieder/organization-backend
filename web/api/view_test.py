from django.test import TestCase

from rest_framework.test import APIRequestFactory


class CreateUserTest(TestCase):
    factory = APIRequestFactory()
    request = factory.post("/api/create/", {"name": "test name"})
