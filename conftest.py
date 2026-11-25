import pytest

@pytest.fixture
def make_user(django_user_model):
    def _make(username, password="Testpassword123", email=None, **extra_fields):
        return django_user_model.objects.create_user(
            username=username,
            password=password,
            email=f"{username}@test.com",
            **extra_fields
        )
    return _make