from django.db import models
from django_ulidfield import ULIDField
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class Account(AbstractBaseUser):
    id = ULIDField(primary_key=True, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=10, db_column="phoneNumber", null=True)
    role = models.CharField(max_length=100, default='pending')
    date_created = models.DateTimeField(auto_now_add=True, db_column='dateCreated')
    status = models.CharField(max_length=20, default='active')
    is_active = models.BooleanField(default=True, db_column='isActive')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    class Meta:
        db_table = 'Account'
