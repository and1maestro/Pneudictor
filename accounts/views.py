import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponse
from config.settings import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY
from .forms import *
from .models import *


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy('accounts:profile')
    template_name = 'registration/profile.html'

    def get_object(self, *args, **kwargs):
        return self.request.user


def PremiumView(request):
    return render(request, 'accounts/premium.html')


stripe.api_key = STRIPE_SECRET_KEY


def create_checkout_session(request):
    if request.method == 'POST':
        try:
            domain_url = request.build_absolute_uri('/')[:-1]

            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': 1000,
                            'product_data': {
                                'name': 'Pneudictor Premium',
                                'description': 'Advanced analysis and history features',
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=domain_url + reverse('accounts:profile') + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + reverse('accounts:premium'),
            )
            return redirect(checkout_session.url)

        except Exception as e:
            return HttpResponse(f"Stripe error: {e}", status=400)

    return redirect('accounts:premium')
