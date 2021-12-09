from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    barcode_number = models.CharField(max_length=100)

    def __str__(self):
        return f'employee: username:{str(self.user.username)}, barcode:{str(self.barcode_number)}'
