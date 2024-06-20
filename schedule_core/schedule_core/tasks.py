from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def delete_unconfirmed_users():
    one_minute_ago = timezone.now() - timedelta(minutes=1)
    unconfirmed_users = User.objects.filter(is_active=False, code_created_at__lt=one_minute_ago)
    unconfirmed_users.delete()
