from django.urls import path
from .views import get_usd_to_eur_rate

urlpatterns = [
    path('usd-to-eur/', get_usd_to_eur_rate, name='usd_to_eur_rate'),
]
