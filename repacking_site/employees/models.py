from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    barcode = models.CharField(max_length=100)

    def __str__(self):
        return f'employee: username:{str(self.username)}, barcode:{str(self.barcode)}'
