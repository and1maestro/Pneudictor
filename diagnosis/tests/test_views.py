import pytest
from diagnosis.models import ClinicalData
from django.urls import reverse

@pytest.fixture
def make_clinical_data():
    def _make(user, **overrides):
        defaults = {
            "age": 20,
            "temperature": 36.6,
            "hemoglobin": 140.0
        }
        defaults.update(overrides)
        return ClinicalData.objects.create(user=user, **defaults)
    return _make

@pytest.mark.django_db
@pytest.mark.integration
class TestDiagnosisAccessControl:
    def test_history_redirects_anonymous_user_to_login(self, client):
        url = reverse("diagnosis:history")
        response = client.get(url)

        assert response.status_code == 302
        assert reverse("login") in response.url

    def test_owner_can_view_own_clinical_diagnosis(self, client, make_user, make_clinical_data):
        owner = make_user("owner")
        clinical_data = make_clinical_data(user=owner)
        client.force_login(owner)

        response = client.get(reverse("diagnosis:diagnosis_cd", kwargs={"pk": clinical_data.pk}))

        assert response.status_code == 200
        assert response.context["clinical_record"] == clinical_data

    def test_other_user_cannot_view_another_users_clinical_diagnosis(self, client, make_user, make_clinical_data):
        user1 = make_user("user1")
        user2 = make_user("user2", email="test2@test.com")
        clinical_data_1 = make_clinical_data(user=user1)
        client.force_login(user2)

        response = client.get(reverse("diagnosis:diagnosis_cd", kwargs={"pk": clinical_data_1.pk}))

        assert response.status_code == 302
        assert response.url == reverse("home")