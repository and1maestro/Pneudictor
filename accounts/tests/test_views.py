import pytest
from django.urls import reverse

@pytest.mark.unit
class TestCreateCheckoutSession:

    @pytest.fixture
    def url(self):
        return reverse("accounts:create_checkout_session")
    def test_get_request_redirects_to_premium(self, client, mocker, url):
        checkout = mocker.patch("accounts.views.stripe.checkout.Session.create")

        response = client.get(url)

        assert response.status_code == 302
        assert response.url == reverse("accounts:premium")
        checkout.assert_not_called()

    def test_post_creates_stripe_session_and_redirects(self, client, mocker, url):
        fake_session = mocker.Mock(url="https://checkout.stripe.com/test_session")
        checkout = mocker.patch("accounts.views.stripe.checkout.Session.create", return_value=fake_session)

        response = client.post(url)

        assert response.status_code == 302
        assert response.url == "https://checkout.stripe.com/test_session"
        checkout.assert_called_once()

    def test_post_returns_400_on_stripe_error(self, client, mocker, url):
        checkout = mocker.patch("accounts.views.stripe.checkout.Session.create", side_effect=Exception("API key invalid"))

        response = client.post(url)

        assert response.status_code == 400
        assert "Stripe error: API key invalid" in response.content.decode()

