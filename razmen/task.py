# tasks.py
from celery import shared_task
from datetime import datetime, timedelta
from django.utils import timezone
from .models import UserProfile

@shared_task
def burn_unused_coins():
    last_day_of_month = datetime.now().replace(day=1, month=datetime.now().month+1) - timedelta(days=1)
    unused_profiles = UserProfile.objects.filter(geek_coins__gt=0, user__last_login__lt=last_day_of_month)

    for profile in unused_profiles:
        profile.geek_coins = 0
        profile.save()
