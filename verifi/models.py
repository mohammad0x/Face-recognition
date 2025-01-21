import pytz
from django.db import models

# Create your models here.
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from jdatetime import datetime as jdatetime_datetime
from jalali_date import datetime2jalali, date2jalali


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Dbmodel(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='faces/')
    date = models.DateTimeField(auto_now_add=True)
    point = models.TextField(null=True, blank=False)

    def __str__(self) -> str:
        return self.name


class Face(models.Model):
    name = models.CharField(max_length=50, unique=True)
    date = models.CharField(default=jdatetime_datetime.now().strftime('%d %B %Y'), max_length=100)
    time = models.TimeField(auto_now_add=timezone.now)
    verify = models.BooleanField(default=False)
    noise = models.BooleanField(default=False)
    point = models.TextField(null=True, blank=False)


class Result(models.Model):
    name = models.CharField(max_length=100)
    recognition = models.CharField(max_length=100, unique=True)
    date = models.CharField(default=jdatetime_datetime.now().strftime('%d %B %Y'), max_length=100)
    time = models.TimeField(auto_now_add=True)
    noise = models.BooleanField(default=False)
    location = models.CharField(max_length=2, null=True, blank=False)

    def __str__(self) -> str:
        return self.name


class Attendance(models.Model):
    STATUS_CHOICES = (
        ('1', 'humanities'),
        ('2', 'library'),
        ('3', 'administrative'),
        ('4', 'engineering'),
        ('5', 'sama'),
        ('6', 'medical sciences'),
    )

    user = models.ForeignKey(Result, on_delete=models.CASCADE)
    flag = models.BooleanField(default=False)
    check_in_date = models.CharField(max_length=100)
    check_in_time = models.TimeField(auto_now_add=timezone.now, unique=True)
    location = models.CharField(max_length=5, choices=STATUS_CHOICES)
    login_or_logout = models.BooleanField(default=False)


class Getdate(models.Model):
    text = models.CharField(max_length=50)
    date_time = models.CharField(default=jdatetime_datetime.now().strftime('%d %B %Y'), max_length=100, unique=True)
