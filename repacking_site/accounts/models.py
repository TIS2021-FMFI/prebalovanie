from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.core.exceptions import ValidationError


class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


def barcode_validator(barcode):
    if User.objects.filter(barcode=barcode).exists():
        raise ValidationError("Tento čiarový kód už je priradený inému používateľovi!", code='invalid')


class User(AbstractUser):
    class Meta:
        verbose_name = 'Účet'
        verbose_name_plural = 'Účty'
        permissions = (('history', 'Prístup k histórii'),
                       ('user_managment', 'Správa používateľov'),
                       ('sku_managment', 'Správa štandardov'),)
        default_permissions = ()

    barcode = models.CharField(max_length=100, unique=True, validators=[barcode_validator])

    def __str__(self):
        # return f'(username:{str(self.username)}, barcode:{str(self.barcode)})'
        return f'{str(self.username)}'

    @staticmethod
    def get_operator_by_sku_code(barcode):
        try:
            user = User.objects.get(barcode=barcode)
            return user
        except User.DoesNotExist:
            return None
