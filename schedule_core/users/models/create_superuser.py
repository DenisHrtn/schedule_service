from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config


class Command(BaseCommand):
    help = 'Create a superuser if one does not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(config('SUPERUSER_EMAIL'), config('SUPERUSER_PASSWORD'))
            self.stdout.write(self.style.SUCCESS('Superuser "admin" created successfully.'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser "admin" already exists.'))