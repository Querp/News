from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Create a superuser from environment variables"

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SU_NAME")
        password = os.environ.get("DJANGO_SU_PASSWORD")
        email = os.environ.get("DJANGO_SU_EMAIL", "")

        if not username or not password:
            self.stdout.write("Missing username or password")
            return

        User = get_user_model()
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(f"Superuser {username} created")
        else:
            self.stdout.write(f"Superuser {username} already exists")
